import streamlit as st
import pandas as pd
import joblib
import re
import numpy as np
import os
from streamlit_option_menu import option_menu

# إعداد الصفحة لتكون بوضع واسع
st.set_page_config(page_title="منصة ذكاء البلاغات", layout="wide")

# تصميم CSS عصري (Dashboard Style)
st.markdown("""
    <style>
    .stApp {background-color: #f4f7f6;}
    .card {background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);}
    .stButton>button {background: #2563eb; color: white; border-radius: 10px; width: 100%; border: none; padding: 10px; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# تحميل النماذج (بمسار ديناميكي لضمان عدم حدوث خطأ الملف)
@st.cache_resource
def load_models():
    # المسار الحالي للملف
    base_path = os.path.dirname(__file__)
    model = joblib.load(os.path.join(base_path, "SVM_Model.pkl"))
    vectorizer = joblib.load(os.path.join(base_path, "TFIDF_Vectorizer.pkl"))
    label_encoder = joblib.load(os.path.join(base_path, "Label_Encoder.pkl"))
    return model, vectorizer, label_encoder

try:
    model, vectorizer, label_encoder = load_models()
except Exception as e:
    st.error(f"❌ خطأ: لم يتم العثور على ملفات النموذج. تأكدي من رفعها في نفس مجلد app.py. التفاصيل: {e}")
    st.stop()

# دالة المعالجة
def preprocess_text(text):
    return re.sub(r'[^\w\s]', ' ', str(text))

# القائمة الجانبية الاحترافية
with st.sidebar:
    selected = option_menu("قائمة النظام", ["تصنيف بلاغ", "لوحة القيادة"], 
                           icons=['rocket', 'graph-up'], menu_icon="cast", default_index=0)

# محتوى الصفحة
if selected == "تصنيف بلاغ":
    st.markdown("<h2 style='color:#1e293b;'>🚀 منصة التصنيف الذكي للبلاغات</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    user_input = st.text_area("أدخل تفاصيل البلاغ هنا:", height=150, placeholder="مثال: تسرب مياه في شارع...")
    
    if st.button("تحليل البلاغ"):
        if user_input:
            vec = vectorizer.transform([preprocess_text(user_input)])
            
            # التصنيف المباشر (بعد إعادة حفظ النموذج بنجاح)
            try:
                pred = model.predict(vec)
                cat = label_encoder.inverse_transform(pred)[0]
            except:
                # حل احتياطي إذا حدث أي خطأ تقني
                pred = np.argmax(model.decision_function(vec.toarray()), axis=1)
                cat = label_encoder.inverse_transform(pred)[0]
                
            st.success(f"### النتيجة: {cat}")
        else:
            st.warning("يرجى إدخال نص البلاغ!")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title("📊 لوحة القيادة (Dashboard)")
    st.info("هنا يمكنك عرض تحليلات البلاغات.")
