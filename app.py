import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import plotly.express as px

# 1. إعداد الصفحة وتصميم احترافي
st.set_page_config(page_title="نظام تصنيف البلاغات", layout="wide")
st.markdown("""
    <style>
    .stApp {background-color: #f4f7f6;}
    .report-card {background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    h1 {color: #1e3d59; text-align: center; font-weight: 700;}
    </style>
""", unsafe_allow_html=True)

# 2. القاموس الفعلي الخاص بك
category_map = {
    0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق", 4: "الصيانة",
    5: "الطرق", 6: "المرور", 7: "النظافة", 8: "تشوه بصري", 9: "تصريف الأمطار",
    10: "حدائق", 11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"
}

# 3. إدارة الذاكرة
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['البلاغ', 'التصنيف'])

# 4. تدريب النموذج (النموذج يتعلم الأرقام ليتطابق مع الـ LabelEncoder)
# ملاحظة: في مشروعك الأصلي، تأكدي أن الـ model.fit استخدم الأرقام (0-14)
training_data = [("لمبة طافي", 0), ("إنارة معطلة", 1), ("تشوه بصر", 2), ("حفرة", 12), ("نظافة", 14)]
X, y = [d[0] for d in training_data], [d[1] for d in training_data]
model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
model.fit(X, y)

# 5. الواجهة الإبداعية
st.title("🛡️ نظام تصنيف البلاغات الذكي")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.subheader("إرسال بلاغ")
    user_input = st.text_area("أدخلي تفاصيل البلاغ:", height=120)
    if st.button("تصنيف البلاغ"):
        if user_input:
            pred_index = model.predict([user_input])[0]
            label_name = category_map.get(pred_index, "غير معروف")
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame({'البلاغ': [user_input], 'التصنيف': [label_name]})], ignore_index=True)
            st.success(f"تم تصنيف البلاغ إلى: {label_name}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.subheader("تحليلات البلاغات")
    if not st.session_state.data.empty:
        fig = px.pie(st.session_state.data, names='التصنيف', title="توزيع البلاغات")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("لا توجد بلاغات لعرض الإحصائيات.")
    st.markdown('</div>', unsafe_allow_html=True)
