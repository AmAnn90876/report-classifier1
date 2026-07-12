import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GHARS - منصة بلاغات", layout="wide")

if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# القاموس الذي حددته
category_map = {
    0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق",
    4: "الصيانة", 5: "الطرق", 6: "المرور", 7: "النظافة",
    8: "تشوه بصري", 9: "تصريف الأمطار", 10: "حدائق",
    11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"
}

# دالة تصنيف حازمة
def strict_classify(text):
    text = text.lower()
    
    # ربط الكلمات المفتاحية الدقيقة بكل تصنيف
    rules = {
        "إنارة": ["إنارة", "نور", "إضاءة", "لمبة"],
        "الإنارة": ["إنارة", "نور", "إضاءة", "لمبة"],
        "التشوه البصري": ["تشوه", "بصري", "جدار"],
        "تشوه بصري": ["تشوه", "بصري"],
        "الحدائق": ["حديقة", "حدائق", "شجر"],
        "حدائق": ["حديقة", "حدائق"],
        "الصيانة": ["صيانة", "عطل", "إصلاح"],
        "الطرق": ["طريق", "طرق", "أسفلت", "حفرة", "رصيف"],
        "طرق": ["طريق", "طرق"],
        "المرور": ["مرور", "ازدحام", "سيارات"],
        "النظافة": ["نظافة", "زبالة", "نفايات", "قمامة"],
        "نظافة": ["نظافة", "قمامة"],
        "تصريف الأمطار": ["مياه", "أمطار", "تصريف", "سيول"],
        "حفريات": ["حفرية", "حفريات"],
        "مبانٍ قابلة للسقوط": ["مبنى", "سقوط", "تصدع", "آيل"]
    }
    
    for label, keywords in rules.items():
        if any(keyword in text for keyword in keywords):
            return label
            
    return "غير محدد" # هنا لن يذهب للصيانة، سيقول غير محدد

page = st.sidebar.radio("التنقل", ["إرسال بلاغ", "لوحة الإحصائيات"])

if page == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:")
    
    if st.button("🚀 تصنيف"):
        if user_input.strip():
            cat = strict_classify(user_input)
            
            if cat == "غير محدد":
                st.warning("لم يتمكن النظام من تصنيف البلاغ تلقائياً. يرجى اختيار القسم يدوياً:")
                cat = st.selectbox("اختر القسم الصحيح:", list(category_map.values()))
            
            new_data = pd.DataFrame({'القسم': [cat], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_data], ignore_index=True)
            st.success(f"✅ تم حفظ البلاغ تحت قسم: **{cat}**")
        else:
            st.error("يرجى كتابة البلاغ.")

elif page == "لوحة الإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء")
    if not st.session_state.reports.empty:
        stats = st.session_state.reports['القسم'].value_counts().reset_index()
        stats.columns = ['القسم', 'count']
        st.plotly_chart(px.pie(stats, values='count', names='القسم'))
    else:
        st.info("لا توجد بلاغات.")
