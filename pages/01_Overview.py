import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd

st.title("Let's create a better dataset")
st.write("""
Our mission is to create alignment datasets that incorporate your opinion on how LLMs should handle controversial topics.
You have the option to rate pre-generated responses, modify pre-generated responses, or create your own responses.
Once you finish one task, you can return and complete the other tasks. 
""")

st.subheader("Rate pre-generated responses")
st.write("You can rate pre-generated responses and share your thoughts on them.")
if st.button("Let's rate!"):
    st.switch_page("pages/02_Rate_responses.py")

st.subheader("Edit pre-generated responses")
st.write("You can edit pre-generated responses and customize them as you prefer.")
if st.button("Let's edit!"):
    st.switch_page("pages/03_Edit_responses.py")

st.subheader("Craft your own responses")
st.write("You can write your own responses and show us how you would want an LLM to answer questions.")
if st.button("Let's write!"):
    st.switch_page("pages/04_Craft_responses.py")

st.divider()

if st.button("End participation"):
    st.switch_page("pages/Demographics.py")
