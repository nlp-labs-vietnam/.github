// ─── Base Components ──────────────────────────────────────────────────────────
export { Button }      from "./components/Button";
export type { ButtonProps } from "./components/Button";

export { Card }        from "./components/Card";
export type { CardProps } from "./components/Card";

export { Badge }       from "./components/Badge";
export type { BadgeProps } from "./components/Badge";

export { ProgressBar } from "./components/ProgressBar";
export type { ProgressBarProps } from "./components/ProgressBar";

// ─── AI Chat Components ───────────────────────────────────────────────────────
export { ChatBubble }     from "./ai-chat/ChatBubble";
export type { ChatBubbleProps } from "./ai-chat/ChatBubble";

export { TypingIndicator } from "./ai-chat/TypingIndicator";

export { CitationBlock }  from "./ai-chat/CitationBlock";
export type { CitationBlockProps } from "./ai-chat/CitationBlock";

// ─── Solar / Energy Chart Components ─────────────────────────────────────────
export { DataCard }   from "./charts/DataCard";
export type { DataCardProps } from "./charts/DataCard";

export { SolarGauge } from "./charts/SolarGauge";
export type { SolarGaugeProps } from "./charts/SolarGauge";

// ─── Utilities ────────────────────────────────────────────────────────────────
export { cn } from "./utils/cn";
