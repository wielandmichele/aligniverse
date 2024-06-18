import streamlit as st

st.title("Thank you")
st.write("Thank you for being part of our study and helping us improve the alignment of Large Language Models.")
st.balloons()

st.divider()
st.write("If you'd like to spend more time rating, editing, and creating answers, please restart the survey. This is required for data protection purposes.")
st.link_button("Restart survey", "https://aligniverse.streamlit.app/")