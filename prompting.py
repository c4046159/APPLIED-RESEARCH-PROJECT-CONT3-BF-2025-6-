from typing import Iterable, Mapping
from config import SYSTEM_INSTRUCTION

def build_prompt(user_message: str, history: Iterable[Mapping[str, str]] | None = None) -> str:
    """Create the same plain-text prompt for every provider.

    Using one normalized text prompt reduces provider-specific prompt-format differences.
    """
    lines = [
        "SYSTEM INSTRUCTION:",
        SYSTEM_INSTRUCTION,
        "",
    ]

    history = list(history or [])
    if history:
        lines.append("CONVERSATION SO FAR:")
        for item in history:
            role = item.get("role", "user").upper()
            content = item.get("content", "")
            lines.append(f"{role}: {content}")
        lines.append("")

    lines.extend([
        "CURRENT USER REQUEST:",
        user_message,
        "",
        "ASSISTANT RESPONSE:",
    ])
    return "\n".join(lines)
