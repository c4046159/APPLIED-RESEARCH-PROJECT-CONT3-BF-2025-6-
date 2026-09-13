import streamlit as st
import cohere

from google import genai


st.set_page_config(
    page_title="Applied Research Project - AI Chatbot Comparison",
    page_icon="🎓",
    layout="centered"
)


# -----------------------------------------
# SHU-INSPIRED VISUAL TREATMENT
# -----------------------------------------

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


# -----------------------------------------
# PROJECT HEADER
# -----------------------------------------

st.markdown(
    '<div class="shu-kicker">Academic Research Prototype</div>',
    unsafe_allow_html=True
)

st.title("APPLIED RESEARCH PROJECT (CONT3 BF-2025/6)")
st.caption("Module: 55-709708-BF-20256")

st.markdown(
    """
    <div class="shu-theme-note">
        The visual theme of this prototype is inspired by Sheffield Hallam University's
        online website and publicly available brand guidance. The application remains an
        independent student research prototype and is not an official Sheffield Hallam
        University digital service.
    </div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):

    st.subheader("Student Information")
    st.write("**Full Name:** Carlos Pizarro")
    st.write("**Email Address:** Carlos.Pizarro@student.shu.ac.uk")
    st.write("**Student ID:** 34046159")


st.subheader("Project Overview")

st.info(
    "This research prototype compares two large language model chatbot systems "
    "through the same Streamlit interface. The aim is to evaluate how the models "
    "respond to the same engineering questions under controlled conditions. "
    "Later stages of the project will provide both chatbots with the same "
    "research-safe engineering knowledge source and will compare measures such "
    "as response quality, groundedness, consistency and response time."
)

st.markdown(
    "**How to use the prototype:** Enter an engineering question in Chatbot A "
    "and submit it. Then open Chatbot B, enter the same question and submit it. "
    "The responses can then be compared under the same test conditions."
)

st.warning(
    "Disclaimer: This application is a non-commercial academic research prototype. "
    "It relies on third-party AI services, which remain subject to their own terms "
    "and conditions, availability, usage limits and policies. This project is not "
    "a commercial enterprise and is not operated for profit. No revenue is generated "
    "from the prototype; its development represents academic time and effort only."
)

st.divider()


# Create two chatbot tabs
tab_a, tab_b = st.tabs([
    "Chatbot A - Gemini",
    "Chatbot B - Cohere"
])


# -----------------------------------------
# CHATBOT A - GOOGLE GEMINI
# -----------------------------------------

with tab_a:

    st.subheader("Chatbot A")
    st.write("**Provider:** Google")
    st.write("**Model:** Gemini 3.5 Flash-Lite")
    st.write("**Connection:** Google GenAI API")
    st.success("Status: Operational")

    with st.container(border=True):

        question_a = st.text_input(
            "Engineering question",
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


# -----------------------------------------
# CHATBOT B - COHERE
# -----------------------------------------

with tab_b:

    st.subheader("Chatbot B")
    st.write("**Provider:** Cohere")
    st.write("**Model:** Command A+")
    st.write("**Model ID:** command-a-plus-05-2026")
    st.write("**Connection:** Cohere Chat API")
    st.success("Status: Operational")

    with st.container(border=True):

        question_b = st.text_input(
            "Engineering question",
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
