// Utility: merges Tailwind class names safely (handles conditional classes)
// Lightweight alternative to clsx + tailwind-merge
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
