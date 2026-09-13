import streamlit as st
import requests

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
# CHATBOT B - OPENROUTER / POOLSIDE LAGUNA
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

                openrouter_key = st.secrets["OPENROUTER_API_KEY"]

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": "Bearer " + openrouter_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "poolside/laguna-s-2.1:free",
                        "messages": [
                            {
                                "role": "user",
                                "content": question_b
                            }
                        ]
                    },
                    timeout=60
                )

                data = response.json()

                if response.status_code == 200 and "choices" in data:

                    st.write("Response:")
                    st.write(
                        data["choices"][0]["message"]["content"]
                    )

                elif "error" in data:

                    st.error(data["error"].get("message", str(data["error"])))

                else:

                    st.error("Unexpected response from OpenRouter:")
                    st.write(data)

            except Exception as error:
                st.error(error)
