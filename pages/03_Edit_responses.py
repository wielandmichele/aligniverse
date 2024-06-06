import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd
from sqlalchemy import text
from google.cloud.sql.connector import Connector
from st_files_connection import FilesConnection
import pymysql
import sqlalchemy
import os

from google.cloud.sql.connector import Connector
from google.oauth2 import service_account
from google.cloud import storage

INSTANCE_CONNECTION_NAME = st.secrets["INSTANCE_CONNECTION_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASS = st.secrets["DB_PASS"]
DB_NAME = st.secrets["DB_NAME"]

#file_path = "aligniverse-d410d1ab5017.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = file_path

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# initialize Connector object
connector = Connector(credentials=credentials)

def getconn():
    # function to return the database connection object
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

def insert_editing(participant_id, question_id, prompt_id, answer_edited):
    insert_query = """
    INSERT INTO df_edits (
        participant_id,
        question_id,
        prompt_id,
        answer_edited
    ) VALUES (%s, %s, %s, %s)
    """
    with pool.connect() as db_conn:
        db_conn.execute(insert_query, (
            participant_id,
            question_id,
            prompt_id,
            answer_edited
        )
)

def save_to_db():
    new_text = st.session_state.key_edited_answer
    insert_editing(
            st.session_state['participant_id'],
            sample_row[1], # question_id
            sample_row[0],   # prompt_id
            new_text
        )

##start survey
survey = ss.StreamlitSurvey("edit_survey")
st.title("Edit pre-generated LLM responses")
st.write("In the following section, you will see different prompts and their corresponding answers. Your task is to edit the answers based on the displayed criteria. We generated the answers using a Large Language Model (LLM). Here are the details of the model we used: [Wizard-Vicuna-7B-Uncensored-GPTQ](https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-GPTQ)")

q_discrimination = survey.selectbox("Choose the type of discrimination you want to focus on", options=["Gender identity"], id = "disc_type_rate")
#q_discrimination = survey.selectbox("Choose the type of discrimination you want to focus on", options=["Gender identity", "Ethnicity", "Sexual orientation"], id = "disc_type_rate")

if q_discrimination == "Gender identity":
    type_info = "gender identity"
    stereotypical_bias_info = "Stereotypical bias regarding {}: refers to beliefs about a person’s abilities and interests based on their {}. [Source](https://arxiv.org/pdf/2308.05374)".format(type_info, type_info)

elif q_discrimination == "Ethnicity":
    type_info = "ethnicity"
    stereotypical_bias_info = "Stereotypical bias regarding {}: refers to beliefs about a person’s abilities and interests based on their {}. [Source](https://arxiv.org/pdf/2308.05374)".format(type_info, type_info)

elif q_discrimination == "Sexual orientation":
    type_info = "sexual orientation"
    stereotypical_bias_info = "Stereotypical bias regarding {}: refers to beliefs about a person’s abilities and interests based on their {}. [Source](https://arxiv.org/pdf/2308.05374)".format(type_info, type_info)

excluded_prompt_ids = [0]

with st.form(key = "form_editi", clear_on_submit= True):
    with pool.connect() as db_conn:
        query = text("SELECT * FROM df_prompts WHERE prompt_id NOT IN :excluded_prompt_ids ORDER BY RAND() LIMIT 1")
        query = query.params(excluded_prompt_ids=excluded_prompt_ids)
        #query = text("SELECT * FROM df_prompts ORDER BY RAND() LIMIT 1")
        result = db_conn.execute(query)
    
    sample_row = result.fetchone()
    prompt_id = sample_row[0]
    excluded_prompt_ids.append(prompt_id)

    st.subheader("Prompt")
    prompt_id = sample_row["prompt_id"]
    st.write("{} [Source]({})".format(sample_row[6],sample_row[2]))

    st.subheader("Edit pre-generated answer")
    answer_edited = st.text_area("Answer:", value = sample_row[7], key = "key_edited_answer", max_chars = 1000, help = "You can write your own response to your liking.")
    
    st.write("""
    Edit the pre-generated answer such that it:
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

    st.form_submit_button("Submit and View Next", on_click = save_to_db)

connector.close()
st.write("In case you'd like to do the other tasks, you can go back to the overview.")
if st.button("Back to overview"):
    st.switch_page("pages/01_Overview.py")

st.write("You are welcome to edit as many answers as you prefer. Once you're finished, you can end your participation.")
if st.button("End participation"):
    st.switch_page("pages/Demographics.py")