// =============================================================================
// WHAT THIS FILE DOES
// =============================================================================
//
// This is the only place in the frontend that knows how to talk to the
// backend. Everything related to API calls lives here, and the rest of
// the frontend just imports sendMessage() when it needs to.
//
// API_URL reads from your .env.local file. In development that's
// http://localhost:8000 (your local Python server). When deployed to
// Vercel you set it to your Railway/Render backend URL and nothing
// else in the codebase needs to change.
//
// The two interfaces (Article and ChatResponse) define the exact shape
// of what comes back from the backend. TypeScript uses these to catch
// mistakes at build time — if the backend changes its response format,
// TypeScript will immediately flag every place that breaks.
//
// sendMessage() is the one function the UI calls. It takes the user's
// message and their selected category, sends them to POST /chat, and
// returns the parsed response. If the server returns an error status
// it throws an error, which the UI can catch and show to the user.
// =============================================================================

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface Article {
    title: string;
    description: string;
    url: string;
    source: string;
    publishedAt: string;
}

export interface ChatResponse {
    response: string;
    query_type: string;
    articles: Article[];
}

export async function sendMessage(
    message: string,
    category: string
): Promise<ChatResponse> {
    const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, category }),
    });

    const raw = await res.text();

    console.log("API_URL:", API_URL);
    console.log("Status:", res.status);
    console.log("Raw response:", raw);

    if (!res.ok) {
        throw new Error(`API error ${res.status}: ${raw}`);
    }

    return JSON.parse(raw);
}