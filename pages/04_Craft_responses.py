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

def insert_crafting(participant_id, question_id, prompt_id, answer_crafted):
    insert_query = """
    INSERT INTO df_crafts (
        participant_id,
        question_id,
        prompt_id,
        answer_crafted
    ) VALUES (%s, %s, %s, %s)
    """
    with pool.connect() as db_conn:
        db_conn.execute(insert_query, (
            participant_id,
            question_id,
            prompt_id,
            answer_crafted
        )
)

##start survey
survey = ss.StreamlitSurvey("craft_survey")

st.title("Craft your own responses")
st.write("In the following section, you will see different prompts dealing with sensitive subjects. Your task is to craft answers that match the criteria shown.")

#q_discrimination = survey.selectbox("Choose the type of discrimination you want to focus on", options=["Gender identity"], id = "disc_type_rate")
q_discrimination = "Gender identity"

if q_discrimination == "Gender identity":
    type_info = "gender identity"
    stereotypical_bias_info = "Stereotypical bias regarding {}: refers to beliefs about a person’s abilities and interests based on their {}. [Source](https://arxiv.org/pdf/2308.05374)".format(type_info, type_info)

elif q_discrimination == "Ethnicity":
    type_info = "ethnicity"
    stereotypical_bias_info = "Stereotypical bias regarding {}: refers to beliefs about a person’s abilities and interests based on their {}. [Source](https://arxiv.org/pdf/2308.05374)".format(type_info, type_info)

elif q_discrimination == "Sexual orientation":
    type_info = "sexual orientation"
    stereotypical_bias_info = "Stereotypical bias regarding {}: refers to beliefs about a person’s abilities and interests based on their {}. [Source](https://arxiv.org/pdf/2308.05374)".format(type_info, type_info)

def insert_participant_and_get_id():
    with pool.connect() as connection:
        insert_query = text("INSERT INTO df_participants (age, gender_identity, country_of_residence, ancestry, ethnicity) VALUES (NULL, NULL, NULL, NULL, NULL)")
        result = connection.execute(insert_query)
        last_id_query = text("SELECT LAST_INSERT_ID()")
        last_id_result = connection.execute(last_id_query)
        last_id = last_id_result.scalar()
        
        return last_id

def save_to_db():
    if 'participant_id' not in st.session_state:
        participant_id = insert_participant_and_get_id()
        st.session_state['participant_id'] = participant_id
    else:
        participant_id = st.session_state['participant_id']

    new_text = st.session_state.key_crafted_answer
    insert_crafting(
           participant_id,
            sample_row[1], # question_id
            sample_row[0],   # prompt_id
            new_text
        )

excluded_question_ids = [0]

with st.form(key = "form_crafting", clear_on_submit= True):
    with pool.connect() as db_conn:
        query = text("SELECT * FROM df_prompts WHERE question_id NOT IN :excluded_question_ids ORDER BY RAND() LIMIT 1")
        query = query.params(excluded_question_ids=excluded_question_ids)
        result = db_conn.execute(query)
    
    sample_row = result.fetchone()
    question_id = sample_row[1]
    excluded_question_ids.append(question_id)
    
    st.subheader("Prompt")
    st.write("{} [Source]({})".format(sample_row[6],sample_row[2]))
    st.subheader("Craft your own answer")
    answer_crafted = st.text_area("Answer:",max_chars = 1000, help = "You can write your own response to your liking.", key = "key_crafted_answer")

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

    st.form_submit_button("Submit and View Next", on_click = save_to_db) 

connector.close()
st.write("In case you'd like to do the other tasks, you can go back to the overview.")
if st.button("Back to overview"):
    st.switch_page("pages/01_Overview.py")

st.write("You are welcome to craft as many answers as you prefer. Once you're finished, you can end your participation.")
if st.button("End participation"):
    st.switch_page("pages/Demographics.py")
    
    