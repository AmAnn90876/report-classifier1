import streamlit as st
import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords

# إعداد الصفحة لتكون بوضع واسع
st.set_page_config(page_title="نظام ذكاء البلاغات", layout="wide")

# تنسيق CSS مخصص للواجهة (لجعلها فخمة)
st.markdown("""
    <style>
    .main {background-color: #f5f7f9;}
    .stButton>button {width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; font-weight: bold;}
    .css-1d391kg {background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_models():
    model = joblib.load("SVM_Model.pkl")
    vectorizer = joblib.load("TFIDF_Vectorizer.pkl")
    label_encoder = joblib.load("Label_Encoder.pkl")
    return model, vectorizer, label_encoder

model, vectorizer, label_encoder = load_models()

# المعالجة (نفسها)
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'[\d]+', '', text)
    return text

# العنوان الرئيسي
st.title("🏛️ منصة ذكاء البلاغات البلدية")
st.markdown("---")

# القائمة الجانبية
menu = st.sidebar.radio("📋 القائمة الرئيسية", ["تصنيف بلاغ جديد", "تحليل إحصائي"])

if menu == "تصنيف بلاغ جديد":
    st.subheader("📝 نموذج التصنيف الذكي")
    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.text_area("اكتب تفاصيل البلاغ هنا:", height=200, placeholder="مثال: يوجد تسريب مياه في الشارع الرئيسي...")
        if st.button("🚀 تصنيف البلاغ"):
            if user_input:
                cleaned = preprocess_text(user_input)
                vec = vectorizer.transform([cleaned])
                # حل الخطأ باستخدام toarray()
                pred = model.predict(vec.toarray())
                cat = label_encoder.inverse_transform(pred)[0]
                st.success(f"### النتيجة: {cat}")
            else:
                st.warning("الرجاء إدخال نص البلاغ!")
    with col2:
        st.info("💡 **كيفية الاستخدام:**\n1. أدخل نص البلاغ بوضوح.\n2. اضغط على زر التصنيف.\n3. سيقوم النظام بتحليل البلاغ وتوجيهه للجهة المختصة.")

else:
    st.header("📈 لوحة مؤشرات الأداء")
    uploaded_file = st.file_uploader("ارفع ملف البلاغات (Excel)", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("تم رفع الملف بنجاح")
        # هنا يمكنك إضافة الإحصائيات الفخمةالملف المرفوع يجب أن يحتوي على عمودين باسم 'complaint' و 'category'.")
