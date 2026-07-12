import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from streamlit_option_menu import option_menu
import plotly.express as px

st.set_page_config(page_title="نظام تصنيف البلاغات", layout="wide")

# القائمة المعتمدة رسمياً (تجنبنا الأرقام والقاموس لضمان الدقة)
categories = [
    "إنارة", "تشوه بصري", "حدائق", "صيانة", "طرق", 
    "مرور", "نظافة", "تصريف أمطار", "مبانٍ قابلة للسقوط"
]

if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# تدريب النموذج مباشرة على الأسماء المعتمدة
training_data = [
    ("إنارة عمود نور لمبة طافي", "إنارة"),
    ("تشوه بصري كتابات على الجدار", "تشوه بصري"),
    ("حدائق تشجير ري", "حدائق"),
    ("صيانة مباني", "صيانة"),
    ("طرق حفرة هبوط أسفلت رصيف", "طرق"),
    ("مرور زحام تنظيم", "مرور"),
    ("نظافة زبالة حاوية روائح", "نظافة"),
    ("تصريف أمطار مياه طفح ماسورة", "تصريف أمطار"),
    ("مبنى قديم سقوط تصدع", "مبانٍ قابلة للسقوط")
]
df = pd.DataFrame(training_data, columns=['text', 'label'])
model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
model.fit(df['text'], df['label'])

selected = option_menu(None, ["إرسال بلاغ", "الإحصائيات"], orientation="horizontal")

if selected == "إرسال بلاغ":
    st.subheader("تقديم بلاغ جديد")
    user_input = st.text_area("تفاصيل البلاغ:", height=150)
    
    if st.button("تحليل وإرسال"):
        if user_input:
            # النتيجة ستخرج نصاً مباشراً ولا داعي لأي قاموس أرقام
            final_label = model.predict([user_input])[0]
            
            new_report = pd.DataFrame({'القسم': [final_label], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_report], ignore_index=True)
            
            st.success(f"التصنيف: {final_label}")
        else:
            st.warning("يرجى إدخال تفاصيل البلاغ.")

elif selected == "الإحصائيات":
    st.subheader("الإحصائيات")
    if not st.session_state.reports.empty:
        stats = st.session_state.reports["القسم"].value_counts().reset_index()
        stats.columns = ["القسم", "العدد"]
        
        fig = px.bar(stats, x="القسم", y="العدد")
        st.plotly_chart(fig)
        st.table(st.session_state.reports)
    else:
        st.write("لا توجد بلاغات.")
