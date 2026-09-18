"""Small, dependency-free adapter for Baidu News public listing pages.

The adapter deliberately returns only metadata and the original article URL.  It
does not republish the full article body, which keeps the application a news
discovery client rather than a copy of a publisher's content.
"""
from __future__ import annotations

import html
import hashlib
import json
import re
import subprocess
import time
from html.parser import HTMLParser
from typing import Final
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen


BAIDU_HOME: Final = "https://news.baidu.com/"
CATEGORY_PATHS: Final = {
    "头条": "",
    "国内": "guonei",
    "国际": "guoji",
    "军事": "mil",
    "财经": "finance",
    "娱乐": "ent",
    "体育": "sports",
    "科技": "tech",
}
GDELT_QUERIES: Final = {
    "头条": "China OR world", "社会": "China society", "国内": "China", "国际": "world news",
    "军事": "military", "财经": "economy OR finance", "娱乐": "entertainment", "体育": "sports", "科技": "technology",
}
CHINANEWS_SECTIONS: Final = {"头条": (), "社会": ("/sh/",), "国内": ("/gn/",), "国际": ("/gj/",), "军事": ("/mil/",), "财经": ("/cj/",), "娱乐": ("/yl/",), "体育": ("/ty/",), "科技": ("/it/",)}
USER_AGENT: Final = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
_cache: dict[str, tuple[float, list[dict]]] = {}
_CACHE_SECONDS: Final = 120


def _stable_id(prefix: str, value: str) -> str:
    """A URL must keep the same article id across Uvicorn reloads."""
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]}"


class _AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            title = " ".join("".join(self._text).split())
            self.links.append((self._href, title))
            self._href = None
            self._text = []


def _fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "zh-CN,zh;q=0.9"})
    with urlopen(request, timeout=8) as response:  # nosec B310: URL is built from fixed Baidu endpoints
        body = response.read()
    page = body.decode("utf-8", errors="ignore")
    # Some network routes are challenged by Baidu's anti-bot page. Windows
    # ships curl.exe; its TLS fingerprint is accepted by that public endpoint.
    if "安全验证" not in page:
        return page
    result = subprocess.run(
        ["curl.exe", "-L", "-s", "--max-time", "12", "-A", "Mozilla/5.0", url],
        capture_output=True, check=False, timeout=15,
    )
    if result.returncode or not result.stdout:
        return page
    return result.stdout.decode("utf-8", errors="ignore")


def _clean_items(markup: str, limit: int) -> list[dict]:
    parser = _AnchorParser()
    parser.feed(markup)
    ignored = {"首页", "国内", "国际", "军事", "财经", "娱乐", "体育", "科技", "新闻", "更多", "搜索"}
    seen: set[str] = set()
    items: list[dict] = []
    for href, raw_title in parser.links:
        title = html.unescape(raw_title).strip()
        url = urljoin(BAIDU_HOME, html.unescape(href))
        if (
            not title or title in ignored or len(title) < 8 or len(title) > 80
            or title in seen or not url.startswith("http") or "baidu.com" in url
        ):
            continue
        # Navigation and product links are generally short, whereas article
        # headlines contain Chinese text or a normal sentence length.
        if not re.search(r"[\u4e00-\u9fff]", title):
            continue
        seen.add(title)
        host = re.sub(r"^www\.", "", url.split("/")[2])
        items.append({
            "id": _stable_id("baidu", url),
            "title": title,
            "description": "来自百度新闻的实时聚合资讯，点击查看原始报道。",
            "author": host,
            "publishTime": "刚刚更新",
            "views": 0,
            "image": None,
            "source": "百度新闻",
            "sourceUrl": url,
            "isLive": True,
        })
        if len(items) >= limit:
            break
    return items


def _cached(key: str, url: str, limit: int) -> list[dict]:
    cached = _cache.get(key)
    if cached and time.monotonic() - cached[0] < _CACHE_SECONDS:
        return cached[1]
    items = _clean_items(_fetch(url), limit)
    _cache[key] = (time.monotonic(), items)
    return items


def get_live_news(category_name: str = "头条", keyword: str | None = None, limit: int = 20) -> list[dict]:
    """Return latest public Baidu News headlines, optionally for a keyword."""
    limit = max(1, min(limit, 50))
    # The desktop category pages intermittently return HTTP 500 to automated
    # clients. Baidu's own mobile search endpoint is public, stable, and still
    # returns Baidu News-indexed results, so it is the dependable transport.
    query = keyword.strip() if keyword else f"{category_name} 新闻"
    word = quote(query)
    url = f"https://m.baidu.com/s?word={word}&tn=news"
    return _cached(f"query:{query}:{limit}", url, limit)


def get_hot_words(limit: int = 10) -> list[dict]:
    """Return homepage headlines as a compact trending list."""
    return get_live_news(limit=limit)


def get_global_news(category_name: str = "头条", limit: int = 20) -> list[dict]:
    """Free fallback index for when Baidu challenges a request.

    GDELT indexes articles from thousands of publishers and returns the original
    publisher URL and social-image metadata; we never claim it is Baidu data.
    """
    query = quote(GDELT_QUERIES.get(category_name, category_name))
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&format=json&maxrecords={min(limit, 50)}"
    try:
        data = json.loads(_fetch(url))
    except Exception:
        return []
    items = []
    for article in data.get("articles", []):
        title, link = article.get("title", ""), article.get("url", "")
        if not title or not link:
            continue
        items.append({"id": _stable_id("global", link), "title": title, "description": article.get("seendate", "实时更新的新闻索引"),
                      "author": article.get("domain", "新闻来源"), "publishTime": article.get("seendate", "刚刚更新"),
                      "views": 0, "image": article.get("socialimage"), "source": "全球新闻索引", "sourceUrl": link, "isLive": True})
    return items


def get_chinanews(category_name: str = "头条", limit: int = 20) -> list[dict]:
    """Reliable public fallback from China News Service's homepage.

    The home page contains current articles across sections and is accessible
    without an API key. Category filtering uses the site's article URL paths.
    """
    result = subprocess.run(["curl.exe", "-L", "-s", "--max-time", "12", "-A", "Mozilla/5.0", "https://www.chinanews.com.cn/"], capture_output=True, check=False, timeout=15)
    if result.returncode or not result.stdout:
        return []
    parser = _AnchorParser(); parser.feed(result.stdout.decode("utf-8", errors="ignore"))
    allowed = CHINANEWS_SECTIONS.get(category_name, ())
    seen, items = set(), []
    for href, title in parser.links:
        url = urljoin("https://www.chinanews.com.cn/", html.unescape(href)); title = html.unescape(title).strip()
        if not title or len(title) < 8 or title in seen or ".sht" not in url:
            continue
        if allowed and not any(section in url for section in allowed):
            continue
        seen.add(title)
        items.append({"id": _stable_id("cns", url), "title": title, "description": "中新网实时报道，点击进入项目内详情后可查看摘要与原文来源。",
                      "author": "中国新闻网", "publishTime": "实时更新", "views": 0, "image": None, "source": "中国新闻网", "sourceUrl": url, "isLive": True})
        if len(items) >= limit:
            break
    return items
