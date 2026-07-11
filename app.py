import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from streamlit_option_menu import option_menu
import plotly.express as px

st.set_page_config(page_title="GHARS - منصة ذكية", layout="wide")

# 1. ذاكرة التطبيق (لحفظ البلاغات)
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# 2. النموذج الذكي
training_data = [
    ("نفايات متراكمة حاويات زبالة روائح مخلفات تنظيف", "نظافة"),
    ("تسرب مياه كسر ماسورة انفجار تجمع مياه طفح", "مياه"),
    ("الإنارة معطلة الشارع مظلم عمود النور طافي ظلام", "إنارة"),
    ("حفرة طريق هبوط أسفلت تشققات رصيف مطبات", "طرق")
]
df = pd.DataFrame(training_data, columns=['text', 'label'])
model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
model.fit(df['text'], df['label'])

# 3. القائمة
selected = option_menu(None, ["إرسال بلاغ", "لوحة الإحصائيات"], icons=['pencil', 'bar-chart'], orientation="horizontal")

if selected == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    user_input = st.text_area("تفاصيل البلاغ:", height=100)
    if st.button("🚀 تصنيف وإرسال"):
        if user_input:
            pred = model.predict([user_input])[0]
            # حفظ البلاغ في الذاكرة
            new_report = pd.DataFrame({'القسم': [pred], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_report], ignore_index=True)
            st.success(f"تم تصنيف البلاغ كـ: {pred}")
        else:
            st.warning("يرجى كتابة نص البلاغ")

elif selected == "لوحة الإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء")
    if not st.session_state.reports.empty:
        # حساب الإحصائيات
        stats = st.session_state.reports['القسم'].value_counts().reset_index()
        stats.columns = ['القسم', 'العدد']
        
        # عرض الرسم البياني
        fig = px.pie(stats, values='العدد', names='القسم', title="توزيع البلاغات حسب القسم")
        st.plotly_chart(fig, use_container_width=True)
        
        st.table(st.session_state.reports)
    else:
        st.info("لا توجد بلاغات حالياً، أرسلي بلاغاً لتظهر الإحصائيات.")
