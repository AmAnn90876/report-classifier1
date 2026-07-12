import streamlit as st
import pandas as pd
import pickle
import re
import plotly.express as px
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="GHARS - منصة ذكية", layout="wide")

# 1. القاموس الفعلي والمطابق لنتائج الـ LabelEncoder
category_map = {
    0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق", 4: "الصيانة",
    5: "الطرق", 6: "المرور", 7: "النظافة", 8: "تشوه بصري", 9: "تصريف الأمطار",
    10: "حدائق", 11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"
}

# 2. كلاس لفك تشفير النموذج (لضمان توافق الإصدارات)
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'sklearn.linear_model._logistic':
            return super().find_class('sklearn.linear_model', name)
        return super().find_class(module, name)

# 3. تحميل النماذج (باستخدام أسماء الملفات الصحيحة من مشروعك)
@st.cache_resource
def load_models():
    with open('SVM_Model (2).pkl', 'rb') as f:
        model = CustomUnpickler(f).load()
    with open('TFIDF_Vectorizer.pkl', 'rb') as f:
        vectorizer = CustomUnpickler(f).load()
    return model, vectorizer

# 4. دالة تنظيف النص
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[\d\u0660-\u0669]+', '', text)
    return text.strip()

# تحميل النماذج
try:
    model, vectorizer = load_models()
except Exception as e:
    st.error(f"خطأ في تحميل الملفات: {e}")
    st.stop()

# 5. ذاكرة البلاغات
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# 6. واجهة التطبيق
st.title("🛡️ GHARS - نظام التصنيف الذكي")

selected = option_menu(
    menu_title=None, 
    options=["إرسال بلاغ", "لوحة الإحصائيات"], 
    icons=['pencil', 'bar-chart'], 
    orientation="horizontal"
)

if selected == "إرسال بلاغ":
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:", height=150)
    if st.button("🚀 تصنيف وإرسال"):
        if user_input.strip():
            cleaned = clean_text(user_input)
            vec = vectorizer.transform([cleaned])
            pred_numeric = int(model.predict(vec)[0])
            category = category_map.get(pred_numeric, f"قسم {pred_numeric}")
            
            new_report = pd.DataFrame({'القسم': [category], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_report], ignore_index=True)
            st.success(f"✅ تم تصنيف البلاغ إلى: **{category}**")
        else:
            st.warning("يرجى كتابة نص البلاغ.")

elif selected == "لوحة الإحصائيات":
    if not st.session_state.reports.empty:
        fig = px.pie(st.session_state.reports, names='القسم', title="توزيع البلاغات حسب الأقسام")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(st.session_state.reports, use_container_width=True)
    else:
        st.info("لا توجد بلاغات حالياً.")
