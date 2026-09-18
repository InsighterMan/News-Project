import asyncio
import json

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from services.baidu_news import get_chinanews, get_global_news, get_hot_words, get_live_news


def _dedupe(items: list[dict]) -> list[dict]:
    """Preserve order while removing syndicated copies of the same headline."""
    seen: set[str] = set()
    result: list[dict] = []
    for item in items:
        key = "".join(str(item.get("title", "")).split()).replace("【", "").replace("】", "")
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result

router = APIRouter(prefix="/api/live", tags=["live-news"])


@router.get("/news")
async def live_news(
    category: str = Query("头条"),
    keyword: str | None = Query(None, max_length=60),
    limit: int = Query(20, ge=1, le=50),
):
    try:
        items = await asyncio.to_thread(get_live_news, category, keyword, limit)
        # Baidu sometimes serves an empty challenge page. Fall back to a real
        # multi-publisher index rather than returning an empty information flow.
        if not items:
            # China News is the dependable no-key fallback. For a keyword, get
            # a fresh public index first and only expose entries that match it.
            fallback = await asyncio.to_thread(get_chinanews, category, 50)
            if keyword:
                word = keyword.casefold()
                items = [item for item in fallback if word in item["title"].casefold() or word in item.get("description", "").casefold()]
            else:
                items = fallback
        if not items and not keyword:
            items = await asyncio.to_thread(get_global_news, category, limit)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="百度新闻暂时无法访问，请稍后重试") from exc
    items = _dedupe(items)[:limit]
    return {"code": 200, "message": "success", "data": {"list": items, "total": len(items), "source": items[0]["source"] if items else "暂无可用来源"}}


@router.get("/trending")
async def trending(limit: int = Query(10, ge=1, le=20)):
    try:
        items = await asyncio.to_thread(get_hot_words, limit)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="百度新闻热榜暂时无法访问") from exc
    return {"code": 200, "message": "success", "data": items}


@router.get("/stream")
async def live_stream(category: str = Query("头条"), keyword: str | None = Query(None, max_length=60)):
    """SSE feed. The browser receives a fresh headline snapshot every 60 seconds."""
    async def event_generator():
        while True:
            try:
                items = await asyncio.to_thread(get_live_news, category, keyword, 20)
                yield f"event: news\ndata: {json.dumps(items, ensure_ascii=False)}\n\n"
            except Exception:
                yield "event: error\ndata: {\"message\": \"source unavailable\"}\n\n"
            await asyncio.sleep(60)

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})
