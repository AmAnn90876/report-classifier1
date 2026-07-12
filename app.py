import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة (يجب أن يكون أول أمر في Streamlit)
st.set_page_config(page_title=" منصة البلاغات", layout="wide")

# 2. تهيئة الذاكرة (لضمان بقاء البيانات عند التنقل)
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# 3. قائمة الخيارات (كما طلبتها بالضبط)
category_options = [
    "إنارة", "الإنارة", "التشوه البصري", "الحدائق", "الصيانة", 
    "الطرق", "المرور", "النظافة", "تشوه بصري", "تصريف الأمطار", 
    "حدائق", "حفريات", "طرق", "مبانٍ قابلة للسقوط", "نظافة"
]

# 4. القائمة الجانبية للتنقل
menu = st.sidebar.radio("القائمة", ["الرئيسية", "إرسال بلاغ", "لوحة الإحصائيات"])

# 5. منطق الصفحات
if menu == "الرئيسية":
    st.title("🛡️ منصة البلاغات ")
    st.markdown("---")
    st.write("مرحباً بك في نظام إدارة البلاغات الخاص بمشروع GHARS.")
    st.write("استخدم القائمة الجانبية للتنقل بين الصفحات.")

elif menu == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    selected_cat = st.selectbox("حدد القسم بدقة:", options=category_options)
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:", height=150)
    
    if st.button("🚀 إرسال البلاغ"):
        if user_input.strip():
            # إضافة البيانات للجدول في الذاكرة
            new_row = pd.DataFrame({'القسم': [selected_cat], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_row], ignore_index=True)
            st.success(f"✅ تم حفظ البلاغ بنجاح في قسم: **{selected_cat}**")
        else:
            st.warning("يرجى كتابة نص البلاغ قبل الإرسال.")

elif menu == "لوحة الإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء")
    
    if not st.session_state.reports.empty:
        # عرض الرسم البياني
        fig = px.pie(st.session_state.reports, names='القسم', title="توزيع البلاغات")
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض الجدول
        st.subheader("سجل البلاغات")
        st.dataframe(st.session_state.reports, use_container_width=True)
    else:
        st.info("لا توجد بلاغات مسجلة حالياً.")
