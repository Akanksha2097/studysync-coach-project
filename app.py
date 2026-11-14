"""
StudySync -- a small study-session app.

Ships complete from Week 2. Each tinker below is a real ticket against this
running app: a scoped, working feature with one part that isn't finished yet.

Run with: streamlit run app.py
"""

import streamlit as st

from scoring import render_session_scorer_tab
from sessions import render_session_log_tab
from ranking import render_study_spot_tab
from coach.rag import answer_question

st.set_page_config(page_title="StudySync Coach", page_icon="📚", layout="wide")
st.title("📚 StudySync Coach")
st.caption("Plan a study session with transparent retrieval, ranked study spots, and reliability guardrails.")

tab1, tab2, tab3, tab4 = st.tabs(["AI Study Coach", "Session Scorer", "Session Log", "Find a Study Spot"])

with tab1:
    st.subheader("Ask the local study coach")
    st.write("The coach retrieves evidence from the committed study guide before writing its recommendation.")
    question = st.text_area("What do you want help planning?", placeholder="How can I remember what I read?", max_chars=500)
    if st.button("Ask coach", type="primary"):
        response = answer_question(question)
        st.info(response.answer)
        col1, col2 = st.columns(2)
        col1.metric("Confidence", f"{response.confidence:.0%}")
        col2.write("**Retrieved sources**\n" + ("\n".join(f"- {source}" for source in response.sources) if response.sources else "- None"))
        if response.guardrail:
            st.warning(f"Guardrail: {response.guardrail}")

with tab2:
    render_session_scorer_tab()

with tab3:
    render_session_log_tab()

with tab4:
    render_study_spot_tab()
