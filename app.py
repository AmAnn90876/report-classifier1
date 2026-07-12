import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="GHARS - منصة بلاغات", layout="wide")

# تهيئة الذاكرة (للحفاظ على البيانات أثناء التنقل)
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# القائمة الدقيقة للخيارات
category_options = [
    "إنارة", "الإنارة", "التشوه البصري", "الحدائق", "الصيانة", 
    "الطرق", "المرور", "النظافة", "تشوه بصري", "تصريف الأمطار", 
    "حدائق", "حفريات", "طرق", "مبانٍ قابلة للسقوط", "نظافة"
]

# القائمة الجانبية للتنقل
menu = st.sidebar.radio("القائمة", ["الرئيسية", "إرسال بلاغ", "لوحة الإحصائيات"])

# 1. صفحة الترحيب
if menu == "الرئيسية":
    st.title("🛡️ منصة البلاغات")
    st.markdown("""
    ### أهلاً بك في نظام إدارة البلاغات
    هذا النظام مصمم لتسهيل عملية تقديم ومتابعة البلاغات بدقة عالية.
    
    **استخدم القائمة الجانبية للتنقل:**
    * **إرسال بلاغ**: لتقديم بلاغ جديد وتحديده بدقة.
    * **لوحة الإحصائيات**: لمتابعة توزيع البلاغات وعرض السجل.
    """)

# 2. صفحة إرسال البلاغ
elif menu == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    
    # اختيار القسم يدوياً (لضمان عدم الخطأ في التصنيف)
    selected_cat = st.selectbox("حدد القسم بدقة:", options=category_options)
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:", height=150)
    
    if st.button("🚀 إرسال البلاغ"):
        if user_input.strip():
            # إضافة البلاغ للذاكرة
            new_data = pd.DataFrame({'القسم': [selected_cat], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_data], ignore_index=True)
            st.success(f"✅ تم حفظ البلاغ بنجاح تحت قسم: **{selected_cat}**")
        else:
            st.warning("يرجى كتابة تفاصيل البلاغ أولاً.")

# 3. صفحة الإحصائيات
elif menu == "لوحة الإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء")
    
    if not st.session_state.reports.empty:
        # حساب الإحصائيات
        stats = st.session_state.reports['القسم'].value_counts().reset_index()
        stats.columns = ['القسم', 'count']
        
        # الرسم البياني
        fig = px.pie(stats, values='count', names='القسم', title="توزيع البلاغات")
        st.plotly_chart(fig, use_container_width=True)
        
        # جدول البيانات
        st.subheader("سجل البلاغات المسجلة:")
        st.dataframe(st.session_state.reports, use_container_width=True)
    else:
        st.info("لا توجد بلاغات مسجلة حالياً.")
