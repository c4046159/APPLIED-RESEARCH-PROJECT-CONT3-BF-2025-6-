import streamlit as st
import cohere

from google import genai


st.title("AI Chatbot Comparison")
st.write("Applied Research Project")


# Create two chatbot tabs
tab_a, tab_b = st.tabs([
    "Chatbot A",
    "Chatbot B"
])


# -----------------------------------------
# CHATBOT A - GOOGLE GEMINI
# -----------------------------------------

with tab_a:

    st.subheader("Chatbot A")

    question_a = st.text_input(
        "Enter a question",
        key="question_a"
    )

    if st.button(
        "Send to Chatbot A",
        key="button_a"
    ):

        if question_a == "":
            st.warning("Please enter a question.")

        else:

            try:

                gemini_key = st.secrets["GEMINI_API_KEY"]

                client = genai.Client(
                    api_key=gemini_key
                )

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=question_a
                )

                st.write("Response:")
                st.write(response.text)

            except Exception as error:
                st.error(error)


# -----------------------------------------
# CHATBOT B - COHERE
# -----------------------------------------

with tab_b:

    st.subheader("Chatbot B")

    question_b = st.text_input(
        "Enter a question",
        key="question_b"
    )

    if st.button(
        "Send to Chatbot B",
        key="button_b"
    ):

        if question_b == "":
            st.warning("Please enter a question.")

        else:

            try:

                cohere_key = st.secrets["COHERE_API_KEY"]

                client = cohere.ClientV2(
                    api_key=cohere_key
                )

                response = client.chat(
                    model="command-a-plus-05-2026",
                    messages=[
                        {
                            "role": "user",
                            "content": question_b
                        }
                    ]
                )

                st.write("Response:")
                st.write(
                    response.message.content[0].text
                )

            except Exception as error:
                st.error(error)
