"use client";

import { useState, useRef, useEffect } from "react";
import CategorySelector from "./components/CategorySelector";
import ChatInput from "./components/ChatInput";
import ChatMessage from "./components/ChatMessage";
import { sendMessage } from "../lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [category, setCategory] = useState("technology");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text: string) => {
    // Add user message immediately
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);

    try {
      const data = await sendMessage(text, category);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch (err) {
      console.error("Chat request failed:", err);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            err instanceof Error
              ? `DEBUG ERROR: ${err.message}`
              : "DEBUG ERROR: Unknown failure",
        },
      ]);
    
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 border-r border-gray-800 p-6 flex flex-col">
        <h1 className="text-2xl font-bold text-emerald-400 mb-2">NewsGenie</h1>
        <p className="text-gray-400 text-sm mb-8">Your AI news assistant</p>
        <p className="text-gray-500 text-xs uppercase tracking-wider mb-3">Category</p>
        <CategorySelector selected={category} onChange={setCategory} />
      </aside>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 p-6 overflow-y-auto">
          {messages.length === 0 ? (
            <p className="text-gray-500 text-center mt-20">
              Ask me about the latest news!
            </p>
          ) : (
            messages.map((msg, i) => (
              <ChatMessage key={i} role={msg.role} content={msg.content} />
            ))
          )}
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-800 rounded-2xl rounded-bl-none px-4 py-3 text-sm text-gray-400">
                Thinking...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
        <div className="p-4 border-t border-gray-800">
          <ChatInput onSend={handleSend} disabled={loading} />
        </div>
      </div>
    </main>
  );
}