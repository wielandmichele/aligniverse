import streamlit as st
import streamlit_survey as ss
import streamlit_scrollable_textbox as stx
import json
import pandas as pd
import time

##set config
st.set_page_config(initial_sidebar_state="collapsed")

##start survey
survey = ss.StreamlitSurvey("Survey Aligniverse")

st.title("Welcome at Aligniverse")
    
text1 = "Hi - great to see you today! Are you wondering what Aligniverse is? Our mission involves collecting data to align Large Language Models (LLMs) in a way that fosters positivity and reduces discrimination, particularly towards minority groups."
st.write(text1)

text2 = "Large Language Models (LLMs) are advanced computer programs designed to understand and generate human-like text based on the data they have been trained on. They can answer questions, write essays, and even engage in conversations. Alignment refers to the process of ensuring that these models behave in a way that is consistent with human values and ethical principles. This means teaching the models to respond in ways that are positive, helpful, and free from bias or discrimination."
st.write(text2)

text3 = "We're curious about your opinion. How do you envision an LLM responding to sensitive questions? Your participation in our study would be fantastic. Throughout the study, you will review different texts created by Large language models (LLMs) that cover sensitive topics. Your task will be to evaluate these texts based on several criteria. We will publish these ratings as an alignment dataset and share it with the community. This dataset can be utilized by practitioners to improve the alignment of LLMs."
st.write(text3)

text4 = "Participating typically takes between 10 and 30 minutes. Rating one pre-generated text is expected to take 10 minutes. You're welcome to rate as many texts as you prefer, and we truly appreciate your willingness to contribute."
st.write(text4)

st.divider()

st.write("We are committed to safeguarding your privacy and making your participation enjoyable. Please review the study terms.")
if st.button("Review general information and consent form"):
    #st.switch_page("pages/Study_terms.py")
    
    content = """Dear participants, we invite you to take part in our research study. You will find all relevant information in the participant information form below. Please review it carefully, and we are available for any questions you may have.
    Our goal is to recruit about 10,000 participants across more than five locations. At the Technical University of Munich (TUM), we intend to recruit around 1,000 participants. The study was planned by TUM and will be carried out in cooperation with Eidgenössiche Technische Hochschule (ETH), with funding from our institute.
    
    Why do we conduct this study?
    Our mission involves collecting data to align Large Language Models (LLMs) in a way that fosters positivity and reduces discrimination, particularly towards minority groups. In light of this, we're curious about your opinion. How do you envision an LLM responding to sensitive questions? 

    Throughout the study, you will review different texts created by large language models (LLMs) that cover sensitive topics. Your task will be to evaluate these texts based on several criteria. We will publish these ratings as an alignment dataset and share it with the community. This dataset can be utilized by practitioners to improve the alignment of LLMs.
    """
    #st.markdown(latex_content)
    stx.scrollableTextbox(content, height = 150)

## include consent questions plus information about contact
consent1 = survey.checkbox("I have read the terms and hereby give my consent to participate in the study.")
consent2 = survey.checkbox("I confirm that I am at least 18 years old.")

if not all([consent1, consent2]):
    st.write("Please give your consent by ticking both boxes.")

elif all([consent1, consent2]):
    if st.button("Let's create a better dataset!"):
        st.switch_page("pages/01_Overview.py")