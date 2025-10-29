
import os
from typing import Optional, Dict, Any

# OpenAI SDK (>=1.0) style
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception:
        return None

def grammar_feedback(prompt: str, lang: str = "ja") -> str:
    """
    Returns grammar feedback using OpenAI if available, else a graceful local fallback.
    """
    client = get_client()
    if client is None:
        # Local fallback: very simple hints
        hints = []
        if "i" in prompt and "I " not in prompt and not prompt.strip().startswith("I"):
            hints.append("英語では一人称 'I' は常に大文字です。")
        if "didn't" in prompt and "didn't went" in prompt:
            hints.append("'didn't' の後は動詞の原形（go）を使います。")
        if not hints:
            hints.append("大きな誤りは見つかりませんでした。句読点や大文字小文字を確認しましょう。")
        return "（ローカル簡易チェック）\\n- " + "\\n- ".join(hints)

    # Cloud path
    try:
        sys_prompt = (
            "You are an English grammar coach for a Japanese learner. "
            "Explain errors briefly and give a corrected version. "
            "Add short IPA for key words in slashes only when useful. "
            "Keep tone friendly. Reply in Japanese by default."
        )
        rsp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return rsp.choices[0].message.content.strip()
    except Exception as e:
        return "（OpenAI呼び出しに失敗しました。ローカル簡易チェックに切替）\\n- 大文字小文字や時制の基本を確認しましょう。"
