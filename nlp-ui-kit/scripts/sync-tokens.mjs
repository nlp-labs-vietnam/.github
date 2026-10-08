/**
 * scripts/sync-tokens.mjs
 *
 * Reads tokens/tokens.json and regenerates the resolved tailwind.config.js.
 * Run via: npm run tokens:sync
 *
 * Usage in CI:
 *   npm run tokens:sync && git diff --exit-code tailwind.config.js
 *   (fails the pipeline if Figma tokens diverged from committed config)
 */

import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");

const tokens = JSON.parse(
  readFileSync(resolve(root, "tokens/tokens.json"), "utf-8")
);

const config = `/** @type {import('tailwindcss').Config} */
// ─── AUTO-GENERATED — do not edit manually ────────────────────────────────
// Source: tokens/tokens.json  |  Regenerate: npm run tokens:sync

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: ${JSON.stringify(tokens.colors, null, 6)},
      fontFamily: ${JSON.stringify(tokens.fontFamily, null, 6)},
      fontSize: ${JSON.stringify(tokens.fontSize, null, 6)},
      spacing: ${JSON.stringify(tokens.spacing, null, 6)},
      borderRadius: ${JSON.stringify(tokens.borderRadius, null, 6)},
      boxShadow: ${JSON.stringify(tokens.boxShadow, null, 6)},
    },
  },
  plugins: [],
};
`;

writeFileSync(resolve(root, "tailwind.config.js"), config, "utf-8");
console.log("✅  tailwind.config.js synced from tokens/tokens.json");
