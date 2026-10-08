import React from "react";

/**
 * TypingIndicator — the classic three-dot animation shown while the AI
 * is generating a response.
 */
export const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-center gap-3">
      {/* Avatar */}
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-ai text-white text-xs font-bold">
        AI
      </div>

      {/* Bubble */}
      <div className="flex items-center gap-1.5 rounded-2xl rounded-tl-sm bg-neutral-100 px-4 py-3">
        <span
          className="h-2 w-2 rounded-full bg-neutral-400 animate-bounce"
          style={{ animationDelay: "0ms" }}
        />
        <span
          className="h-2 w-2 rounded-full bg-neutral-400 animate-bounce"
          style={{ animationDelay: "150ms" }}
        />
        <span
          className="h-2 w-2 rounded-full bg-neutral-400 animate-bounce"
          style={{ animationDelay: "300ms" }}
        />
      </div>
    </div>
  );
};
