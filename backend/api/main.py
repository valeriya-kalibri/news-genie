# =============================================================================
# WHAT THIS FILE DOES
#
# This is the front door of the backend. It's a web server that listens for
# requests coming from the Next.js frontend and hands them to the LangGraph
# workflow to process.
#
# There is one main endpoint that matters:
#
#   POST /chat
#   The frontend sends a user message + a news category (technology, finance,
#   or sports). This file passes that into the LangGraph graph, waits for it
#   to finish, and sends the result back as JSON.
#
#   GET /health
#   Just a quick check to confirm the server is running. Useful for Vercel
#   and Railway to know the app is alive.
#
# The CORS section is important — it controls which websites are allowed to
# call this API. Right now it allows localhost (for development) and any
# Vercel deployment (for production). Without this, the browser would block
# the frontend from talking to the backend.
#
# load_dotenv() at the top reads your .env file so the API keys you put in
# there are available to the rest of the code.
# =============================================================================

# IMPORTS 

#FastAPI is the web framework. It lets us define routes (URLs) and what
#happens when someone calls them.
from fastapi import FastAPI

# CORSMiddleware is a security layer. Browsers block cross-origin requests
# by default. This middleware tells the browser "yes, these origins are
# allowed to talk to our API."
from fastapi.middleware.cors import CORSMiddleware

# BaseModel comes from Pydantic. It lets us define the exact shape of data
# we expect to receive or send. If the data doesn't match, FastAPI
# automatically returns a helpful error — no manual validation needed.
from pydantic import BaseModel

# load_dotenv reads your .env file and loads the key=value pairs into the
# system's environment variables. 
from dotenv import load_dotenv

# This actually triggers the .env file loading. It must run BEFORE any code
load_dotenv()

# This imports the compiled LangGraph workflow. "graph" is the object we
# call to process a user's message through the full classify → fetch/answer
# → format pipeline you saw in the diagram.
from graph.workflow import graph

# --- APP SETUP ----------------------------------------------------------------


app = FastAPI(title="NewsGenie API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    category: str = "technology"

class ChatResponse(BaseModel):
    response: str
    query_type: str
    articles: list[dict] = []

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        print("---- /chat called ----")
        print("message:", req.message)
        print("category:", req.category)

        result = await graph.ainvoke({
            "user_message": req.message,
            "category": req.category,
            "query_type": "",
            "articles": [],
            "final_response": "",
            "error": None,
        })

        print("graph result:", result)

        return ChatResponse(
            response=result.get("final_response", ""),
            query_type=result.get("query_type", ""),
            articles=result.get("articles", []),
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}