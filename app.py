import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# إعداد الصفحة
st.set_page_config(page_title="GHARS - منصة تصنيف البلاغات", layout="wide")

# 1. ذاكرة التطبيق
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# 2. دالة تصنيف ذكية ومحدثة
def get_prediction(text):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import Pipeline
    
    # القاموس الاحترافي الخاص بكِ
    category_map = {
        0: "إنارة", 1: "الإنارة", 2: "التشوه البصري", 3: "الحدائق", 4: "الصيانة",
        5: "الطرق", 6: "المرور", 7: "النظافة", 8: "تشوه بصري", 9: "تصريف الأمطار",
        10: "حدائق", 11: "حفريات", 12: "طرق", 13: "مبانٍ قابلة للسقوط", 14: "نظافة"
    }
    
    # بيانات تدريب موسعة تغطي جميع الأقسام الـ 15 ليكون النظام ذكياً
    X = [
        "لمبة عمود نور", "إضاءة الشوارع", "جدار مشوه كتابات", "حديقة عامة أزهار", "صيانة مرافق عامة",
        "طريق متضرر", "ازدحام مروري", "نفايات زبالة", "منظر غير حضاري", "سيول تصريف أمطار",
        "مسطحات خضراء حدائق", "حفريات شركة المياه", "تعبيد طرق أسفلت", "سقوط مبنى قديم", "تراكم مخلفات"
    ]
    y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    
    model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
    model.fit(X, y)
    
    # التنبؤ
    pred_index = model.predict([text])[0]
    return category_map.get(pred_index, "غير مصنف")

# 3. واجهة المستخدم
st.title("🛡️ منصة تصنيف البلاغات الذكية")

selected = option_menu(
    menu_title=None, 
    options=["إرسال بلاغ", "لوحة الإحصائيات"], 
    icons=['pencil', 'bar-chart'], 
    orientation="horizontal"
)

if selected == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:", height=150, placeholder="مثال: يوجد مبنى قديم يمثل خطر...")
    
    if st.button("🚀 تصنيف وإرسال"):
        if user_input.strip():
            with st.spinner('جاري تحليل البلاغ بذكاء...'):
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
        stats = st.session_state.reports['القسم'].value_counts().reset_index()
        stats.columns = ['القسم', 'العدد']
        
        # عرض الرسم البياني
        fig = px.pie(stats, values='العدد', names='القسم', title="توزيع البلاغات حسب الأقسام")
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض الجدول
        st.dataframe(st.session_state.reports, use_container_width=True)
    else:
        st.info("لا توجد بلاغات حالياً.")
