# app.py
# Streamlit UI for LangChain CSV School Analytics Agent
# Run:
#   pip install streamlit langchain langchain-experimental langchain-openai pandas
#   streamlit run app.py

import streamlit as st
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
import time

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="🎓 AI School Analytics",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------------------
# Custom Styling
# ---------------------------------------------------

st.markdown("""
<style>
.main {
    background: linear-gradient(180deg, #f7f9ff 0%, #eef4ff 100%);
}

.big-title {
    font-size: 3rem;
    font-weight: 800;
    color: #4F46E5;
    text-align: center;
    margin-bottom: 0.3rem;
}

.subtitle {
    font-size: 1.2rem;
    text-align: center;
    color: #475569;
    margin-bottom: 2rem;
}

.question-box {
    background-color: white;
    padding: 1rem;
    border-radius: 18px;
    border: 2px solid #dbeafe;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
}

.answer-card {
    background: white;
    padding: 1.5rem;
    border-radius: 20px;
    border-left: 8px solid #6366F1;
    box-shadow: 0px 8px 18px rgba(0,0,0,0.08);
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    font-size: 1rem;
    font-weight: 700;
    background-color: #4F46E5;
    color: white;
    border: none;
}

.stButton>button:hover {
    background-color: #4338CA;
    color: white;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.markdown(
    '<div class="big-title">🎓 AI School Analytics Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about students, marks, toppers, and subjects using AI 🚀</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
        width=140
    )

    st.header("📘 About")

    st.write("""
This app uses:

✅ Streamlit UI  
✅ LangChain CSV Agent  
✅ Ollama Local LLM  
✅ AI-powered data analysis
""")

    st.header("💡 Example Questions")

    examples = [
        "Who is the topper of the class?",
        "What are the top marks in Math?",
        "Which student scored highest in Science?",
        "Show average marks per subject",
        "List top marks of every subject with student names"
    ]

    for ex in examples:
        st.info(ex)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

@st.cache_data
def load_data():
    students = pd.read_csv("students.csv")
    subjects = pd.read_csv("subjects.csv")
    marks = pd.read_csv("marks.csv")
    return students, subjects, marks

students_df, subjects_df, marks_df = load_data()

# ---------------------------------------------------
# Quick Stats
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h2>👨‍🎓 {len(students_df)}</h2>
        <p>Total Students</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h2>📚 {len(subjects_df)}</h2>
        <p>Total Subjects</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h2>📝 {len(marks_df)}</h2>
        <p>Total Marks Entries</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------------------------------------------
# Create Agent
# ---------------------------------------------------

@st.cache_resource
def create_agent():

    llm = ChatOpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
        model='qwen2.5-coder',
        temperature=0
    )

    agent = create_csv_agent(
        llm,
        ["students.csv", "subjects.csv", "marks.csv"],
        verbose=True,
        agent_type="openai-tools",
        allow_dangerous_code=True,
        agent_executor_kwargs={
            "handle_parsing_errors": True
        }
    )

    return agent

agent = create_agent()

# ---------------------------------------------------
# Main Chat Area
# ---------------------------------------------------

st.markdown("## 🤖 Ask Your Question")

question = st.text_input(
    "",
    placeholder="Example: Who is the topper of the class?"
)

# ---------------------------------------------------
# Suggested Question Buttons
# ---------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    topper_btn = st.button("🏆 Find Class Topper")

with c2:
    math_btn = st.button("📐 Best Math Score")

with c3:
    avg_btn = st.button("📊 Subject Averages")

if topper_btn:
    question = "Who is the topper of the class?"

if math_btn:
    question = "What are the top marks in Math?"

if avg_btn:
    question = "Show average marks per subject"

# ---------------------------------------------------
# Run Query
# ---------------------------------------------------

if question:

    with st.spinner("🧠 AI is analyzing the school data..."):

        start = time.time()

        try:
            response = agent.invoke({"input": question})
            answer = response["output"]

            elapsed = round(time.time() - start, 2)

            st.markdown(
                f"""
                <div class="answer-card">
                    <h2>✨ AI Answer</h2>
                    <p style="font-size:1.2rem;">
                        {answer}
                    </p>
                    <hr>
                    <p>⏱️ Generated in {elapsed} seconds</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.balloons()

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------------------------------------------------
# Data Preview Section
# ---------------------------------------------------

with st.expander("📂 Preview CSV Data"):

    tab1, tab2, tab3 = st.tabs(
        ["👨‍🎓 Students", "📚 Subjects", "📝 Marks"]
    )

    with tab1:
        st.dataframe(students_df, use_container_width=True)

    with tab2:
        st.dataframe(subjects_df, use_container_width=True)

    with tab3:
        st.dataframe(marks_df, use_container_width=True)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.write("")
st.write("")

st.markdown("""
<div style='text-align:center; color:gray; padding:20px;'>
Built with ❤️ using Streamlit + LangChain + Ollama
</div>
""", unsafe_allow_html=True)