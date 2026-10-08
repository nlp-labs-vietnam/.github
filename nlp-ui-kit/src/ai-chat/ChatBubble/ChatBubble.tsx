import React from "react";
import { cn } from "../../utils/cn";

export interface ChatBubbleProps {
  /** Message content */
  message: string;
  /** Who sent this message */
  role: "user" | "assistant";
  /** ISO timestamp string */
  timestamp?: string;
  /** Show avatar icon for the assistant */
  showAvatar?: boolean;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  message,
  role,
  timestamp,
  showAvatar = true,
}) => {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        "flex w-full gap-3",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {/* Avatar (assistant only) */}
      {!isUser && showAvatar && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-ai text-white text-xs font-bold">
          AI
        </div>
      )}

      <div
        className={cn(
          "max-w-[75%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed",
          isUser
            ? "rounded-tr-sm bg-primary text-white"
            : "rounded-tl-sm bg-neutral-100 text-neutral-900"
        )}
      >
        <p className="whitespace-pre-wrap break-words">{message}</p>
        {timestamp && (
          <p
            className={cn(
              "mt-1 text-xs",
              isUser ? "text-primary-100" : "text-neutral-400"
            )}
          >
            {new Date(timestamp).toLocaleTimeString("vi-VN", {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </p>
        )}
      </div>
    </div>
  );
};
