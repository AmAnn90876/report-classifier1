import streamlit as st
import pandas as pd
import joblib
import re
import numpy as np
import os
import plotly.express as px
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="منصة ذكاء البلاغات", layout="wide", page_icon="🏛️")

# CSS لتصميم فخم
st.markdown("""
    <style>
    .stApp {background-color: #f8fafc;}
    .card {background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);}
    .stButton>button {width: 100%; border-radius: 12px; background: #4f46e5; color: white; font-weight: bold; border: none; padding: 12px;}
    </style>
    """, unsafe_allow_html=True)

# تحميل النماذج
@st.cache_resource
def load_models():
    base_path = os.path.dirname(__file__)
    model = joblib.load(os.path.join(base_path, "SVM_Model (2).pkl"))
    vectorizer = joblib.load(os.path.join(base_path, "TFIDF_Vectorizer.pkl"))
    label_encoder = joblib.load(os.path.join(base_path, "Label_Encoder.pkl"))
    return model, vectorizer, label_encoder

model, vectorizer, label_encoder = load_models()

# القائمة
with st.sidebar:
    selected = option_menu("نظام التصنيف", ["تصنيف بلاغ", "لوحة القيادة"], icons=['rocket', 'graph-up'])

if selected == "تصنيف بلاغ":
    st.title("🏛️ منصة تصنيف البلاغات")
    user_input = st.text_area("أدخل تفاصيل البلاغ:", height=150)
    
    if st.button("🚀 تحليل وتصنيف"):
        if user_input:
            # 1. تحويل النص
            vec = vectorizer.transform([re.sub(r'[^\w\s]', ' ', user_input)])
            X = vec.toarray()
            
            # 2. الحساب الرياضي المباشر (تجنباً لأي خطأ في المكتبة)
            # النتيجة = (المدخلات * الأوزان) + الانحياز
            decision = np.dot(X, model.coef_.T) + model.intercept_
            
            # 3. اختيار الفئة ذات أعلى قيمة
            pred_idx = np.argmax(decision, axis=1)
            cat = label_encoder.inverse_transform(pred_idx)[0]
            
            st.success(f"### النتيجة: {cat}")
        else:
            st.warning("يرجى كتابة نص البلاغ!")
else:
    st.title("📊 لوحة القيادة")
    data = pd.DataFrame({'التصنيف': ['نظافة', 'إنارة', 'طرق', 'مياه'], 'عدد البلاغات': [45, 20, 35, 15]})
    fig = px.bar(data, x='التصنيف', y='عدد البلاغات', color='عدد البلاغات', color_continuous_scale='Bluered')
    st.plotly_chart(fig, use_container_width=True)
