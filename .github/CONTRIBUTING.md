# 🤝 Hướng dẫn Đóng góp — NLP Labs Vietnam

Cảm ơn bạn đã quan tâm đến việc đóng góp cho **NLP Labs Vietnam**! Tài liệu này là "luật chơi" chung áp dụng cho tất cả các repository trong tổ chức. Hãy đọc kỹ trước khi bắt đầu.

---

## 📋 Mục lục

1. [Quy tắc ứng xử](#quy-tắc-ứng-xử)
2. [Cách bắt đầu](#cách-bắt-đầu)
3. [Quy trình đóng góp](#quy-trình-đóng-góp)
4. [Quy ước đặt tên branch](#quy-ước-đặt-tên-branch)
5. [Tiêu chuẩn Commit (Conventional Commits)](#tiêu-chuẩn-commit-conventional-commits)
6. [Quy trình tạo Pull Request](#quy-trình-tạo-pull-request)
7. [Tiêu chí Review](#tiêu-chí-review)
8. [Tiêu chuẩn code](#tiêu-chuẩn-code)
9. [Báo cáo lỗi](#báo-cáo-lỗi)
10. [Đề xuất tính năng](#đề-xuất-tính-năng)
11. [Liên hệ](#liên-hệ)

---

## Quy tắc ứng xử

Dự án này tuân theo [Quy tắc Ứng xử Cộng đồng (Contributor Covenant v2.1)](.github/CODE_OF_CONDUCT.md). Khi tham gia, bạn đồng ý tuân thủ các điều khoản đó.

---

## Cách bắt đầu

### Yêu cầu môi trường

| Công cụ | Phiên bản tối thiểu |
|---|---|
| Python | ≥ 3.10 |
| Git | ≥ 2.40 |
| Node.js *(cho nlp-ui-kit)* | ≥ 20 LTS |

### Fork & Clone

```bash
# 1. Fork repository trên GitHub, sau đó clone về máy
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2. Thêm upstream để đồng bộ với bản gốc
git remote add upstream https://github.com/nlp-labs-vietnam/<repo-name>.git

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Đảm bảo test suite chạy thành công trước khi bắt đầu
pytest tests/ -v
```

---

## Quy trình đóng góp

```
Fork → Branch → Code → Test → Commit → Push → Pull Request → Review → Merge
```

---

## Quy ước đặt tên branch

Đặt tên branch theo quy ước sau để CI/CD và labeler hoạt động chính xác:

| Loại thay đổi | Tiền tố | Ví dụ |
|---|---|---|
| Tính năng mới | `feat/` | `feat/solar-irradiance-map` |
| Sửa lỗi | `fix/` | `fix/rag-retrieval-timeout` |
| Tài liệu | `docs/` | `docs/update-contributing` |
| Cải tiến hiệu năng | `perf/` | `perf/vector-search-cache` |
| Refactor | `refactor/` | `refactor/llm-chain-module` |
| CI/CD & DevOps | `ci/` | `ci/add-security-scan` |
| Hotfix khẩn cấp | `hotfix/` | `hotfix/critical-auth-bug` |

```bash
git checkout -b feat/ten-tinh-nang-cua-ban
```

---

## Tiêu chuẩn Commit (Conventional Commits)

Tất cả commit phải tuân theo định dạng [Conventional Commits](https://www.conventionalcommits.org/). Điều này cho phép tự động hóa changelog và tăng version theo semantic versioning.

### Định dạng

```
<type>(<scope>): <mô tả ngắn gọn>

[body tuỳ chọn — giải thích LÝ DO thay đổi, không chỉ nêu cái đã thay đổi]

[footer tuỳ chọn — ví dụ: Closes #123, BREAKING CHANGE: ...]
```

### Các loại commit hợp lệ

| Type | Ý nghĩa | Tăng version |
|---|---|---|
| `feat` | Tính năng mới | MINOR |
| `fix` | Sửa lỗi | PATCH |
| `docs` | Chỉ thay đổi tài liệu | PATCH |
| `style` | Thay đổi format, không ảnh hưởng logic | — |
| `refactor` | Tái cấu trúc code, không fix bug, không thêm feature | PATCH |
| `perf` | Cải thiện hiệu năng | PATCH |
| `test` | Thêm hoặc sửa test | — |
| `ci` | Thay đổi CI/CD configuration | — |
| `chore` | Các thay đổi không ảnh hưởng src hoặc test | — |
| `revert` | Hoàn tác commit trước | — |

> **BREAKING CHANGE:** Thêm `!` sau type hoặc thêm footer `BREAKING CHANGE:` để đánh dấu thay đổi phá vỡ tương thích ngược → tăng MAJOR version.

### Ví dụ thực tế

```bash
# Tính năng mới
feat(rag): thêm bộ lọc bức xạ mặt trời theo tỉnh thành

Người dùng có thể chỉ định tỉnh/thành phố để AI trả về số liệu
bức xạ chính xác hơn thay vì dùng giá trị trung bình quốc gia.

Closes #45

# Sửa lỗi
fix(llm): sửa lỗi timeout khi câu hỏi dài hơn 512 token

# Breaking change
feat(api)!: đổi endpoint /solar/calculate thành /v2/solar/estimate

BREAKING CHANGE: Clients cần cập nhật URL endpoint. Xem migration guide tại docs/migration-v2.md.

# Chỉ tài liệu
docs(contributing): bổ sung hướng dẫn cài đặt môi trường Windows

# CI/CD
ci: thêm job security-scan vào workflow CI
```

---

## Quy trình tạo Pull Request

1. **Đảm bảo branch đã cập nhật** với `upstream/main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Chạy toàn bộ kiểm thử** trước khi mở PR:
   ```bash
   ruff check .
   black --check .
   pytest tests/ -v --cov=src
   ```

3. **Điền đầy đủ PR template** bao gồm:
   - Mô tả thay đổi rõ ràng
   - Loại thay đổi (feature / bugfix / docs / ...)
   - Link đến Issue liên quan: `Closes #<số>`
   - Hướng dẫn kiểm thử cho reviewer

4. **Gắn nhãn phù hợp** cho PR (feat, fix, docs, ci/cd, ...) để release-drafter tự động tạo changelog.

5. **Yêu cầu ít nhất 1 review** từ thành viên `@nlp-labs-vietnam/core-team` trước khi merge.

---

## Tiêu chí Review

Reviewer sẽ kiểm tra theo thứ tự ưu tiên:

| Tiêu chí | Mô tả |
|---|---|
| ✅ **Đúng chức năng** | Code làm đúng những gì PR mô tả |
| ✅ **Test coverage** | Có unit test cho logic mới; coverage không giảm |
| ✅ **Không breaking** | Không phá vỡ tương thích ngược nếu không có `BREAKING CHANGE` |
| ✅ **Type safety** | Mypy không báo lỗi mới |
| ✅ **Hiệu năng** | Không có truy vấn N+1, không load model không cần thiết |
| ✅ **Bảo mật** | Không hardcode secret, không log dữ liệu nhạy cảm |
| ✅ **Tài liệu** | Docstring đầy đủ cho public API mới |

---

## Tiêu chuẩn code

### Python

- Tuân thủ [PEP 8](https://pep8.org/). Dùng `black` để format tự động.
- Type hints bắt buộc cho tất cả hàm public.
- Docstring theo chuẩn Google style.

```python
def calculate_solar_output(capacity_kwp: float, irradiance: float) -> float:
    """Tính sản lượng điện ước tính của hệ thống.

    Args:
        capacity_kwp: Công suất lắp đặt tính bằng kWp.
        irradiance: Bức xạ mặt trời trung bình (kWh/m²/ngày).

    Returns:
        Sản lượng điện ước tính (kWh/ngày).

    Example:
        >>> calculate_solar_output(5.0, 4.9)
        19.6
    """
    performance_ratio = 0.80
    return capacity_kwp * irradiance * performance_ratio
```

### Kiểm thử (Testing)

```bash
# Chạy toàn bộ test suite
pytest tests/ -v --cov=src --cov-report=term-missing

# Chạy một file test cụ thể
pytest tests/test_solar_calculator.py -v
```

---

## Báo cáo lỗi

Sử dụng mẫu **Bug Report** khi tạo Issue. Xem [`.github/ISSUE_TEMPLATE/bug_report.yml`](.github/ISSUE_TEMPLATE/bug_report.yml).

---

## Đề xuất tính năng

Sử dụng mẫu **Feature Request** khi tạo Issue. Xem [`.github/ISSUE_TEMPLATE/feature_request.yml`](.github/ISSUE_TEMPLATE/feature_request.yml).

---

## Liên hệ

- 📧 Email: `contact@nlpgroup.vn`
- 💬 Discussions: [github.com/nlp-labs-vietnam/nlpgroup/discussions](https://github.com/nlp-labs-vietnam/nlpgroup/discussions)
- 🐛 Issues: [github.com/nlp-labs-vietnam/nlpgroup/issues](https://github.com/nlp-labs-vietnam/nlpgroup/issues)

---

<p align="center"><sub>NLP Labs Vietnam · Mã nguồn mở · Made with ❤️ in Vietnam</sub></p>
