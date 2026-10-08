# 🤝 Hướng dẫn Đóng góp — NLP Labs Vietnam

Cảm ơn bạn đã quan tâm đến việc đóng góp cho **NLP Labs Vietnam**! Tài liệu này là "luật chơi" chung áp dụng cho tất cả các repository trong tổ chức. Hãy đọc kỹ trước khi bắt đầu.

---

## 📋 Mục lục

1. [Quy tắc ứng xử](#quy-tắc-ứng-xử)
2. [Cách bắt đầu](#cách-bắt-đầu)
3. [Quy trình đóng góp](#quy-trình-đóng-góp)
4. [Tiêu chuẩn code](#tiêu-chuẩn-code)
5. [Báo cáo lỗi](#báo-cáo-lỗi)
6. [Đề xuất tính năng](#đề-xuất-tính-năng)
7. [Liên hệ](#liên-hệ)

---

## Quy tắc ứng xử

Chúng tôi cam kết tạo ra một môi trường thân thiện, bao gồm và tôn trọng cho tất cả mọi người. Khi tham gia:

- ✅ Sử dụng ngôn ngữ lịch sự, tôn trọng và xây dựng.
- ✅ Chấp nhận phản hồi mang tính xây dựng một cách cởi mở.
- ✅ Tập trung vào những gì tốt nhất cho cộng đồng và dự án.
- ❌ Không sử dụng ngôn ngữ hoặc hình ảnh mang tính xúc phạm.
- ❌ Không quấy rối dưới bất kỳ hình thức nào.

---

## Cách bắt đầu

### Yêu cầu môi trường

- Python ≥ 3.10
- Git
- (Tuỳ dự án) Docker, Node.js — xem `README.md` của từng repository.

### Fork & Clone

```bash
# 1. Fork repository trên GitHub, sau đó clone về máy
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2. Thêm upstream để đồng bộ với bản gốc
git remote add upstream https://github.com/nlp-labs-vietnam/<repo-name>.git

# 3. Cài đặt dependencies
pip install -r requirements.txt
```

---

## Quy trình đóng góp

```
Fork → Branch → Code → Test → Pull Request → Review → Merge
```

### 1. Tạo branch mới

Đặt tên branch theo quy ước:

| Loại thay đổi | Tiền tố | Ví dụ |
|---|---|---|
| Tính năng mới | `feat/` | `feat/solar-irradiance-map` |
| Sửa lỗi | `fix/` | `fix/rag-retrieval-timeout` |
| Tài liệu | `docs/` | `docs/update-contributing` |
| Cải tiến hiệu năng | `perf/` | `perf/vector-search-cache` |
| Refactor | `refactor/` | `refactor/llm-chain-module` |

```bash
git checkout -b feat/ten-tinh-nang-cua-ban
```

### 2. Viết code & commit

Tuân theo định dạng [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <mô tả ngắn gọn bằng tiếng Anh hoặc tiếng Việt>

[body tuỳ chọn — giải thích lý do thay đổi]
[footer tuỳ chọn — đóng issue: Closes #123]
```

**Ví dụ:**
```
feat(rag): add province-level solar irradiance filtering

Người dùng có thể lọc dữ liệu theo tỉnh/thành phố để cải thiện
độ chính xác của gợi ý hệ thống.

Closes #45
```

### 3. Mở Pull Request

- Đảm bảo branch của bạn đã được cập nhật với `upstream/main`.
- Mô tả rõ ràng **vấn đề** bạn đang giải quyết và **cách tiếp cận**.
- Liên kết đến Issue liên quan (nếu có) bằng `Closes #<số>`.
- Đảm bảo tất cả CI checks đều pass.

---

## Tiêu chuẩn code

### Python

- Tuân thủ [PEP 8](https://pep8.org/). Dùng `black` để format tự động.
- Type hints bắt buộc cho các hàm public.
- Docstring theo chuẩn Google style cho mọi hàm, class và module.

```python
def calculate_solar_output(capacity_kwp: float, irradiance: float) -> float:
    """Tính sản lượng điện ước tính của hệ thống.

    Args:
        capacity_kwp: Công suất lắp đặt tính bằng kWp.
        irradiance: Bức xạ mặt trời trung bình (kWh/m²/ngày).

    Returns:
        Sản lượng điện ước tính (kWh/ngày).
    """
    performance_ratio = 0.80  # Hệ số hiệu suất thực tế điển hình
    return capacity_kwp * irradiance * performance_ratio
```

### Kiểm thử (Testing)

- Viết unit test cho mọi logic nghiệp vụ mới bằng `pytest`.
- Đảm bảo code coverage không giảm so với trước khi bạn thêm code.

```bash
pytest tests/ -v --cov=src
```

---

## Báo cáo lỗi

Hãy sử dụng mẫu **Bug Report** khi tạo Issue để cung cấp đủ thông tin cho đội ngũ xử lý nhanh nhất có thể. Xem [`.github/ISSUE_TEMPLATE/bug_report.md`](.github/ISSUE_TEMPLATE/bug_report.md).

---

## Đề xuất tính năng

Hãy sử dụng mẫu **Feature Request** khi tạo Issue. Một đề xuất tốt cần mô tả rõ **vấn đề** (không chỉ giải pháp) để đội ngũ có thể đánh giá đúng mức độ ưu tiên. Xem [`.github/ISSUE_TEMPLATE/feature_request.md`](.github/ISSUE_TEMPLATE/feature_request.md).

---

## Liên hệ

- 📧 Email: `contact@nlp-labs-vietnam.com`
- 💬 Discussions: [github.com/nlp-labs-vietnam/nlpgroup/discussions](https://github.com/nlp-labs-vietnam/nlpgroup/discussions)
- 🐛 Issues: [github.com/nlp-labs-vietnam/nlpgroup/issues](https://github.com/nlp-labs-vietnam/nlpgroup/issues)

---

<p align="center"><sub>NLP Labs Vietnam · Mã nguồn mở · Made with ❤️ in Vietnam</sub></p>
