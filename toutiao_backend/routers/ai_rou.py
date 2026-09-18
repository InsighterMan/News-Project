import asyncio
import json
import os
from urllib import error, request

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from models.toutiao_mod import User
from utils.auth import get_current_token
from utils.response import success_response


router = APIRouter(prefix="/api/ai", tags=["ai"])

OLLAMA_CHAT_URL = os.getenv("OLLAMA_CHAT_URL", "http://127.0.0.1:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=12)
    language: str = Field(default="zh-CN", pattern="^(zh-CN|en-US)$")


def _chat_with_ollama(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        OLLAMA_CHAT_URL,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with request.urlopen(req, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


@router.post("/chat")
async def chat_with_ai(
    data: ChatRequest,
    _: User = Depends(get_current_token),
):
    """Use the locally deployed Ollama model without exposing it to the browser."""
    system_prompt = (
        "You are the AI assistant for a news application. Reply in English. "
        "Be concise, helpful, and factual. Do not invent news facts; recommend checking the original source when needed."
        if data.language == "en-US"
        else "你是新闻应用中的 AI 助理。请使用简体中文回答，保持简洁、有帮助且符合事实。"
        "不要编造新闻事实；涉及新闻事实时，提醒用户以原始来源为准。"
    )
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [{"role": "system", "content": system_prompt}]
        + [message.model_dump() for message in data.messages],
        # DeepSeek-R1 needs enough output budget to complete its internal reasoning.
        "options": {"temperature": 0.6, "num_predict": 1024},
    }

    try:
        result = await asyncio.to_thread(_chat_with_ollama, payload)
    except (error.URLError, TimeoutError, OSError) as exc:
        raise HTTPException(
            status_code=503,
            detail="本地 AI 服务不可用，请确认 Ollama 正在运行且 deepseek-r1:7b 已安装。",
        ) from exc

    content = (result.get("message") or {}).get("content", "").strip()
    if not content:
        raise HTTPException(status_code=502, detail="本地 AI 服务没有返回有效回答，请稍后重试。")

    return success_response(data={"content": content, "model": OLLAMA_MODEL})
