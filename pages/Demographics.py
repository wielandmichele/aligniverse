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

def insert_demographics(age, gender_identity, country_of_residence, ancestry, ethnicity):
    insert_query = """
    INSERT INTO df_participants (
        age,
        gender_identity,
        country_of_residence,
        ancestry,
        ethnicity
    ) VALUES (%s, %s, %s, %s, %s)
    """
    with pool.connect() as db_conn:
        db_conn.execute(insert_query, (
            age,
            gender_identity,
            country_of_residence,
            ancestry,
            ethnicity
        )
    )
##start survey
survey = ss.StreamlitSurvey("demographics_survey")

#load data
df_countries = pd.read_csv("UNSD_Methodology_ancestry.csv", sep = ";")

age_groups = ["I wish not to declare","18-30", "31-40", "41-50","51-60", "60<"]
pronouns = [
    "I wish not to declare",
    "she/her/hers",
    "he/him/his",
    "they/them/theirs",
    "ze/hir/hirs",
    "xe/xem/xyrs",
    "ey/em/eirs",
    "ve/ver/vis",
    "per/pers/perself"
]
racial_groups = [
    "I wish not to declare",
    "American Indian or Alaska Native",
    "Asian",
    "Black or African American",
    "Hispanic or Latino",
    "Middle Eastern or North African",
    "Native Hawaiian or Pacific Islander",
    "White"
]

list_countries = sorted(df_countries["Country or Area"].to_list())
list_countries.insert(0, "I wish not to declare")

st.title("You at Aligniverse")
st.write("Your ratings will contribute to the development of an open-source dataset, which AI practitioners can utilize to align their LLMs. For the creation of this dataset, it's important for us to gather some information about you to determine the specific demographic group you represent. Since demographic data will be aggregated, identifying individual participants will not be possible.")

q1_demo = survey.selectbox("Which age group do you belong to?", options=age_groups, id="Q1_demo", index=None)
q2_demo = survey.selectbox("What pronouns do you use to identify yourself?", options=pronouns, id="Q2_demo", index=None)
q3_demo = survey.multiselect("Which is your country of residence?", options=list_countries, id="Q3_demo")
q4_demo = survey.multiselect("Where do your ancestors (e.g., great-grandparents) come from?", options=list_countries, id="Q4_demo")
q5_demo = survey.multiselect("Which racial group(s) do you identify with?", options=racial_groups, id="Q5_demo")

if not all([q1_demo, q2_demo, q3_demo, q4_demo, q5_demo]):
    st.write("Please select one option for every question. You always have the option not to declare.")

elif all([q1_demo, q2_demo, q3_demo, q4_demo, q5_demo]):
    if st.button("Submit"):
        insert_demographics(
            q1_demo, #age
            q2_demo, #gender identity
            q3_demo, #country of residence
            q4_demo, #ancestry
            q5_demo  #ethnicity
        )
        st.title("Thank you for participating!")
        st.balloons()
