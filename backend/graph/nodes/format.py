# =============================================================================
# WHAT THIS FILE DOES
# =============================================================================
#
# This is the last node that runs, regardless of which path was taken.
# Its job is to make sure state["final_response"] has a clean, readable
# answer ready to send back to the user.
#
# There are three scenarios it handles:
#
#   1. General question path
#      This node has nothing to do — it returns an empty dict and
#      LangGraph moves on. The existing response is untouched.
#
#   2. News path — success
#      fetch_news returned articles. This node takes those articles,
#      formats them into a readable block of text, and asks Claude to
#      write a friendly 2-3 sentence summary of what's going on.
#      That summary becomes the final_response.
#
#   3. News path — something went wrong
#      Either fetch_news set an error, or the articles list is empty.
#      Instead of crashing or showing a blank screen, this node returns
#      a polite fallback message explaining what happened. The user always
#      gets a response, never a broken page.
#
# This node is essentially the safety net and the presentation layer
# combined — it cleans up after both paths and ensures the output is
# always a properly formatted string, never raw data.
# =============================================================================

from langchain_anthropic import ChatAnthropic
from graph.state import NewsGenieState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

def format_response(state: NewsGenieState) -> dict:
    if state.get("final_response"):
        return {}

    if state.get("error") or not state.get("articles"):
        msg = state.get("error") or "No articles found."
        return {"final_response": f"I couldn't fetch the news right now: {msg}"}

    articles_text = "\n\n".join(
        f"**{a['title']}** ({a['source']})\n{a['description']}"
        for a in state["articles"][:5]
    )
    prompt = f"Here are the latest {state.get('category', '')} headlines:\n\n{articles_text}\n\nWrite a brief, friendly summary of these stories for the user."
    result = llm.invoke([{"role": "user", "content": prompt}])
    return {"final_response": result.content}