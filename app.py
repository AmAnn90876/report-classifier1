import streamlit as st
import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix

# إعداد الصفحة
st.set_page_config(page_title="نظام تصنيف البلاغات", layout="wide")
st.title("📊 واجهة تصنيف البلاغات البلدية/العامة")

# --- 1. تحميل النماذج (تُحمل مرة واحدة فقط) ---
@st.cache_resource
def load_models():
    # تأكدي أن هذه الملفات مرفوعة فعلياً في GitHub
    model = joblib.load("SVM_Model.pkl")
    vectorizer = joblib.load("TFIDF_Vectorizer.pkl")
    label_encoder = joblib.load("Label_Encoder.pkl")
    return model, vectorizer, label_encoder

try:
    model, vectorizer, label_encoder = load_models()
except:
    st.error("❌ لم يتم العثور على ملفات النموذج. تأكد من وجود SVM_Model.pkl و TFIDF_Vectorizer.pkl و Label_Encoder.pkl في نفس المجلد.")
    st.stop()

# --- 2. دوال معالجة النصوص (نفس المستخدمة في التدريب) ---
nltk.download('stopwords', quiet=True)
arabic_stopwords = set(stopwords.words('arabic'))

def preprocess_text(text):
    if not isinstance(text, str): return ""
    # 1. إزالة التشكيل
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    # 2. إزالة علامات الترقيم
    text = re.sub(r'[^\w\s]', ' ', text)
    # 3. إزالة الأرقام
    text = re.sub(r'[\d\u0660-\u0669]+', '', text)
    # 4. توحيد الحروف
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'ة\b', 'ه', text)
    text = re.sub(r'ى\b', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # 5. إزالة كلمات التوقف
    words = text.split()
    filtered_words = [word for word in words if word not in arabic_stopwords]
    return ' '.join(filtered_words)

# --- 3. القائمة الجانبية للتنقل ---
st.sidebar.title("القائمة الرئيسية")
app_mode = st.sidebar.radio("اختر الصفحة:", ["📝 تصنيف بلاغ جديد", "📈 لوحة الإحصائيات وقياس الدقة"])

# ==========================================
# الصفحة الأولى: تصنيف بلاغ جديد تلقائياً
# ==========================================
if app_mode == "📝 تصنيف بلاغ جديد":
    st.header("تصنيف البلاغات تلقائياً")
    user_input = st.text_area("أدخل نص البلاغ هنا:", height=150)
    
    if st.button("تصنيف البلاغ"):
        if user_input.strip() == "":
            st.warning("الرجاء إدخال نص البلاغ أولاً.")
        else:
            with st.spinner("جاري تحليل البلاغ..."):
                cleaned_text = preprocess_text(user_input)
                vectorized_text = vectorizer.transform([cleaned_text])
                prediction = model.predict(vectorized_text)
                category = label_encoder.inverse_transform(prediction)[0]
                
                st.success(f"✅ **التصنيف المتوقع:** {category}")

# ==========================================
# الصفحة الثانية: لوحة إحصائية وقياس الدقة
# ==========================================
elif app_mode == "📈 لوحة الإحصائيات وقياس الدقة":
    st.header("لوحة إحصائية لنتائج التصنيف وقياس الدقة")
    st.write("قم برفع ملف البلاغات (Excel/CSV) لاختبار النموذج وعرض الإحصائيات.")
    
    uploaded_file = st.file_uploader("رفع ملف البيانات", type=["xlsx", "csv"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df_test = pd.read_csv(uploaded_file)
        else:
            df_test = pd.read_excel(uploaded_file)
            
        st.write("عينة من البيانات المرفوعة:")
        st.dataframe(df_test.head())
        
        if "complaint" in df_test.columns and "category" in df_test.columns:
            with st.spinner("جاري معالجة البيانات وتقييم النموذج..."):
                df_test['cleaned'] = df_test['complaint'].apply(preprocess_text)
                X_test = vectorizer.transform(df_test['cleaned'])
                y_pred = model.predict(X_test)
                
                y_true = label_encoder.transform(df_test['category'].str.strip())
                df_test['Predicted_Category'] = label_encoder.inverse_transform(y_pred)
                
                accuracy = accuracy_score(y_true, y_pred)
                st.subheader(f"🎯 نسبة الدقة (Accuracy): {accuracy * 100:.2f}%")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("توزيع البلاغات حسب التصنيف (التنبؤات)")
                    fig, ax = plt.subplots()
                    df_test['Predicted_Category'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
                    ax.set_ylabel("عدد البلاغات")
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("مصفوفة الارتباك (Confusion Matrix)")
                    cm = confusion_matrix(y_true, y_pred)
                    fig2, ax2 = plt.subplots()
                    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                                xticklabels=label_encoder.classes_, 
                                yticklabels=label_encoder.classes_, ax=ax2)
                    st.pyplot(fig2)
                    
                st.subheader("البيانات بعد التصنيف")
                st.dataframe(df_test[['complaint', 'category', 'Predicted_Category']])
                
        else:
            st.error("الملف المرفوع يجب أن يحتوي على عمودين باسم 'complaint' و 'category'.")
