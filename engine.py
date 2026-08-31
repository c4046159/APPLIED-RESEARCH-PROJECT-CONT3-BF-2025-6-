from config import BOTS, DEFAULT_MAX_OUTPUT_TOKENS, DEFAULT_TEMPERATURE
from providers import generate_gemini, generate_groq, generate_openrouter
from prompting import build_prompt
from research_logging import log_run

PROVIDER_FUNCS = {
    "gemini": generate_gemini,
    "groq": generate_groq,
    "openrouter": generate_openrouter,
}

def run_bot(
    bot_key: str,
    api_key: str,
    user_message: str,
    history=None,
    *,
    session_id: str,
    run_type: str = "interactive",
    prompt_id: str = "",
    category: str = "",
):
    bot = BOTS[bot_key]
    prompt = build_prompt(user_message, history)
    fn = PROVIDER_FUNCS[bot_key]

    try:
        result = fn(api_key, bot.model, prompt)
        log_run({
            "session_id": session_id,
            "run_type": run_type,
            "prompt_id": prompt_id,
            "category": category,
            "bot_key": bot.key,
            "blind_label": bot.blind_label,
            "provider": bot.provider,
            "model": bot.model,
            "temperature": DEFAULT_TEMPERATURE,
            "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
            "latency_seconds": round(result.latency_seconds, 4),
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
            "total_tokens": result.total_tokens,
            "finish_reason": result.finish_reason,
            "prompt": prompt,
            "response": result.text,
            "error": "",
        })
        return result
    except Exception as exc:
        log_run({
            "session_id": session_id,
            "run_type": run_type,
            "prompt_id": prompt_id,
            "category": category,
            "bot_key": bot.key,
            "blind_label": bot.blind_label,
            "provider": bot.provider,
            "model": bot.model,
            "temperature": DEFAULT_TEMPERATURE,
            "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
            "prompt": prompt,
            "response": "",
            "error": repr(exc),
        })
        raise
