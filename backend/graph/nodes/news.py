# =============================================================================
# WHAT THIS FILE DOES
# =============================================================================
#
# This node only runs when classify_query decided the user wants news.
# Its job is to call the NewsAPI and fetch the 5 most recent headlines
# for whichever category the user selected in the UI.
#
# NewsAPI uses different category names than we do internally, so
# CATEGORY_MAP translates them — "finance" becomes "business" because
# that's what NewsAPI calls it.
#
# The result is a list of article objects saved into state["articles"].
# Each article has a title, description, url, source name, and publish date.
# That list gets passed to format_response, which turns it into a
# readable summary for the user.
#
# Error handling:
#   - If NEWS_API_KEY is missing from .env, it returns an empty list and
#     sets an error message. The app won't crash — format_response will
#     pick up the error and show a friendly fallback message instead.
#   - If the API call fails for any reason (network issue, rate limit, etc.)
#     the except block catches it and does the same thing.
#
# The timeout is set to 8 seconds — if NewsAPI takes longer than that
# something is wrong and we bail out rather than hanging forever.
# =============================================================================

import os, httpx
from graph.state import NewsGenieState

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
CATEGORY_MAP = {"technology": "technology", "finance": "business", "sports": "sports"}

def fetch_news(state: NewsGenieState) -> dict:
    api_key = os.getenv("NEWS_API_KEY", "")
    if not api_key:
        return {"articles": [], "error": "NEWS_API_KEY not configured."}

    category = CATEGORY_MAP.get(state.get("category", "technology"), "technology")
    try:
        resp = httpx.get(
            NEWS_API_URL,
            params={"category": category, "language": "en", "pageSize": 5},
            headers={"X-Api-Key": api_key},
            timeout=8.0,
        )
        resp.raise_for_status()
        data = resp.json()
        articles = [
            {
                "title":       a.get("title", ""),
                "description": a.get("description", ""),
                "url":         a.get("url", ""),
                "source":      a.get("source", {}).get("name", ""),
                "publishedAt": a.get("publishedAt", ""),
            }
            for a in data.get("articles", [])
        ]
        return {"articles": articles, "error": None}
    except Exception as e:
        return {"articles": [], "error": f"News fetch failed: {str(e)}"}
