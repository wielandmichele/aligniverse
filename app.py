import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd

#load data
df_countries = pd.read_csv("UNSD_Methodology_ancestry.csv", sep = ";")

##set config
st.set_page_config(initial_sidebar_state="collapsed")

##start survey
survey = ss.StreamlitSurvey("Survey Aligniverse")

st.title("Welcome at Aligniverse")
st.write("Our mission involves collecting data to align Large Language Models (LLMs) in a way that fosters positivity and reduces discrimination, particularly towards minority groups.")
st.write("In light of this, we're curious about your opinion. How do you envision an LLM responding to sensitive questions? Your participation in our study would be fantastic.")
st.write("It takes 10 minutes to participate by rating one question. If you wish, you can rate as many sets as you like. Of course, we would greatly appreciate your willingness to do so.")
q1 = survey.radio("Do you want to participate in our study?", options=["Yes", "No"], horizontal=True, id="P1_Q1", index = None)

st.divider()

if q1 == "No":
    st.write("We wish you a happy day!")

elif q1 == "Yes":
    st.title("You at Aligniverse")
    st.write("Your ratings will contribute to the development of an open-source dataset, which AI practitioners can utilize to align their LLMs. For the creation of this dataset, it's important for us to gather some information about you to determine the specific demographic group you represent. Our goal is to collect as little information as possible in order to prioritize your privacy.")

    age_groups = ["<18", "18-30", "31-40", "41-50","51-60", "60<", "I wish not to declare"]
    pronouns = [
        "she/her/hers",
        "he/him/his",
        "they/them/theirs",
        "ze/hir/hirs",
        "xe/xem/xyrs",
        "ey/em/eirs",
        "ve/ver/vis",
        "per/pers/perself",
        "I wish not to declare"
    ]
    racial_groups = [
        "American Indian or Alaska Native",
        "Asian",
        "Black or African American",
        "Hispanic or Latino",
        "Middle Eastern or North African",
        "Native Hawaiian or Pacific Islander",
        "White",
        "I wish not to declare"
    ]

    list_countries = sorted(df_countries["Country or Area"].to_list())
    list_countries.insert(0, "I wish not to declare")

    page2_q1 = survey.selectbox("Which age group do you belong to?", options=age_groups, id="P2_Q1", index=None)
    page2_q2 = survey.selectbox("What pronouns do you use to identify yourself?", options=pronouns, id="P2_Q2", index=None)
    page2_q3 = survey.multiselect("Which is your country of residence?", options=list_countries, id="P2_Q3")
    page2_q4 = survey.multiselect("Where do your ancestors (e.g., great-grandparents) come from?", options=list_countries, id="P2_Q4")
    page2_q5 = survey.multiselect("Which racial group(s) do you identify with?", options=racial_groups, id="P2_Q5")

    if not all([page2_q1, page2_q2, page2_q3, page2_q4, page2_q5]):
        st.write("Please select one option for every question. You always have the option not to declare.")
    
    elif all([page2_q1, page2_q2, page2_q3, page2_q4, page2_q5]):
        if st.button("Let's create a better dataset!"):
            st.switch_page("pages/01_Overview.py")
        