interface Props {
    role: "user" | "assistant";
    content: string;
}

export default function ChatMessage({ role, content }: Props) {
    return (
        <div className={`flex ${role === "user" ? "justify-end" : "justify-start"} mb-4`}>
            <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${role === "user"
                        ? "bg-emerald-500 text-white rounded-br-none"
                        : "bg-gray-800 text-gray-100 rounded-bl-none"
                    }`}
            >
                {content}
            </div>
        </div>
    );
}