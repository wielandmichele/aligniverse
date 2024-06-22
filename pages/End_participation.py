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

def insert_email(email):
    insert_query = """
    INSERT INTO df_emails (
        email
    ) VALUES (%s)
    """
    with pool.connect() as db_conn:
        db_conn.execute(insert_query, (
            email
        )
)

st.title("Thank you!")
st.write("Thank you for being part of our study and helping us improve the alignment of Large Language Models.")
st.balloons()

st.write("If you would like to take part in the prize draw for three Airbnb vouchers worth 50 euros each, please leave us your email address. We collect the email address individually for data protection reasons.")
email = st.text_input("Email",max_chars=50)
if st.button("Submit Email"):
    insert_email(email)                                                                                                                                                                             

st.divider()
st.write("If you'd like to spend more time rating, editing, and creating answers, please restart the survey. This is required for data protection purposes.")
st.link_button("Restart survey", "https://aligniverse.streamlit.app/")