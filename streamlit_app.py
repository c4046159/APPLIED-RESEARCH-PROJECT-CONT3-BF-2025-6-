import uuid
import pandas as pd
import streamlit as st

from config import BOTS
from engine import run_bot

st.set_page_config(
    page_title="Applied Research Project — Chatbot Comparison",
    page_icon="🤖",
    layout="wide",
)

st.title("Empirical Comparison of AI Chatbots")
st.caption(
    "Controlled research prototype: identical interface and prompt construction, "
    "with the AI backend as the principal experimental variable."
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = {key: [] for key in BOTS}

with st.sidebar:
    st.header("Research controls")
    blind_mode = st.toggle("Blind model labels", value=True)
    st.write("Session:", st.session_state.session_id[:8])

    if st.button("Start new session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.history = {key: [] for key in BOTS}
        st.rerun()

    st.divider()
    st.markdown(
        "**Privacy:** Do not enter personal, confidential, commercially sensitive, "
        "or client-identifiable information. Research tests should use synthetic or public data."
    )

def get_secret(name: str):
    try:
        return st.secrets[name]
    except Exception:
        return None

api_keys = {
    "gemini": get_secret("GEMINI_API_KEY"),
    "groq": get_secret("GROQ_API_KEY"),
    "openrouter": get_secret("OPENROUTER_API_KEY"),
}

tabs = st.tabs([
    (BOTS[key].blind_label if blind_mode else BOTS[key].display_name)
    for key in BOTS
])

for tab, (bot_key, bot) in zip(tabs, BOTS.items()):
    with tab:
        label = bot.blind_label if blind_mode else bot.display_name
        st.subheader(label)
        if not blind_mode:
            st.caption(f"{bot.provider} · `{bot.model}`")

        if not api_keys[bot_key]:
            st.warning(
                f"Missing API key for {bot.provider}. Add it to "
                "`.streamlit/secrets.toml` locally or Community Cloud Secrets."
            )

        for msg in st.session_state.history[bot_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_message = st.chat_input(f"Message {label}", key=f"chat_{bot_key}")

        if user_message:
            st.session_state.history[bot_key].append(
                {"role": "user", "content": user_message}
            )
            with st.chat_message("user"):
                st.markdown(user_message)

            history_before_current = st.session_state.history[bot_key][:-1]

            with st.chat_message("assistant"):
                if not api_keys[bot_key]:
                    st.error("API key is not configured.")
                else:
                    with st.spinner("Generating response..."):
                        try:
                            result = run_bot(
                                bot_key=bot_key,
                                api_key=api_keys[bot_key],
                                user_message=user_message,
                                history=history_before_current,
                                session_id=st.session_state.session_id,
                            )
                            st.markdown(result.text)
                            metric_cols = st.columns(3)
                            metric_cols[0].metric("Latency", f"{result.latency_seconds:.2f} s")
                            metric_cols[1].metric("Input tokens", result.input_tokens or "n/a")
                            metric_cols[2].metric("Output tokens", result.output_tokens or "n/a")
                            st.session_state.history[bot_key].append(
                                {"role": "assistant", "content": result.text}
                            )
                        except Exception as exc:
                            st.error(f"Provider call failed: {exc}")

st.divider()
st.subheader("Research output")
st.write(
    "Every successful or failed call is logged locally to `data/chatbot_runs.csv` "
    "and `data/chatbot_runs.jsonl`. Do not commit raw participant or sensitive data."
)

try:
    df = pd.read_csv("data/chatbot_runs.csv")
    st.dataframe(df.tail(20), use_container_width=True)
except Exception:
    st.info("No runs logged yet.")
