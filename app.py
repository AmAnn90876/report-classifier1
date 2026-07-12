import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from streamlit_option_menu import option_menu
import plotly.express as px

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
background:#F5F7F8;
}

.block-container{
padding-top:1rem;
padding-bottom:1rem;
max-width:1200px;
}

.hero{
background:linear-gradient(90deg,#006C35,#008C4A);
padding:30px;
border-radius:18px;
color:white;
text-align:center;
margin-bottom:25px;
box-shadow:0px 8px 20px rgba(0,0,0,.15);
}

.hero h1{
font-size:40px;
margin-bottom:8px;
}

.hero p{
font-size:18px;
opacity:.95;
}

.card{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0 5px 20px rgba(0,0,0,.08);
margin-bottom:20px;
}

.stButton>button{
background:#006C35;
color:white;
border:none;
border-radius:10px;
height:52px;
font-size:18px;
font-weight:bold;
width:100%;
transition:.3s;
}

.stButton>button:hover{
background:#008C4A;
transform:scale(1.02);
}

textarea{
border-radius:12px !important;
}

.metric-card{
background:white;
padding:18px;
border-radius:15px;
text-align:center;
box-shadow:0 5px 15px rgba(0,0,0,.08);
}

.result{
background:#EAF7EF;
border-right:8px solid #006C35;
padding:20px;
border-radius:15px;
font-size:22px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<h1>🏛️ وزارة البلديات والإسكان</h1>

<h2>نظام تصنيف البلاغات الذكي</h2>

<p>
يقوم النظام بتحليل البلاغات وتصنيفها تلقائياً باستخدام الذكاء الاصطناعي
</p>

</div>
""", unsafe_allow_html=True)

if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame(
        columns=['القسم','التفاصيل']
    )

training_data = [
("نفايات متراكمة حاويات زبالة روائح مخلفات تنظيف","نظافة"),
("تسرب مياه كسر ماسورة انفجار تجمع مياه طفح","مياه"),
("الإنارة معطلة الشارع مظلم عمود النور طافي ظلام","إنارة"),
("حفرة طريق هبوط أسفلت تشققات رصيف مطبات","طرق")
]

df = pd.DataFrame(training_data,columns=['text','label'])

model = Pipeline([
('tfidf',TfidfVectorizer()),
('clf',LinearSVC())
])

model.fit(df['text'],df['label'])

selected = option_menu(
    None,
    ["📝 إرسال بلاغ", "📊 لوحة الإحصائيات"],
    icons=["clipboard2-check", "bar-chart-fill"],
    orientation="horizontal",
    default_index=0,
)

if selected == "📝 إرسال بلاغ":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📝 تقديم بلاغ جديد")

    st.write("يرجى كتابة تفاصيل البلاغ وسيقوم النظام بتحليله وتصنيفه تلقائياً.")

    user_input = st.text_area(
        "",
        height=180,
        placeholder="مثال: يوجد حفرة كبيرة في شارع الملك عبدالله تسبب خطراً على المركبات..."
    )

    if st.button("🚀 تحليل البلاغ"):

        if user_input.strip() == "":
            st.warning("⚠️ يرجى كتابة تفاصيل البلاغ أولاً.")

        else:

            with st.spinner("جاري تحليل البلاغ بواسطة الذكاء الاصطناعي..."):

                pred = model.predict([user_input])[0]

                new_report = pd.DataFrame(
                    {
                        "القسم":[pred],
                        "التفاصيل":[user_input]
                    }
                )

                st.session_state.reports = pd.concat(
                    [st.session_state.reports,new_report],
                    ignore_index=True
                )

            st.markdown(
                f"""
                <div class="result">

                ✅ تم استلام البلاغ بنجاح

                <br><br>

                📂 <b>التصنيف المتوقع:</b> {pred}

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "📊 لوحة الإحصائيات":

    st.subheader("📊 لوحة مؤشرات الأداء")

    if not st.session_state.reports.empty:

        stats = (
            st.session_state.reports["القسم"]
            .value_counts()
            .reset_index()
        )

        stats.columns = ["القسم","العدد"]

        total_reports = len(st.session_state.reports)

        most_category = stats.iloc[0]["القسم"]

        categories = len(stats)

        c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(
                "📋 إجمالي البلاغات",
                total_reports
            )

        with c2:
            st.metric(
                "🏛️ أكثر تصنيف",
                most_category
            )

        with c3:
            st.metric(
                "📂 عدد الأقسام",
                categories
            )

        st.divider()

        fig = px.bar(
            stats,
            x="القسم",
            y="العدد",
            color="القسم",
            text="العدد",
            height=450
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False,
            title="توزيع البلاغات حسب القسم",
            title_x=0.5
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("📄 سجل البلاغات")

        st.dataframe(
            st.session_state.reports,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "لا توجد بلاغات حتى الآن."
        )
