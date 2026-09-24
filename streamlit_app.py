import streamlit as st
import cohere

from google import genai
from google_drive import list_folder_files


st.set_page_config(
    page_title="Applied Research Project - AI Chatbot Comparison",
    layout="centered"
)


st.markdown(
    """
    <style>
        .shu-accent {
            display: flex;
            width: 100%;
            height: 8px;
            margin-bottom: 1.2rem;
            overflow: hidden;
            border-radius: 4px;
        }

        .shu-accent-maroon {
            width: 60%;
            background: #672146;
        }

        .shu-accent-crimson {
            width: 25%;
            background: #AC145A;
        }

        .shu-accent-pink {
            width: 15%;
            background: #E31C79;
        }

        .shu-kicker {
            color: #AC145A;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }

        .shu-theme-note {
            margin-top: 0.8rem;
            margin-bottom: 1rem;
            padding: 0.8rem 1rem;
            border-left: 4px solid #AC145A;
            background: #F7F5F6;
            color: #445063;
            line-height: 1.5;
        }
    </style>

    <div class="shu-accent">
        <div class="shu-accent-maroon"></div>
        <div class="shu-accent-crimson"></div>
        <div class="shu-accent-pink"></div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="shu-kicker">Academic Research</div>',
    unsafe_allow_html=True
)

st.title("APPLIED RESEARCH PROJECT (CONT3 BF-2025/6) 55-709708-BF-20256")
st.markdown(
    """
    <div class="Sheffield Hallam University theme disclaimer:">
        The visual theme of this web application was inspired by Sheffield Hallam University's
        online websites and other media and materials.
    </div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):

    st.subheader("Student Information")
    st.write("Name: Carlos Pizarro")
    st.write("Email: Carlos.Pizarro@student.shu.ac.uk")
    st.write("Student ID: 34046159")

st.subheader("Project Summary")

st.info(
    "This research prototype compares two large language model chatbot systems "
    "through the same Streamlit interface. The aim is to evaluate how the models"
    "respond to the same engineering questions under controlled conditions:"
    "Providing both chatbots with the same 'research-safe' documents and comparing measures such "
    "as response quality, groundedness, consistency and response time."    
)


st.markdown(
    "How to use: Enter a relevant question in Chatbot A, i.e., 'What Is a PLC?' "
    "and submit it."
    "Then open Chatbot B, enter the same question and submit it. "
    "The responses can then be compared under the same test conditions."
)

st.warning(
    "Disclaimer: This application is a non-commercial academic research prototype. "
    "It relies on third-party AI services, which remain subject to their own terms "
    "and conditions, availability, usage limits and policies."
)

st.divider()

tab_a, tab_b, tab_c = st.tabs([
    "Chatbot A - Gemini",
    "Chatbot B - Cohere",
    "TESTS and METRICS"
])

with tab_a:

    st.subheader("Chatbot A")
    st.write("Provider: Google")
    st.write("Model: Gemini 3.5 Flash-Lite")
    st.write("Connection: Google GenAI API")
    st.success("Status: Operational")

    with st.container(border=True):

        question_a = st.text_input(
            "Engineering related question",
            placeholder="e.g. What is a PLC?",
            key="question_a"
        )

        if st.button(
            "Ask Chatbot A",
            type="primary",
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

                    st.markdown("#### Response")

                    with st.chat_message("assistant"):
                        st.write(response.text)

                except Exception as error:
                    st.error(error)

with tab_b:

    st.subheader("Chatbot B")
    st.write("Provider: Cohere")
    st.write("Model: Command A+")
    st.write("Model ID: command-a-plus-05-2026")
    st.write("Connection: Cohere Chat API")
    st.success("Status: Operational")

    with st.container(border=True):

        question_b = st.text_input(
            "Engineering related question",
            placeholder="e.g. What is a PLC?",
            key="question_b"
        )

        if st.button(
            "Ask Chatbot B",
            type="primary",
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

                    answer = ""

                    for content in response.message.content:

                        if content.type == "text":
                            answer = content.text

                    if answer == "":
                        st.error("No text response was returned.")

                    else:
                        st.markdown("#### Response")

                        with st.chat_message("assistant"):
                            st.write(answer)

                except Exception as error:
                    st.error(error)


with tab_c:

    st.subheader("Research Documents and Test Preparation")

    st.info(
        "Current stage: Google Drive connection validation only. "
        "The files listed below are not yet being supplied to either chatbot. "
        "The next implementation milestone is to extract document text and provide "
        "the same retrieved context to both models."
    )

    with st.container(border=True):

        st.markdown("#### Google Drive Connection")

        try:

            files = list_folder_files()

            st.success(
                f"Connected to Google Drive. {len(files)} file(s) available."
            )

            if files:

                st.write("Documents available to the research prototype:")

                for file in files:
                    st.write(f"- {file['name']}")

            else:
                st.info(
                    "The configured Google Drive folder is accessible "
                    "but currently contains no files."
                )

        except Exception:
            st.error(
                "Google Drive connection could not be completed. "
                "Check the Streamlit Secrets, confirm that the Google Drive API "
                "is enabled, and make sure the research folder is shared with "
                "the service-account email address."
            )
