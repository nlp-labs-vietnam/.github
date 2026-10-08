import React from "react";
import { cn } from "../utils/cn";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Optional header title */
  title?: string;
  /** Optional subtitle below the title */
  subtitle?: string;
  /** Makes the card's padding compact */
  compact?: boolean;
}

export const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  compact,
  className,
  children,
  ...props
}) => {
  return (
    <div
      className={cn(
        "rounded-lg border border-neutral-200 bg-white shadow-sm",
        compact ? "p-3" : "p-5",
        className
      )}
      {...props}
    >
      {(title || subtitle) && (
        <div className="mb-4">
          {title && (
            <h3 className="text-base font-semibold text-neutral-900">{title}</h3>
          )}
          {subtitle && (
            <p className="mt-0.5 text-sm text-neutral-500">{subtitle}</p>
          )}
        </div>
      )}
      {children}
    </div>
  );
};
