import React from "react";
import { cn } from "../utils/cn";

export interface ProgressBarProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Current value (0–100) */
  value: number;
  /** Optional label shown above the bar */
  label?: string;
  /** Optional text shown on the right side of the label row */
  valueLabel?: string;
  /** Color theme */
  color?: "primary" | "solar" | "ai" | "success" | "warning" | "error";
}

const colorMap: Record<NonNullable<ProgressBarProps["color"]>, string> = {
  primary: "bg-primary",
  solar:   "bg-solar",
  ai:      "bg-ai",
  success: "bg-success",
  warning: "bg-warning",
  error:   "bg-error",
};

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  label,
  valueLabel,
  color = "primary",
  className,
  ...props
}) => {
  const clamped = Math.min(100, Math.max(0, value));

  return (
    <div className={cn("w-full", className)} {...props}>
      {(label || valueLabel) && (
        <div className="mb-1 flex items-center justify-between text-sm text-neutral-600">
          {label && <span>{label}</span>}
          {valueLabel && <span className="font-medium">{valueLabel}</span>}
        </div>
      )}
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-neutral-200">
        <div
          className={cn("h-full rounded-full transition-all duration-500", colorMap[color])}
          style={{ width: `${clamped}%` }}
          role="progressbar"
          aria-valuenow={clamped}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
    </div>
  );
};
