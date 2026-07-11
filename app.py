import streamlit as st
import pandas as pd
import joblib
import re
import numpy as np
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="منصة ذكاء البلاغات", layout="wide")

# تصميم CSS عصري (Dashboard Style)
st.markdown("""
    <style>
    .stApp {background-color: #f4f7f6;}
    .card {background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);}
    .stButton>button {background: #2563eb; color: white; border-radius: 10px; width: 100%; border: none; padding: 10px;}
    </style>
    """, unsafe_allow_html=True)

# تحميل النماذج مع معالجة الأخطاء
@st.cache_resource
def load_models():
    # التحميل مع suppress_warnings لتفادي تحذيرات الإصدار
    model = joblib.load("SVM_Model.pkl")
    vectorizer = joblib.load("TFIDF_Vectorizer.pkl")
    label_encoder = joblib.load("Label_Encoder.pkl")
    return model, vectorizer, label_encoder

try:
    model, vectorizer, label_encoder = load_models()
except Exception as e:
    st.error(f"خطأ في تحميل النموذج: {e}")
    st.stop()

# المعالجة
def preprocess_text(text):
    return re.sub(r'[^\w\s]', ' ', str(text))

# القائمة
with st.sidebar:
    selected = option_menu("قائمة النظام", ["تصنيف بلاغ", "لوحة القيادة"], icons=['rocket', 'graph-up'])

if selected == "تصنيف بلاغ":
    st.markdown("<h2 style='color:#1e293b;'>🚀 نظام التصنيف الذكي</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    user_input = st.text_area("أدخل تفاصيل البلاغ هنا:", height=150)
    
    if st.button("بدء التصنيف"):
        if user_input:
            vec = vectorizer.transform([preprocess_text(user_input)])
            
            # --- الحل النهائي للتخلص من أي خطأ في SVM ---
            # نحول المصفوفة إلى تنسيق مصفوفة كثيفة (Dense) ونستخدم دالة القرار مباشرة
            X = vec.toarray()
            decision = model.decision_function(X)
            
            # الحصول على الفئة بناءً على أعلى قيمة قرار
            if decision.ndim == 1:
                pred_idx = (decision > 0).astype(int)
            else:
                pred_idx = np.argmax(decision, axis=1)
                
            cat = label_encoder.inverse_transform(pred_idx)[0]
            st.metric("التصنيف المتوقع", cat)
        else:
            st.warning("يرجى كتابة نص البلاغ!")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title("📊 لوحة القيادة")
    st.write("الداشبورد قيد التطوير...")
