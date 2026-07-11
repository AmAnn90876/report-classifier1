import streamlit as st
import pandas as pd
import joblib
import re
import numpy as np
import os
import plotly.express as px
from streamlit_option_menu import option_menu

# إعداد الصفحة لتكون فخمة
st.set_page_config(page_title="منصة ذكاء البلاغات", layout="wide", page_icon="🏛️")

# تصميم CSS لعرض "كرتيف" (Modern Dashboard UI)
st.markdown("""
    <style>
    .stApp {background-color: #f8fafc;}
    .card {background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);}
    .stButton>button {width: 100%; border-radius: 12px; background: #4f46e5; color: white; font-weight: bold; border: none; padding: 12px; transition: 0.3s;}
    .stButton>button:hover {background: #4338ca; transform: scale(1.02);}
    h1, h2 {color: #1e293b; font-family: 'Segoe UI', sans-serif;}
    </style>
    """, unsafe_allow_html=True)

# تحميل النماذج (بمسار ديناميكي ومضمون)
@st.cache_resource
def load_models():
    base_path = os.path.dirname(__file__)
    # استخدام اسم الملف المحدث كما هو في GitHub
    model = joblib.load(os.path.join(base_path, "SVM_Model (2).pkl"))
    vectorizer = joblib.load(os.path.join(base_path, "TFIDF_Vectorizer.pkl"))
    label_encoder = joblib.load(os.path.join(base_path, "Label_Encoder.pkl"))
    return model, vectorizer, label_encoder

try:
    model, vectorizer, label_encoder = load_models()
except Exception as e:
    st.error(f"❌ خطأ في تحميل النماذج: تأكدي من أن الملفات (SVM_Model (2).pkl, TFIDF_Vectorizer.pkl, Label_Encoder.pkl) موجودة في المجلد الرئيسي.")
    st.stop()

# القائمة الجانبية
with st.sidebar:
    selected = option_menu("نظام التصنيف الذكي", ["تصنيف بلاغ", "لوحة القيادة"], 
                           icons=['rocket', 'graph-up'], menu_icon="cast", default_index=0)

# محتوى الصفحة
if selected == "تصنيف بلاغ":
    st.title("🏛️ منصة تصنيف البلاغات الذكية")
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        user_input = st.text_area("أدخل تفاصيل البلاغ هنا:", height=180, placeholder="مثال: يوجد تسرب مياه في الشارع الرئيسي...")
        if st.button("🚀 تحليل البلاغ"):
            if user_input:
                vec = vectorizer.transform([re.sub(r'[^\w\s]', ' ', user_input)])
                # التنبؤ المباشر (بعد حل مشكلة توافق الإصدارات)
                pred = model.predict(vec)
                cat = label_encoder.inverse_transform(pred)[0]
                st.success(f"### 🎯 التصنيف المتوقع: {cat}")
            else:
                st.warning("⚠️ يرجى كتابة نص البلاغ.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.info("💡 **نصيحة تقنية:** يقوم النظام بمعالجة النصوص وتحويلها إلى متجهات (Vectors) ثم تصنيفها باستخدام خوارزمية SVM المتقدمة.")

else:
    st.title("📊 لوحة المؤشرات (Dashboard)")
    # نموذج للوحة تحكم تفاعلية
    data = pd.DataFrame({'التصنيف': ['نظافة', 'إنارة', 'طرق', 'مياه'], 'عدد البلاغات': [45, 20, 35, 15]})
    fig = px.bar(data, x='التصنيف', y='عدد البلاغات', color='عدد البلاغات', color_continuous_scale='Bluered')
    st.plotly_chart(fig, use_container_width=True)
