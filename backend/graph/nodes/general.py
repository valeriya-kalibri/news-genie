# =============================================================================
# WHAT THIS FILE DOES
# =============================================================================
#
# This node runs when classify_query decided the user asked a general
# question rather than a news request.
#
# NewsGenie is a news-only assistant, so instead of answering the question
# we return a fixed rejection message. No Claude call is made here at all —
# this costs nothing and responds instantly.
#
# The message is written into state["final_response"]. When format_response
# runs next, it sees that final_response is already filled in and passes
# it straight through unchanged.
# =============================================================================

from graph.state import NewsGenieState

REJECTION = (
    "I'm NewsGenie — I can only help with news updates. "
    "Try asking me for the latest technology, finance, or sports headlines!"
)

def answer_general(state: NewsGenieState) -> dict:
    return {"final_response": REJECTION}
