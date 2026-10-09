# 🔀 Mô tả Pull Request

<!-- Mô tả rõ ràng thay đổi này làm gì và tại sao. -->
<!-- Câu đầu tiên sẽ được release-drafter dùng làm entry trong changelog. -->

## 📌 Issue liên quan

Closes #<!-- Số issue -->

---

## 🔖 Loại thay đổi

<!-- Đánh dấu X vào ô phù hợp -->

- [ ] `feat` — Tính năng mới (không phá vỡ tương thích ngược)
- [ ] `fix` — Sửa lỗi (không phá vỡ tương thích ngược)
- [ ] `docs` — Chỉ thay đổi tài liệu
- [ ] `refactor` — Tái cấu trúc code (không fix bug, không thêm feature)
- [ ] `perf` — Cải thiện hiệu năng
- [ ] `test` — Thêm hoặc sửa test
- [ ] `ci` — Thay đổi CI/CD
- [ ] `chore` — Thay đổi khác (build, dependencies...)
- [ ] ⚠️ **BREAKING CHANGE** — Phá vỡ tương thích ngược với phiên bản trước

---

## 🧪 Cách kiểm thử

<!-- Mô tả các bước để reviewer tự kiểm tra tính năng / bản sửa lỗi này. -->

**Môi trường cần thiết:**
- Python x.x / Node.js x.x
- ...

**Các bước kiểm thử:**
1. Clone branch này: `git checkout <branch-name>`
2. Cài đặt dependencies: `pip install -r requirements.txt`
3. Chạy: `...`
4. Kết quả mong đợi: `...`

**Chạy test tự động:**
```bash
pytest tests/ -v -k "tên_test_liên_quan"
```

---

## 📸 Ảnh chụp màn hình (nếu có thay đổi UI)

<!-- Kéo thả ảnh Before / After vào đây -->

| Trước | Sau |
|---|---|
| _(ảnh before)_ | _(ảnh after)_ |

---

## ✅ Checklist trước khi merge

**Tác giả xác nhận:**

- [ ] Tôi đã đọc [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Code tuân theo tiêu chuẩn của dự án (`ruff`, `black`, type hints)
- [ ] Đã thêm / cập nhật unit test cho thay đổi này
- [ ] Tất cả test hiện có (`pytest`) đều pass trên máy local
- [ ] Đã cập nhật tài liệu liên quan (README, docstring, CHANGELOG nếu cần)
- [ ] Không có secret, API key, hoặc thông tin nhạy cảm trong code
- [ ] Commit message tuân theo [Conventional Commits](https://www.conventionalcommits.org/)

**Nếu là BREAKING CHANGE:**

- [ ] Đã ghi rõ `BREAKING CHANGE:` trong commit message
- [ ] Đã cập nhật migration guide trong tài liệu

---

## 💬 Ghi chú cho Reviewer

<!-- Điền những điểm bạn muốn reviewer chú ý đặc biệt, hoặc những quyết định thiết kế cần thảo luận. -->
