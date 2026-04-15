langgraph dev --port 2025 (to open local environment).

LangGraph: Nodes & State
STATE (state/ folder)
Think of state as the shared memory of the entire workflow. It's a Python dictionary (or dataclass) that gets passed from node to node as the graph runs.
Every piece of information the graph needs to track lives here:
    What did the user ask?
    What category did they pick?
    Was it a news query or general query?
    What articles came back from the API?
    What is the final formatted response?

No node talks directly to another node. They all just read from and write to the state. That's how information flows through the graph.

NODES (nodes/ folder)
Nodes are the workers. Each node is a Python function that:
    Receives the current state
    Does one specific job
    Returns the updated state

In NewsGenie, the nodes map directly to the diagram you saw:
    classify_query → reads the message, decides if it's news or general
    fetch_news → calls the news API, writes articles into state
    answer_general → calls the AI, writes the answer into state
    format_response → reads everything, writes the final response into state

HOW THEY WORK
User message enters
       ↓
   [STATE] holds it
       ↓
  classify_query node reads state → updates state with query_type
       ↓
  fetch_news OR answer_general reads state → updates state with results
       ↓
  format_response reads state → writes final_response into state
       ↓
   [STATE] returned to main.py → sent back to frontend