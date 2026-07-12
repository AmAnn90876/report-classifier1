import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="GHARS - منصة ذكية", layout="wide")

# 1. ذاكرة التطبيق
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# 2. محرك التصنيف الذكي (بدون مكتبات ثقيلة لتجنب الانهيار)
def smart_classify(text):
    text = text.lower()
    
    # القاموس الذكي للربط بالأقسام
    if any(word in text for word in ['إنارة', 'نور', 'إضاءة', 'لمبة']): return "الإنارة"
    if any(word in text for word in ['تشوه', 'كتابة', 'جدار', 'بصري']): return "التشوه البصري"
    if any(word in text for word in ['حديقة', 'شجر', 'عشب', 'خضراء']): return "الحدائق"
    if any(word in text for word in ['طريق', 'أسفلت', 'حفرة', 'رصيف', 'هبوط']): return "الطرق"
    if any(word in text for word in ['نظافة', 'زبالة', 'نفايات', 'قمامة', 'روائح']): return "النظافة"
    if any(word in text for word in ['مياه', 'أمطار', 'تصريف', 'طفح', 'سيول']): return "تصريف الأمطار"
    if any(word in text for word in ['مبنى', 'سقوط', 'تصدع', 'آيل']): return "مبانٍ قابلة للسقوط"
    if any(word in text for word in ['حفرية', 'حفريات']): return "حفريات"
    if any(word in text for word in ['مرور', 'ازدحام', 'سيارات']): return "المرور"
    
    return "الصيانة" # القسم الافتراضي إذا لم يجد كلمة مفتاحية

# 3. الواجهة
st.title("🛡️نظام التصنيف الذكي")

selected = option_menu(
    menu_title=None, 
    options=["إرسال بلاغ", "لوحة الإحصائيات"], 
    icons=['pencil', 'bar-chart'], 
    orientation="horizontal"
)

if selected == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:", height=150)
    
    if st.button("🚀 تصنيف وإرسال"):
        if user_input.strip():
            with st.spinner('جاري التحليل...'):
                category = smart_classify(user_input)
                new_report = pd.DataFrame({'القسم': [category], 'التفاصيل': [user_input]})
                st.session_state.reports = pd.concat([st.session_state.reports, new_report], ignore_index=True)
                st.success(f"✅ تم تصنيف البلاغ بنجاح إلى: **{category}**")
        else:
            st.warning("يرجى كتابة نص البلاغ أولاً.")

elif selected == "لوحة الإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء")
    if not st.session_state.reports.empty:
        stats = st.session_state.reports['القسم'].value_counts().reset_index()
        stats.columns = ['القسم', 'العدد']
        
        # الرسم البياني
        fig = px.pie(stats, values='العدد', names='القسم', title="توزيع البلاغات")
        st.plotly_chart(fig, use_container_width=True)
        
        # الجدول
        st.dataframe(st.session_state.reports, use_container_width=True)
    else:
        st.info("لا توجد بلاغات حالياً.")
