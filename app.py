import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="منصة بلاغات ذكية", layout="wide", page_icon="🚀")

# تصميم CSS لعرض "كرتيف" وعصري
st.markdown("""
    <style>
    .stApp {background-color: #f0f2f6;}
    .css-1r6slp0 {padding: 2rem 1rem;}
    .block-container {background-color: white; padding: 2rem; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);}
    .stButton>button {width: 100%; border-radius: 10px; height: 3em; background: #2563eb; color: white; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 1. تدريب النموذج الذكي (الخلفية)
data = {
    "text": ["نظافة", "نفايات", "زبالة", "قمامة", "روائح", "مياه", "تسريب", "ماسورة", "انفجار", "إنارة", "لمبة", "ظلام", "طرق", "حفرة", "أسفلت", "مطبات"],
    "label": ["نظافة", "نظافة", "نظافة", "نظافة", "نظافة", "مياه", "مياه", "مياه", "مياه", "إنارة", "إنارة", "إنارة", "طرق", "طرق", "طرق", "طرق"]
}
model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
model.fit(data['text'], data['label'])

# 2. القائمة الجانبية (شكل عصري)
with st.sidebar:
    selected = option_menu("القائمة الرئيسية", ["إرسال بلاغ", "إحصائيات"], icons=['pencil-square', 'bar-chart'], menu_icon="cast")

# 3. واجهة إرسال البلاغ
if selected == "إرسال بلاغ":
    st.markdown("## 📋 تقديم بلاغ جديد")
    st.write("الرجاء اختيار القسم وتعبئة التفاصيل أدناه:")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # اختيار القسم (محاكاة لاقتراح المستخدم)
        category_choice = st.selectbox("اقتراح صنف البلاغ:", ["نظافة", "مياه", "إنارة", "طرق"])
    
    with col2:
        user_input = st.text_area("تفاصيل البلاغ:", height=100, placeholder="مثال: هناك تسريب مياه في شارع...")
    
    if st.button("🚀 تحليل وإرسال البلاغ"):
        if user_input:
            prediction = model.predict([user_input])[0]
            st.success(f"### تم التحليل بنجاح!")
            st.info(f"القسم المقترح من النظام: **{prediction}**")
            st.write(f"ملاحظة: لقد قمت باقتراح قسم: **{category_choice}**")
        else:
            st.warning("يرجى كتابة نص البلاغ!")

else:
    st.title("📊 لوحة الإحصائيات")
    st.write("هنا ستظهر إحصائيات البلاغات الواردة (قيد التطوير).")

# كود إضافي لقياس "مستوى الأولوية"
if "خطر" in user_input or "عاجل" in user_input or "انهيار" in user_input:
    st.error("🚨 تصنيف أولوية: طارئ (يجب معالجته فوراً)")
else:
    st.success("✅ تصنيف أولوية: عادي (مجدول)")
