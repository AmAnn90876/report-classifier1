import streamlit as st
import pandas as pd
import joblib
import re
import numpy as np
import nltk
from nltk.corpus import stopwords

# إعداد الصفحة
st.set_page_config(page_title="نظام ذكاء البلاغات", layout="wide")

# CSS لتصميم فخم
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {width: 100%; border-radius: 8px; background-color: #1e3a8a; color: white; font-weight: bold;}
    .stSuccess {border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

# تحميل النماذج
@st.cache_resource
def load_models():
    model = joblib.load("SVM_Model.pkl")
    vectorizer = joblib.load("TFIDF_Vectorizer.pkl")
    label_encoder = joblib.load("Label_Encoder.pkl")
    return model, vectorizer, label_encoder

model, vectorizer, label_encoder = load_models()

# دالة المعالجة
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'[\d]+', '', text)
    return text

# الواجهة
st.title("🏛️ منصة ذكاء البلاغات البلدية")
menu = st.sidebar.radio("📋 القائمة الرئيسية", ["تصنيف بلاغ جديد", "تحليل إحصائي"])

if menu == "تصنيف بلاغ جديد":
    st.subheader("📝 نموذج التصنيف الذكي")
    user_input = st.text_area("أدخل نص البلاغ هنا:", height=150)
    
    if st.button("🚀 تصنيف البلاغ"):
        if user_input:
            cleaned = preprocess_text(user_input)
            vec = vectorizer.transform([cleaned])
            
            # الحل الاحترافي لتجاوز مشكلة SVM
            try:
                pred = model.predict(vec.toarray())
            except:
                pred = model.decision_function(vec.toarray())
                pred = np.argmax(pred, axis=1)
                
            cat = label_encoder.inverse_transform(pred)[0]
            st.success(f"### النتيجة: {cat}")
        else:
            st.warning("الرجاء إدخال نص البلاغ!")

else:
    st.header("📈 لوحة مؤشرات الأداء")
    uploaded_file = st.file_uploader("ارفع ملف البلاغات (Excel)", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("تم رفع البيانات بنجاح.")
        st.dataframe(df.head())
