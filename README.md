# NewsGenie – AI-Powered Information and News Assistant

## GitHub Repository

https://github.com/valeriya-kalibri/news-genie

## Project Overview

NewsGenie is an AI-powered news and information assistant designed to provide users with fast, intelligent, conversational access to current news and general information. Instead of requiring users to browse multiple news sources manually, the application interprets natural language requests, determines user intent, retrieves relevant news data when applicable, and returns AI-formatted responses in a concise, user-friendly format.

The goal of the project was to build a production-style full-stack AI application that combines modern frontend development, backend API design, workflow orchestration, and LLM integration into a unified product experience.

## Core Features

* Natural language news querying (e.g., “latest tech news”)
* AI-powered intent classification to determine query type
* Dynamic news retrieval from external news APIs
* AI-generated formatting and summarization of news results
* General information assistant fallback for non-news questions
* Category-based UI filtering for Technology, Finance, and Sports
* Responsive chat-style conversational interface

## Tech Stack

**Frontend**

* Next.js
* React
* TypeScript
* Tailwind CSS

**Backend**

* FastAPI
* Python

**AI / Workflow Orchestration**

* LangGraph
* Anthropic Claude API

**External Data Sources**

* NewsAPI

## System Architecture

The application follows a decoupled frontend/backend architecture:

1. User submits a message through the Next.js frontend interface.
2. Frontend sends the query to the FastAPI backend.
3. Backend passes the request into a LangGraph workflow.
4. LangGraph classifies whether the request is:

   * News-related
   * General information
5. Appropriate processing node executes:

   * News Node → Fetches news from NewsAPI
   * General Node → Routes to AI assistant response
6. Formatting node structures the final response.
7. Backend returns response to frontend for display.

## Key Technical Decisions

* **Next.js over Streamlit:** Chosen for production-grade frontend flexibility and stronger real-world engineering alignment.
* **FastAPI Backend:** Used to separate orchestration/business logic from frontend concerns.
* **LangGraph:** Implemented to create modular, extensible workflow routing for AI decision-making.
* **Decoupled Architecture:** Enables independent scaling and deployment of frontend and backend services.

## Setup Instructions

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

## Environment Variables Required

* Anthropic API Key
* NewsAPI Key

## Challenges & Learnings

During development, several engineering challenges were encountered and resolved:

* Debugged frontend/backend connectivity and CORS configuration issues
* Restructured backend startup/import paths for proper FastAPI deployment
* Refactored Git repository structure and cleaned commit history for production-ready version control
* Integrated LangGraph workflow orchestration into a full-stack web architecture

## Outcome

NewsGenie demonstrates the ability to architect and build a modern AI-powered web application using production-relevant technologies across frontend, backend, API integration, workflow orchestration, and deployment-ready repository management.
