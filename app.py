import streamlit as st
import streamlit_survey as ss

st.title("Welcome at Aligniverse!")
st.write("Our mission involves collecting data to align Large Language Models (LLMs) in a way that fosters positivity and reduces discrimination, particularly towards minority groups.")

survey = ss.StreamlitSurvey("Survey 1")
Q1 = survey.radio("Do you want to participate in our study?:", options=["NA", "👍", "👎"], horizontal=True, id="Q1")
if Q1 == "👍":
    Q1_1 = survey.text_input("Why did you select '👍'?", id="Q1_1")