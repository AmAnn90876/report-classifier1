import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title=" تصنيف البلاغات", layout="wide")

# تهيئة الذاكرة
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# محرك التصنيف
def smart_classify(text):
    text = text.lower()
    if any(word in text for word in ['إنارة', 'نور', 'إضاءة', 'لمبة']): return "الإنارة"
    if any(word in text for word in ['تشوه', 'كتابة', 'جدار']): return "التشوه البصري"
    return "الصيانة العامة"

# القائمة الجانبية للتحكم في التنقل
page = st.sidebar.radio("التنقل", ["الرئيسية", "إرسال بلاغ", "لوحة الإحصائيات"])

if page == "الرئيسية":
    st.title("🛡️ منصة GHARS الذكية")
    st.write("أهلاً بك في نظام إدارة البلاغات. اختر قسماً من القائمة الجانبية.")

elif page == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:")
    if st.button("🚀 تصنيف وإرسال"):
        if user_input.strip():
            cat = smart_classify(user_input)
            new_data = pd.DataFrame({'القسم': [cat], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_data], ignore_index=True)
            st.success(f"تم الإرسال إلى: {cat}")

elif page == "لوحة الإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء")
    if not st.session_state.reports.empty:
        stats = st.session_state.reports['القسم'].value_counts().reset_index()
        fig = px.pie(stats, values='count', names='القسم')
        st.plotly_chart(fig)
        st.dataframe(st.session_state.reports)
    else:
        st.info("لا توجد بيانات.")
