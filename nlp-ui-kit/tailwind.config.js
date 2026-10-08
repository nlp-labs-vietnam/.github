/** @type {import('tailwindcss').Config} */

// ─── Auto-generated from tokens/tokens.json via `npm run tokens:sync` ────────
// DO NOT edit color/spacing/typography values manually — edit tokens.json first.

import tokens from "./tokens/tokens.json" assert { type: "json" };

const { colors, spacing, fontFamily, fontSize, borderRadius } = tokens;

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors,
      spacing,
      fontFamily,
      fontSize,
      borderRadius,
    },
  },
  plugins: [],
};
