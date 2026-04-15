"use client";

import { useState } from "react";

interface Props {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: Props) {
    const [input, setInput] = useState("");

    const handleSend = () => {
        if (!input.trim()) return;
        onSend(input.trim());
        setInput("");
    };

    return (
        <div className="flex gap-3">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="Ask about the latest news..."
                disabled={disabled}
                className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-3 text-sm outline-none border border-gray-700 focus:border-emerald-500 transition-colors placeholder-gray-500 disabled:opacity-50"
            />
            <button
                onClick={handleSend}
                disabled={disabled || !input.trim()}
                className="bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-5 py-3 rounded-lg text-sm font-medium transition-colors"
            >
                Send
            </button>
        </div>
    );
}