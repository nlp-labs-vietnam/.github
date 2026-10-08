# @nlp-labs/ui-kit

> Core Design System — NLP Labs Vietnam  
> Thư viện UI dùng chung cho toàn bộ sản phẩm AI và Năng lượng của tổ chức.

---

## Cài đặt

```bash
npm install @nlp-labs/ui-kit
```

Thêm stylesheet một lần duy nhất tại root của ứng dụng:

```ts
// main.tsx hoặc _app.tsx
import "@nlp-labs/ui-kit/styles";
```

---

## Sử dụng nhanh

```tsx
import {
  Button, Card, Badge, ProgressBar,  // Base UI
  ChatBubble, TypingIndicator, CitationBlock,  // AI Chat
  DataCard, SolarGauge,              // Solar / Energy
} from "@nlp-labs/ui-kit";

// Nút bấm
<Button variant="solar" size="md">Tính toán hệ thống</Button>

// Thẻ dữ liệu điện mặt trời
<DataCard
  label="Sản lượng hôm nay"
  value="24.6"
  unit="kWh"
  trend={+5.2}
  color="solar"
/>

// Bong bóng chat AI
<ChatBubble role="assistant" message="Hệ thống 5 kWp phù hợp cho hộ gia đình..." />

// Trích dẫn nguồn RAG
<CitationBlock
  index={1}
  title="Quy hoạch Điện VIII"
  source="Thủ tướng Chính phủ"
  year={2023}
  href="https://vanban.chinhphu.vn"
/>

// Đồng hồ công suất mặt trời
<SolarGauge currentKw={3.2} capacityKwp={5} />
```

---

## Cấu trúc thư mục

```
src/
├── components/          # Base UI (Button, Card, Badge, ProgressBar)
├── ai-chat/             # Components hội thoại AI (ChatBubble, TypingIndicator, CitationBlock)
├── charts/              # Components biểu đồ năng lượng (DataCard, SolarGauge)
├── utils/               # cn() — class-name merger
└── styles.css           # Global Tailwind entry point

tokens/
└── tokens.json          # Design tokens (màu sắc, font, spacing, radii)
                         # Xuất từ Figma qua Tokens Studio plugin

scripts/
└── sync-tokens.mjs      # Đồng bộ tokens.json → tailwind.config.js
```

---

## Đồng bộ Design Token từ Figma

1. Cài plugin **Tokens Studio** trong Figma.
2. Export tokens → ghi đè `tokens/tokens.json`.
3. Chạy lệnh đồng bộ:

```bash
npm run tokens:sync
```

Lệnh này tự động cập nhật `tailwind.config.js`. Commit cả hai file để CI/CD nhận diện thay đổi.

---

## Build & Publish

```bash
# Build thư viện
npm run build

# Kiểm tra types
npm run typecheck

# Publish lên GitHub Packages hoặc npm
npm publish --access public
```

---

## License

MIT © [NLP Labs Vietnam](https://nlpgroup.vn)
