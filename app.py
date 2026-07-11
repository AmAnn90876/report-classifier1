import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# إعداد الصفحة
st.set_page_config(page_title="منصة ذكاء البلاغات", layout="wide")

st.title("🏛️ منصة تصنيف البلاغات (إصدار الطوارئ)")

# بيانات تجريبية للتدريب (لتشغيل التطبيق فوراً)
texts = ["تسرب مياه", "إنارة متعطلة", "حفرة في الشارع", "نفايات متراكمة"]
labels = ["مياه", "إنارة", "طرق", "نظافة"]

# تدريب نموذج سريع (بديل للنموذج التالف)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
model = LogisticRegression()
model.fit(X, labels)

# واجهة المستخدم
user_input = st.text_area("أدخل تفاصيل البلاغ:")

if st.button("تحليل البلاغ"):
    if user_input:
        vec = vectorizer.transform([user_input])
        prediction = model.predict(vec)[0]
        st.success(f"### التصنيف المتوقع: {prediction}")
    else:
        st.warning("يرجى كتابة نص البلاغ!")
