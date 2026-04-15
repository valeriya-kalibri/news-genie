# =============================================================================
# WHAT THIS FILE DOES
# =============================================================================
#
# This is the brain of the whole backend. It assembles all the individual
# steps (nodes) into a connected workflow that LangGraph can actually run.
#
# Think of it like a director's script — it doesn't act itself, it just
# says who does what and in what order.
#
# The workflow goes like this:
#   1. Every message comes in through classify_query first
#   2. classify_query looks at the message and decides: is this a news
#      request or something else?
#   3. If it's news    → go to fetch_news (calls NewsAPI, returns articles)
#      If it's general → go to answer_general (returns a rejection message,
#                        no Claude call, no API cost)
#   4. Both paths end up at format_response, which packages the final answer
#   5. The result is sent back to the API
#
# NewsGenie is intentionally news-only. General questions get a polite
# message telling the user what the assistant can actually do.
#
# The `graph` variable at the bottom is what LangGraph Studio looks for.
# It's also what api/main.py imports to run queries against.
#
# If you open this project in LangGraph Studio, it reads langgraph.json,
# finds this file, and draws the whole workflow visually for you.
# =============================================================================
from langgraph.graph import StateGraph, END
from graph.state    import NewsGenieState
from graph.nodes    import classify_query, fetch_news, answer_general, format_response

def route(state: NewsGenieState) -> str:
    """Conditional edge: decide next node based on query_type."""
    return state.get("query_type", "general")

builder = StateGraph(NewsGenieState)

builder.add_node("classify_query",  classify_query)
builder.add_node("fetch_news",      fetch_news)
builder.add_node("answer_general",  answer_general)
builder.add_node("format_response", format_response)

builder.set_entry_point("classify_query")

builder.add_conditional_edges(
    "classify_query",
    route,
    {"news": "fetch_news", "general": "answer_general"},
)

builder.add_edge("fetch_news",     "format_response")
builder.add_edge("answer_general", "format_response")
builder.add_edge("format_response", END)

graph = builder.compile()
