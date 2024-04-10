import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd

##import data
df_prompts = pd.read_csv("llm_responses_sample.csv")
df_prompts.rename(columns={"first_question":"question","answer_removed_duplicates":"answer"}, inplace = True)

##start survey
survey = ss.StreamlitSurvey("Survey Aligniverse")

pages = survey.pages(5, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
with pages:
    if pages.current == 0:
        st.title("Welcome at Aligniverse!")
        st.write("Our mission involves collecting data to align Large Language Models (LLMs) in a way that fosters positivity and reduces discrimination, particularly towards minority groups.")
        page1_q1 = survey.radio("Do you want to participate in our study?", options=["Yes", "No"], horizontal=True, id="Q1")

    if pages.current == 1:
        st.title("You at Aligniverse!")
        st.write("Your ratings will contribute to the development of an open-source dataset, which AI practitioners can utilize to align their LLMs. For the creation of this dataset, it's important for us to gather some information about you to determine the specific demographic group you represent. Our goal is to collect as little information as possible in order to prioritize your privacy.")
        
        page2_q1 = survey.selectbox("Gender:", options=["I identify as non-binary", "I identify as female", "I identify as male", "I wish not to declare"])

    if pages.current == 2:
        st.title("Type of discrimination!")
        st.write("Choose the type of discrimination you want to focus on")
        page3_q1 = survey.selectbox("Discrimination type:", options=["Gender identity", "Ethnicity", "LGBTQ+"])

    if pages.current == 3:
        st.title("Rate pre-defined LLM responses")
        sample_row = df_prompts.sample(1)

        st.subheader("Prompt")
        st.write(sample_row["question"].values[0])

        st.subheader("Answer")
        st.write(sample_row["answer"].values[0])
        
        st.subheader("Rate the displayed answer")

        st.write("The answer is not discriminating")
        survey.radio("Discrimination:", options=["strongly agree", "agree", "neutral", "disagree", "strongly disagree"], horizontal=True)
        
        st.write("The answer is encouraging")
        survey.radio("Encouragement:", options=["strongly agree", "agree", "neutral", "disagree", "strongly disagree"], horizontal=True)
        
    if pages.current == 4:
        st.title("Thank you!")
        st.balloons()


results = survey.to_json()

file_path = "results.json"
with open(file_path, 'w') as f:
    json.dump(results, f)
            
        