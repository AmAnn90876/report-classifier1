import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from streamlit_option_menu import option_menu
import plotly.express as px
@st.cache_resource
def train_model():

    data = pd.read_excel("Reports_Dataset.xlsx")

    X = data["complaint"]
    y = data["category"]

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1,2)
            )
        ),
        (
            "svm",
            LinearSVC()
        )
    ])

    model.fit(X, y)

    return model


model = train_model()
st.set_page_config(
    page_title="نظام تصنيف البلاغات الذكي",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.stApp{
background-color:#F4F6F8;
}

.block-container{
max-width:1100px;
padding-top:1.5rem;
padding-bottom:2rem;
}

html, body, [class*="css"]{
font-family: "Segoe UI", sans-serif;
}

.hero{
background:#006C35;
padding:35px;
border-radius:18px;
color:white;
text-align:center;
margin-bottom:30px;
}

.hero h1{
margin:0;
font-size:36px;
}

.hero p{
margin-top:10px;
font-size:18px;
opacity:.95;
}

.section{
background:white;
padding:25px;
border-radius:15px;
box-shadow:0 4px 15px rgba(0,0,0,.08);
margin-bottom:20px;
}

.stTextArea textarea{
border-radius:12px;
font-size:16px;
}

.stButton>button{
width:100%;
height:52px;
border:none;
border-radius:10px;
background:#006C35;
color:white;
font-size:18px;
font-weight:bold;
transition:.3s;
}

.stButton>button:hover{
background:#0B7A43;
}

.result{
background:#EEF8F2;
padding:20px;
border-right:6px solid #006C35;
border-radius:12px;
font-size:20px;
margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<h1>🏛️ نظام تصنيف البلاغات الذكي</h1>

<p>
تحليل البلاغات البلدية وتصنيفها تلقائياً باستخدام الذكاء الاصطناعي
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">

<h3>📝 تفاصيل البلاغ</h3>

</div>
""", unsafe_allow_html=True)


complaint_text = st.text_area(
    "اكتب وصف البلاغ هنا:",
    placeholder="مثال: يوجد حفريات في الشارع الرئيسي تسبب خطراً على المارة...",
    height=150
)


st.markdown("""
<div class="section">

<h3>📷 صورة البلاغ (اختياري)</h3>

</div>
""", unsafe_allow_html=True)


uploaded_image = st.file_uploader(
    "ارفع صورة توضح المشكلة:",
    type=["png", "jpg", "jpeg"]
)


st.markdown("""
<div class="section">

<h3>📍 موقع البلاغ (اختياري)</h3>

</div>
""", unsafe_allow_html=True)


location = st.text_input(
    "أدخل موقع البلاغ:",
    placeholder="مثال: حي السلام، شارع الملك عبدالعزيز"
)


st.markdown("<br>", unsafe_allow_html=True)


analyze_button = st.button(
    "🚀 تحليل البلاغ"
)

if analyze_button:

    if complaint_text.strip() == "":
        st.warning("⚠️ الرجاء كتابة وصف البلاغ أولاً.")

    else:

        prediction = model.predict([complaint_text])[0]

        st.markdown(f"""
        <div class="result">

        ✅ نوع البلاغ المتوقع:
        <br><br>

        <b>{prediction}</b>

        </div>
        """, unsafe_allow_html=True)


        if uploaded_image is not None:

            st.markdown("""
            <div class="section">

            <h3>📷 الصورة المرفوعة</h3>

            </div>
            """, unsafe_allow_html=True)

            st.image(
                uploaded_image,
                width=400
            )


        if location.strip() != "":

            st.markdown(f"""
            <div class="section">

            📍 موقع البلاغ:
            <br><br>

            <b>{location}</b>

            </div>
            """, unsafe_allow_html=True)
st.markdown("""
<div class="section">

<h3>📊 إحصائيات البلاغات</h3>

</div>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():

    return pd.read_excel("Reports_Dataset.xlsx")


df = load_data()


category_count = (
    df["category"]
    .value_counts()
    .reset_index()
)

category_count.columns = [
    "Category",
    "Count"
]


fig = px.bar(
    category_count,
    x="Category",
    y="Count",
    text="Count",
    title="عدد البلاغات حسب التصنيف"
)


st.plotly_chart(
    fig,
    use_container_width=True
)

priority_map = {
    "حفريات": "عالية",
    "مبانٍ آيلة للسقوط": "عالية",
    "إنارة": "متوسطة",
    "طرق": "متوسطة",
    "نظافة": "متوسطة",
    "تشوه بصري": "منخفضة",
    "حدائق": "منخفضة"
}


department_map = {
    "حفريات": "إدارة الطرق",
    "مبانٍ آيلة للسقوط": "قسم السلامة",
    "إنارة": "إدارة الإنارة",
    "طرق": "إدارة الطرق",
    "نظافة": "إدارة النظافة",
    "تشوه بصري": "قسم الرقابة",
    "حدائق": "إدارة الحدائق"
}


if analyze_button and complaint_text.strip():

    prediction = model.predict([complaint_text])[0]

    priority = priority_map.get(
        prediction,
        "غير محددة"
    )

    department = department_map.get(
        prediction,
        "غير محدد"
    )


    st.markdown(f"""
    <div class="result">

    ✅ تصنيف البلاغ:
    <br>
    <b>{prediction}</b>

    <br><br>

    ⚡ الأولوية:
    <br>
    <b>{priority}</b>

    <br><br>

    🏢 الجهة المسؤولة:
    <br>
    <b>{department}</b>

    </div>
    """, unsafe_allow_html=True)

