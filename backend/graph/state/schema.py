# =============================================================================
# WHAT THIS FILE DOES
# =============================================================================
#
# This file defines the "clipboard" — the shared object that gets passed
# between every step (node) in the LangGraph workflow.
#
# Every node reads from this, does its job, and writes its results back
# into it. LangGraph then automatically passes the updated version to the
# next node.
#
# Here is what each field holds:
#
#   user_message    The raw message the user typed in the chat
#
#   query_type      Filled in by classify_query. Will be either "news" or
#                   "general". This is what the routing decision is based on.
#
#   category        The news category the user selected in the UI — one of
#                   "technology", "finance", or "sports". Only used when
#                   query_type is "news".
#
#   articles        Filled in by fetch_news. A list of article objects
#                   returned by NewsAPI. Empty list if it's a general query.
#
#   final_response  The finished text that gets sent back to the user.
#                   Either written by answer_general or by format_response.
#
#   error           If something goes wrong (API key missing, network issue,
#                   etc.) the error message is stored here so format_response
#                   can return a helpful fallback instead of crashing.
# =============================================================================

from typing import TypedDict, Optional

class NewsGenieState(TypedDict):
    user_message:   str
    query_type:     str          # "news" | "general"
    category:       str          # "technology" | "finance" | "sports"
    articles:       list[dict]
    final_response: str
    error:          Optional[str]
