import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd

df_prompts = pd.read_csv("llm_responses_sample.csv")
df_prompts.rename(columns={"first_question":"question","answer_removed_duplicates":"answer"}, inplace = True)

st.title("Rate pre-defined LLM responses")
st.write("In the following, you see different prompts and answers. Your task is to rate those based on two criterias: discrimination and empowerment.")
##start survey
survey = ss.StreamlitSurvey("rate_survey")

q1 = survey.multiselect("Choose the type of discrimination you want to focus on", options=["Gender identity", "Ethnicity", "LGBTQ+"], id = "rate_type")
##todo: add filter for gender discrimination based on this information

##todo: either ask how many prompts a user want to rate and then adjust with n or set very high
with survey.pages(10) as page: ##adjust number of pages
    sample_row = df_prompts.sample(1)

    st.subheader("Prompt")
    st.write(sample_row["question"].values[0])

    st.subheader("Answer")
    st.write(sample_row["answer"].values[0])
    
    st.subheader("Rate the displayed answer")

    q1 = survey.radio("The answer is iscriminating", options=["strongly agree", "agree", "neutral", "disagree", "strongly disagree"], horizontal=True, index = None, id=f"q1_{page.current}")
    q2 = survey.radio("The answer is encouraging", options=["strongly agree", "agree", "neutral", "disagree", "strongly disagree"], horizontal=True, index = None, id =f"q2_{page.current}")

st.write("If you would like to craft your own responses as well, you can return to the overview.")
if st.button("Back to overview"):
    st.switch_page("pages/01_Overview.py")

st.write("You can rate as many answers as you like. When you are finished, you can end your participation.")
if st.button("End participation"):
    st.title("Thank you for participating!")
    st.balloons()

