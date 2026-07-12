import streamlit as st
import pandas as pd
import pickle
import re
import plotly.express as px
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="GHARS - منصة ذكية", layout="wide")

# القاموس الفعلي الخاص بكِ
category_map = {
    0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق", 4: "الصيانة",
    5: "الطرق", 6: "المرور", 7: "النظافة", 8: "تشوه بصري", 9: "تصريف الأمطار",
    10: "حدائق", 11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"
}

# كلاس لفك تشفير النموذج
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'sklearn.linear_model._logistic':
            return super().find_class('sklearn.linear_model', name)
        return super().find_class(module, name)

# تحميل النموذج والـ Vectorizer (مع Cached لتسريع الأداء)
@st.cache_resource
def load_models():
    with open('model.pkl', 'rb') as f:
        model = CustomUnpickler(f).load()
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = CustomUnpickler(f).load()
    return model, vectorizer

# دالة تنظيف النص
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[\d\u0660-\u0669]+', '', text)
    return text.strip()

# تحميل النماذج
try:
    model, vectorizer = load_models()
except Exception as e:
    st.error(f"خطأ في تحميل النموذج: {e}")

# ذاكرة البلاغات
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# واجهة التطبيق
st.title("🛡️ نظام التصنيف ")
selected = option_menu(None, ["إرسال بلاغ", "لوحة الإحصائيات"], icons=['pencil', 'bar-chart'], orientation="horizontal")

if selected == "إرسال بلاغ":
    user_input = st.text_area("أدخلي تفاصيل البلاغ:", height=150)
    if st.button("🚀 تصنيف البلاغ"):
        if user_input:
            cleaned = clean_text(user_input)
            vec = vectorizer.transform([cleaned])
            pred_numeric = int(model.predict(vec)[0])
            category = category_map.get(pred_numeric, "غير مصنف")
            
            st.session_state.reports = pd.concat([st.session_state.reports, pd.DataFrame({'القسم': [category], 'التفاصيل': [user_input]})], ignore_index=True)
            st.success(f"تم تصنيف البلاغ إلى: **{category}**")

elif selected == "لوحة الإحصائيات":
    if not st.session_state.reports.empty:
        fig = px.pie(st.session_state.reports, names='القسم', title="توزيع البلاغات")
        st.plotly_chart(fig, use_container_width=True)
        st.table(st.session_state.reports)
