from dataclasses import dataclass

@dataclass(frozen=True)
class BotConfig:
    key: str
    blind_label: str
    display_name: str
    provider: str
    model: str

BOTS = {
    "gemini": BotConfig(
        key="gemini",
        blind_label="Chatbot A",
        display_name="Google Gemini 3.1 Flash-Lite",
        provider="Google Gemini API",
        model="gemini-3.1-flash-lite",
    ),
    "groq": BotConfig(
        key="groq",
        blind_label="Chatbot B",
        display_name="OpenAI GPT-OSS 120B via Groq",
        provider="GroqCloud",
        model="openai/gpt-oss-120b",
    ),
    "openrouter": BotConfig(
        key="openrouter",
        blind_label="Chatbot C",
        display_name="NVIDIA Nemotron 3 Ultra via OpenRouter",
        provider="OpenRouter / NVIDIA",
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
    ),
}

SYSTEM_INSTRUCTION = (
    "You are a professional engineering and computing assistant. "
    "Answer the user's request directly and accurately. "
    "If information is uncertain or insufficient, state that clearly rather than inventing facts. "
    "Do not claim to have performed actions, accessed systems, or verified sources unless the supplied "
    "prompt explicitly provides that evidence. Keep answers concise unless detail is requested."
)

DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_OUTPUT_TOKENS = 900
