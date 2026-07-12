import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px

# 1. ذاكرة التطبيق
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# 2. دالة تصنيف ذكية (تحميل النموذج عند الطلب فقط - هذا يمنع الانهيار)
def get_prediction(text):
    # نستدعي المكتبات هنا فقط (Lazy Loading)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import Pipeline
    
    training_data = [
        ("نفايات متراكمة حاويات زبالة روائح مخلفات تنظيف", "نظافة"),
        ("تسرب مياه كسر ماسورة انفجار تجمع مياه طفح", "مياه"),
        ("الإنارة معطلة الشارع مظلم عمود النور طافي ظلام", "إنارة"),
        ("حفرة طريق هبوط أسفلت تشققات رصيف مطبات", "طرق")
    ]
    df = pd.DataFrame(training_data, columns=['text', 'label'])
    model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
    model.fit(df['text'], df['label'])
    return model.predict([text])[0]

# 3. القائمة
selected = option_menu(None, ["إرسال بلاغ", "لوحة الإحصائيات"], icons=['pencil', 'bar-chart'], orientation="horizontal")

if selected == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    user_input = st.text_area("تفاصيل البلاغ:", height=100)
    if st.button("🚀 تصنيف وإرسال"):
        if user_input:
            # هنا يتم التصنيف
            pred = get_prediction(user_input)
            new_report = pd.DataFrame({'القسم': [pred], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_report], ignore_index=True)
            st.success(f"تم تصنيف البلاغ كـ: {pred}")
        else:
            st.warning("يرجى كتابة نص البلاغ")
# ... بقية الكود الخاص بالإحصائيات (نفس كودك وهو صحيح 100%)
