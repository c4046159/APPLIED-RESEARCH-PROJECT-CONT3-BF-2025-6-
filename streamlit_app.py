import streamlit as st

st.title("AI Chatbot Comparison")
st.write("Applied Research Project")

question = st.text_input("Enter a question")

if st.button("Send"):
    st.write("You asked:", question)
