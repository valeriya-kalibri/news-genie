"use client";

const CATEGORIES = ["technology", "finance", "sports"];

interface Props {
  selected: string;
  onChange: (category: string) => void;
}

export default function CategorySelector({ selected, onChange }: Props) {
  return (
    <div className="flex flex-col gap-2">
      {CATEGORIES.map((cat) => (
        <button
          key={cat}
          onClick={() => onChange(cat)}
          className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${
            selected === cat
              ? "bg-emerald-500 text-white"
              : "bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white"
          }`}
        >
          {cat}
        </button>
      ))}
    </div>
  );
}