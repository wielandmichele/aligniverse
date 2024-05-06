import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd

st.title("Let's create a better dataset")
st.write("You can choose between rating pre-defined responses or craft your own responses. After completing one task, you can come back and do the other task as well.")

st.subheader("Rate pre-defined responses")
st.write("You can rate generated responses and tell us which ones you prefer.")
if st.button("Let's rate!"):
    st.switch_page("pages/02_Rate_responses.py")

st.subheader("Craft your own responses")
st.write("You can write your own responses and show us how you would want an LLM to answer questions.")
if st.button("Let's write!"):
    st.switch_page("pages/03_Craft_responses.py")

st.divider()

if st.button("End participation"):
    st.title("Thank you for participating!")
    st.balloons()