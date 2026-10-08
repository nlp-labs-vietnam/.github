import React from "react";
import { cn } from "../../utils/cn";

export interface CitationBlockProps {
  /** Reference index number shown as superscript, e.g. [1] */
  index: number;
  /** Document title, e.g. "Quy hoạch Điện VIII (QĐ 500/QĐ-TTg)" */
  title: string;
  /** Source / publisher */
  source?: string;
  /** Year of publication */
  year?: string | number;
  /** Direct URL to the source document */
  href?: string;
}

/**
 * CitationBlock — displayed below AI messages when the RAG pipeline
 * retrieves a passage from a reference document (e.g. Electricity Plan VIII).
 */
export const CitationBlock: React.FC<CitationBlockProps> = ({
  index,
  title,
  source,
  year,
  href,
}) => {
  return (
    <div className="mt-1 flex items-start gap-2 rounded-lg border border-ai-200 bg-ai-50 px-3 py-2 text-sm">
      {/* Index badge */}
      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-ai text-white text-xs font-bold">
        {index}
      </span>

      <div className="flex flex-col gap-0.5">
        {href ? (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-ai-700 underline-offset-2 hover:underline"
          >
            {title}
          </a>
        ) : (
          <span className="font-medium text-ai-700">{title}</span>
        )}
        {(source || year) && (
          <span className="text-xs text-neutral-500">
            {[source, year].filter(Boolean).join(" · ")}
          </span>
        )}
      </div>
    </div>
  );
};
