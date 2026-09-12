import streamlit as st
from google import genai


st.title("AI Chatbot Comparison")
st.write("Applied Research Project")

st.subheader("Chatbot A - Gemini")

question = st.text_input("Enter a question")


if st.button("Send"):

    if question == "":
        st.warning("Please enter a question.")

    else:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]

            client = genai.Client(
                api_key=api_key
            )

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=question
            )

            st.write("Response:")
            st.write(response.text)

        except Exception as error:
            st.error(error)
