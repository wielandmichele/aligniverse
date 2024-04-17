import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd

df_prompts = pd.read_csv("llm_responses_sample.csv")
df_prompts.rename(columns={"first_question":"question","answer_removed_duplicates":"answer"}, inplace = True)

##start survey
survey = ss.StreamlitSurvey("craft_survey")

q1 = survey.multiselect("Choose the type of discrimination you want to focus on", options=["Gender identity", "Ethnicity", "LGBTQ+"], id = "craft_type")
##todo: add filter for gender discrimination based on this information

##todo: either ask how many answers a user wants to write or set very high
with survey.pages(3) as page:
    sample_row = df_prompts.sample(1)

    st.subheader("Prompt")
    st.write(sample_row["question"].values[0])
    a1 = survey.text_input("Your answer", id = f"answer_{page.current}")

st.write("If you would like to rate pre-defined responses as well, you can return to the overview.")
if st.button("Back to overview"):
    st.switch_page("pages/01_Overview.py")

st.write("You can craft as many answers as you like. When you are finished, you can end your participation.")
if st.button("End participation"):
    st.title("Thank you for participating!")
    st.balloons()