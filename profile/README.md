<div align="center">

# 🧠 NLP Labs Vietnam

**Foundational AI Infrastructure · Open Source · Vietnamese NLP · Financial Intelligence**

[![MIT License](https://img.shields.io/badge/license-MIT-3b82d4?style=flat-square)](LICENSE)
[![pnpm](https://img.shields.io/badge/pnpm-≥9-F69220?style=flat-square&logo=pnpm)](https://pnpm.io)
[![Turborepo](https://img.shields.io/badge/turborepo-enabled-EF4444?style=flat-square&logo=turborepo)](https://turbo.build)
[![Project Lead](https://img.shields.io/badge/lead-%40Dennis--nham-7c5cd8?style=flat-square)](https://github.com/Dennis-nham)

</div>

---

## 🌏 Giới thiệu

**NLP Labs Vietnam** là tổ chức mã nguồn mở xây dựng hạ tầng AI cốt lõi cho:

- 🇻🇳 **Xử lý ngôn ngữ tự nhiên tiếng Việt** và các ngôn ngữ ít tài nguyên
- 📈 **Nền tảng đầu tư thông minh** — phân tích cảm xúc thị trường tài chính thời gian thực
- 🎨 **Hệ thống thiết kế iOS** — `@alisababivip/*` Design System chuẩn Apple HIG
- 🌱 **Hệ sinh thái ESG** — Năng lượng xanh · Xe điện · Công nghệ bền vững

> Được vận hành bởi **NLP GROUP JOINT STOCK COMPANY** · Thành lập 2023

---

## 📦 Repositories

| Repo | Mô tả | Maintainer |
|------|--------|-----------|
| [`ios-design-system`](https://github.com/nlp-labs-vietnam/ios-design-system) | Pure iOS HIG Design System — Turborepo monorepo | [@thekingbao](https://github.com/thekingbao) |
| `investment-platform` | AI-driven NLP financial intelligence engine | [@nhamlapquoc](https://github.com/nhamlapquoc) |
| `core-nlp` | Vietnamese NLP models & algorithms | [@nhamlapquoc](https://github.com/nhamlapquoc) |
| `wikialisa-labs` | Satellite packages, parsers, open standards | [@wikialisalabs](https://github.com/wikialisalabs) |
| `.github` | Org-level templates, CODEOWNERS, issue templates | [@Dennis-nham](https://github.com/Dennis-nham) |

---

## 🏗️ Kiến trúc Monorepo Chuẩn

Tất cả repository chính của tổ chức tuân theo cấu trúc sau:

```
org-repo/
├── .github/
│   ├── CODEOWNERS              ← Phân quyền review tự động
│   ├── workflows/              ← CI/CD (GitHub Actions)
│   └── ISSUE_TEMPLATE/
├── packages/                   ← Shared libraries / npm packages
│   ├── tokens/
│   ├── core/
│   └── [module]/
├── apps/                       ← Deployable applications
│   ├── docs/
│   └── [app]/
├── services/                   ← Backend microservices (NLP workers)
├── MAINTAINERS.md              ← Danh sách người bảo trì
├── CODEOWNERS                  ← GitHub code ownership rules
├── CONTRIBUTING.md             ← Hướng dẫn đóng góp
├── CODE_OF_CONDUCT.md
├── pnpm-workspace.yaml
├── turbo.json
└── README.md
```

**Build system:** Turborepo + pnpm workspaces  
**Node requirement:** ≥ 20  
**Package manager:** pnpm ≥ 9

---

## 👥 Nhóm cốt lõi

| | Handle | Vai trò |
|---|---|---|
| 👑 | [@Dennis-nham](https://github.com/Dennis-nham) | Project Lead · Kiến trúc hệ thống · Roadmap |
| 🛠 | [@thekingbao](https://github.com/thekingbao) | Tech Lead · Infrastructure · UI/UX · Docs |
| 🤖 | [@nhamlapquoc](https://github.com/nhamlapquoc) | Core NLP Engineer · AI/ML · Data Pipeline |
| 📦 | [@wikialisalabs](https://github.com/wikialisalabs) | Org Admin · Packages · Parsers · Standards |

→ Xem chi tiết phân quyền tại [MAINTAINERS.md](MAINTAINERS.md)

---

## 🚀 Roadmap

```
Phase I  ✅  Genesis & Foundation
              └── Core NLP PoC · Community bootstrap · ios-design-system v0

Phase II 🔄  Infrastructure & Investment Platform  (2024–present)
              └── Turborepo monorepo · Kafka/RabbitMQ pipeline · Design system v1

Phase III 🎯 $50M Scale & Global Expansion         (24–36 months)
              └── GPU clusters · Enterprise licensing · Multi-lingual alpha
                  New York · London · Singapore · Tokyo
```

---

## 💰 Sponsorship

NLP Labs Vietnam đang thực hiện vòng gọi vốn chiến lược **$50,000,000 USD**.

- 🏆 **Vanguard Partner** ($20M–$30M+): Board seat · Pro-rata rights · Co-development
- 🚀 **Strategic Growth** ($5M–$15M): Observer rights · Beta access
- 🌱 **Ecosystem Builder** ($1M–$5M): Advisory board · Annual summit

📧 Liên hệ: [GitHub Sponsors](https://github.com/sponsors/Dennis-nham) · enterprise@nlpgroup.ai

---

## 🤝 Đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md) để bắt đầu.  
Tất cả đóng góp phải tuân thủ [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

```bash
git clone https://github.com/nlp-labs-vietnam/<repo>.git
pnpm install
pnpm build
pnpm dev
```

---

<div align="center">
<sub>NLP Group · Kiến tạo hệ sinh thái đổi mới bền vững · Năng lượng xanh · Xe điện · Công nghệ · AI · ESG</sub>
</div>
