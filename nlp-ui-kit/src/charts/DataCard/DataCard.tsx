import React from "react";
import { cn } from "../../utils/cn";

export interface DataCardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Primary metric label, e.g. "Sản lượng điện hôm nay" */
  label: string;
  /** Numeric or string value, e.g. "24.6" */
  value: string | number;
  /** Unit shown after value, e.g. "kWh" or "kWp" */
  unit?: string;
  /** Optional trend vs previous period: positive = green, negative = red */
  trend?: number;
  /** Icon slot (pass an SVG or emoji node) */
  icon?: React.ReactNode;
  /** Color accent */
  color?: "primary" | "solar" | "ai";
}

const colorAccent: Record<NonNullable<DataCardProps["color"]>, string> = {
  primary: "border-t-primary",
  solar:   "border-t-solar",
  ai:      "border-t-ai",
};

export const DataCard: React.FC<DataCardProps> = ({
  label,
  value,
  unit,
  trend,
  icon,
  color = "solar",
  className,
  ...props
}) => {
  const trendSign = trend !== undefined ? (trend >= 0 ? "+" : "") : null;
  const trendColor =
    trend === undefined
      ? ""
      : trend >= 0
      ? "text-success"
      : "text-error";

  return (
    <div
      className={cn(
        "rounded-lg border border-neutral-200 bg-white p-4 shadow-sm",
        "border-t-4",
        colorAccent[color],
        className
      )}
      {...props}
    >
      {/* Header row */}
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-neutral-500">{label}</span>
        {icon && (
          <span className="text-xl text-neutral-400">{icon}</span>
        )}
      </div>

      {/* Value row */}
      <div className="mt-2 flex items-baseline gap-1">
        <span className="text-2xl font-bold text-neutral-900">{value}</span>
        {unit && (
          <span className="text-sm font-medium text-neutral-500">{unit}</span>
        )}
      </div>

      {/* Trend row */}
      {trend !== undefined && (
        <p className={cn("mt-1 text-xs font-medium", trendColor)}>
          {trendSign}{trend.toFixed(1)}% so với hôm qua
        </p>
      )}
    </div>
  );
};
