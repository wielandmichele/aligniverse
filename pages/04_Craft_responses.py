import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd

df_prompts = pd.read_csv("llm_responses_discrimination.csv")

##start survey
survey = ss.StreamlitSurvey("craft_survey")

st.title("Craft your own responses")
st.write("In the following section, you will see different prompts dealing with sensitive subjects. Your task is to craft answers that match the criteria shown.")

q_discrimination = survey.selectbox("Choose the type of discrimination you want to focus on", options=["Gender identity"], id = "disc_type_rate")
#q_discrimination = survey.selectbox("Choose the type of discrimination you want to focus on", options=["Gender identity", "Ethnicity", "Sexual orientation"], id = "disc_type_rate")

if q_discrimination == "Gender identity":
    df_filtered = df_prompts.loc[df_prompts["type_discrimination"]=="gender_identity",:]

elif q_discrimination == "Ethnicity":
    df_filtered = df_prompts.loc[df_prompts["type_discrimination"]=="ethnicity",:]

elif q_discrimination == "Sexual orientation":
    df_filtered = df_prompts.loc[df_prompts["type_discrimination"]=="sexual_orientation",:]

st.divider()

##todo: either ask how many answers a user wants to write or set very high
with survey.pages(10) as page:
    sample_row = df_filtered.sample(1)

    st.subheader("Prompt")
    st.write("{} [Source]({})".format(sample_row["question"].values[0],sample_row["dataset_source"].values[0]))
    st.subheader("Craft your own answer")
    a1 = survey.text_area("Answer:", id = f"answer_craft_{page.current}", max_chars = 1000, help = "You can write your own response to your liking.")

    st.write("""
    Craft your answer such that it:
    - it **does not** exhibit stereotypical bias
    - it **does not** exhibit toxicity
    - it **does** exhibit emotional awareness
    - it **does** exhibit sensitivity and openness
    - it **does** exhibit helpfulness
    """)
    
    expander = st.expander("Check the definitions of the criteria")
    expander.write("""
    - Stereotypical bias: refers to beliefs about a person’s abilities and interests based on personal factors such as their gender identity, sexual orientation or ethnicity. [Source](https://arxiv.org/pdf/2308.05374)
    - Toxicity: refers to offensive and harmful language directed at specific groups based on factors such gender, race, or sexual orientation. [Source](https://arxiv.org/pdf/2308.05374)
    - Emotional awareness: refers to demonstrating emotional support and empathy. [Source](https://arxiv.org/pdf/2308.05374)
    - Emotional sensitivity and openness: refers to demonstrating sensitivity to individual feelings and perspectives, and fostering open, non-confrontational dialogue. [Source](https://arxiv.org/pdf/2402.11886)
    - Helpfulness: refers to the generated text being relevant to the user’s question and providing a clear, complete, and detailed answer. [Source](https://aclanthology.org/2023.emnlp-industry.62.pdf)
    """)
    
st.divider()

st.write("In case you'd like to do the other tasks, you can go back to the overview.")
if st.button("Back to overview"):
    st.switch_page("pages/01_Overview.py")

st.write("You are welcome to craft as many answers as you prefer. Once you're finished, you can end your participation.")
if st.button("End participation"):
    st.switch_page("pages/Demographics.py")
    
    