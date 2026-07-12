import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="منصة البلاغات", layout="centered")

# تهيئة الذاكرة
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(columns=['القسم', 'التفاصيل'])

# القائمة الجانبية للتنقل
menu = st.sidebar.radio("القائمة", ["الرئيسية", "إرسال بلاغ"])

if menu == "الرئيسية":
    st.title("🛡️ منصة البلاغات")
    st.markdown("---")
    st.write("أهلاً بك في نظام إدارة البلاغات.")
    st.write("استخدم القائمة الجانبية لإرسال بلاغ جديد.")

elif menu == "إرسال بلاغ":
    st.header("📋 تقديم بلاغ جديد")
    
    # حقل حر لكتابة القسم وتفاصيل البلاغ
    user_category = st.text_input("أدخلي اسم القسم:")
    user_input = st.text_area("أدخلي تفاصيل البلاغ هنا:", height=150)
    
    if st.button("🚀 إرسال البلاغ"):
        if user_category.strip() and user_input.strip():
            # إضافة البلاغ للذاكرة
            new_row = pd.DataFrame({'القسم': [user_category], 'التفاصيل': [user_input]})
            st.session_state.reports = pd.concat([st.session_state.reports, new_row], ignore_index=True)
            st.success(f"✅ تم حفظ البلاغ في قسم: **{user_category}**")
        else:
            st.warning("يرجى تعبئة اسم القسم وتفاصيل البلاغ.")
