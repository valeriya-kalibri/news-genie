# =============================================================================
# WHAT THIS FILE DOES
#
# This is the first node that runs for every single message. Its only job
# is to read what the user typed and decide: are they asking for news, or
# are they asking a general question?
#
# It does this by sending the user's message to Claude with a very strict
# system prompt that forces a one-word answer — either "news" or "general".
# No explanation, no punctuation, just the one word.
#
# The result gets written into state["query_type"], and the workflow uses
# that value to decide which node to go to next.
#
# The safety check at the bottom handles the rare case where Claude replies
# with something unexpected — if the answer isn't exactly "news" or
# "general", we default to "general" so the app never crashes.
#
# Examples of what gets classified as "news":
#   "What's happening in tech today?"
#   "Show me sports headlines"
#   "Latest finance news"
#
# Examples of what gets classified as "general":
#   "What is inflation?"
#   "Who won the 2022 World Cup?"
#   "Explain how interest rates work"
# =============================================================================

from langchain_anthropic import ChatAnthropic
from graph.state import NewsGenieState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

SYSTEM = """You classify user messages into exactly one of two categories:
- "news"    — the user wants current news, headlines, or recent events
- "general" — the user wants an answer, explanation, or help with something

Reply with ONLY the word: news   OR   general
No punctuation. No explanation."""

def classify_query(state: NewsGenieState) -> dict:
    result = llm.invoke([      # Send the system prompt and the user's message to Claude
        {"role": "system", "content": SYSTEM},  
        {"role": "user",   "content": state["user_message"]},
    ])
    query_type = result.content.strip().lower()  # pulls raw AI response, trims whitespace, and converts to lowercase.
    if query_type not in ("news", "general"):
        query_type = "general"
    return {"query_type": query_type}