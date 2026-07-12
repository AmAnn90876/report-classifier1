import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="GHARS - منصة ذكية", layout="wide")

# 1. ذاكرة التطبيق لحفظ البلاغات أثناء الجلسة
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# 2. دالة تصنيف ذكية (تُحمل المكتبات عند الطلب فقط لتجنب انهيار الخادم)
def get_prediction(text):
    # نستدعي المكتبات هنا (داخل الدالة) وليس في بداية الملف
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import Pipeline
    
    # بيانات التدريب
    training_data = [
        ("نفايات متراكمة حاويات زبالة روائح مخلفات تنظيف", "نظافة"),
        ("تسرب مياه كسر ماسورة انفجار تجمع مياه طفح", "مياه"),
        ("الإنارة معطلة الشارع مظلم عمود النور طافي ظلام", "إنارة"),
        ("حفرة طريق هبوط أسفلت تشققات رصيف مطبات", "طرق")
    ]
    df = pd.DataFrame(training_data, columns=['text', 'label'])
    
    # بناء النموذج وتدريبه
    model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
    model.fit(df['text'], df['label'])
    
    return model.predict([text])[0]

# 3. واجهة المستخدم
st.title("🛡️منصة تصنيف البلاغات الذكية")

# القائمة الأفقية
selected = option_menu(
    menu_title=None, 
    options=["إرسال بلاغ", "لوحة الإحصائيات"], 
    icons=['pencil', 'bar-chart'], 
    orientation="horizontal"
)

if selected == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:", height=150, placeholder="مثال: يوجد تجمع مياه في الشارع...")
    
    if st.button("🚀 تصنيف وإرسال"):
        if user_input.strip():
            with st.spinner('جاري تحليل البلاغ...'):
                pred = get_prediction(user_input)
                # حفظ في الذاكرة
                new_report = pd.DataFrame({'القسم': [pred], 'التفاصيل': [user_input]})
                st.session_state.reports = pd.concat([st.session_state.reports, new_report], ignore_index=True)
                st.success(f"✅ تم تصنيف البلاغ بنجاح إلى: **{pred}**")
        else:
            st.warning("يرجى كتابة نص البلاغ أولاً.")

elif selected == "لوحة الإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء")
    
    if not st.session_state.reports.empty:
        # حساب الإحصائيات
        stats = st.session_state.reports['القسم'].value_counts().reset_index()
        stats.columns = ['القسم', 'العدد']
        
        # عرض الرسم البياني
        fig = px.pie(stats, values='العدد', names='القسم', title="توزيع البلاغات حسب الأقسام")
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض جدول البيانات
        st.subheader("سجل البلاغات المرفوعة")
        st.dataframe(st.session_state.reports, use_container_width=True)
    else:
        st.info("لا توجد بلاغات حالياً، أرسلي بلاغاً من القائمة الأولى لتظهر الإحصائيات هنا.")
