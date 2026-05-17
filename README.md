# RAG Evaluation Dataset — Cẩm nang học vụ cao học UIT 2025

Bộ dữ liệu đánh giá (test set) cho hệ thống **Retrieval-Augmented Generation (RAG)** trên tài liệu Cẩm nang học vụ sau đại học — Trường Đại học Công nghệ Thông tin (UIT), khóa 20 năm 2025.

## Nguồn dữ liệu

| Mục | Chi tiết |
|---|---|
| **Tài liệu gốc** | `cam_nang_sau_dai_hoc_2025_0.pdf` |
| **Ngôn ngữ** | Tiếng Việt |
| **Phạm vi** | Quy chế đào tạo trình độ thạc sĩ, khóa 20/2025 |

## Thống kê

- **Tổng số mẫu**: 100

### Phân bố theo `category`

| Category | Số lượng | Mô tả |
|---|:---:|---|
| `fact` | 30 | Câu hỏi thực tế, trả lời trực tiếp từ cẩm nang |
| `rule_condition` | 25 | Câu hỏi về quy định, điều kiện, ràng buộc |
| `multi_hop` | 20 | Câu hỏi cần tổng hợp nhiều đoạn / nhiều mục |
| `scenario` | 15 | Câu hỏi tình huống giả định, cần suy luận |
| `out_of_scope` | 10 | Câu hỏi nằm ngoài phạm vi cẩm nang |

### Phân bố theo `difficulty`

| Difficulty | Số lượng |
|---|:---:|
| `easy` | 17 |
| `medium` | 63 |
| `hard` | 20 |

### Phân bố theo `expected_behavior`

| Behavior | Số lượng |
|---|:---:|
| `answer_from_context` | 90 |
| `refuse_or_say_not_enough_info` | 10 |

## Định dạng file

Dataset được cung cấp ở **2 định dạng** (nội dung giống nhau):

| File | Định dạng | Ghi chú |
|---|---|---|
| `handbook_test.jsonl` | JSON Lines | Mỗi dòng là 1 JSON object; `must_contain` và `must_not_contain` là **mảng** |
| `handbook_test.csv` | CSV | `must_contain` và `must_not_contain` phân cách bởi dấu `\|` |

## Schema

| Trường | Kiểu | Mô tả |
|---|---|---|
| `id` | `string` | Mã định danh mẫu (`HV_001` → `HV_100`) |
| `category` | `string` | Loại câu hỏi: `fact`, `rule_condition`, `multi_hop`, `scenario`, `out_of_scope` |
| `difficulty` | `string` | Độ khó: `easy`, `medium`, `hard` |
| `question` | `string` | Câu hỏi đầu vào cho hệ thống RAG |
| `expected_answer` | `string` | Câu trả lời chuẩn (ground truth) để đối chiếu |
| `source_section` | `string` | Mục/chương trong cẩm nang chứa thông tin liên quan. Với `out_of_scope`: có thể là `"Không có trong cẩm nang"` hoặc tên mục liên quan gần nhất |
| `source_pages` | `string` | Số trang tham chiếu trong PDF. **Để trống** với nhóm `out_of_scope` |
| `source_quote` | `string` | Đoạn trích gốc rút gọn từ tài liệu. **Để trống** với hầu hết nhóm `out_of_scope` |
| `expected_behavior` | `string` | Hành vi mong đợi: `answer_from_context` (trả lời từ context) hoặc `refuse_or_say_not_enough_info` (từ chối / nói không đủ thông tin) |
| `must_contain` | `list[string]` | Các từ khóa / ý chính **bắt buộc phải có** trong câu trả lời |
| `must_not_contain` | `list[string]` | Các từ khóa / thông tin **không được xuất hiện** (thường là thông tin bịa đặt ngoài cẩm nang) |

## Tiêu chí đánh giá Pass/Fail

Một mẫu được đánh giá **Pass** khi thỏa mãn **tất cả** điều kiện sau:

1. **Retrieval** — Hệ thống truy xuất được đoạn context liên quan đến câu hỏi.
2. **Correctness** — Câu trả lời đúng nội dung so với `expected_answer`.
3. **Completeness** — Câu trả lời chứa **phần lớn** các từ khóa trong `must_contain`.
4. **Safety** — Câu trả lời **không chứa** thông tin trong `must_not_contain`.
5. **Refusal** — Với nhóm `out_of_scope` (`expected_behavior = refuse_or_say_not_enough_info`), model phải **từ chối trả lời** hoặc nói rõ không đủ thông tin, thay vì tự suy đoán/bịa đặt.

## Lưu ý

- Nhóm `out_of_scope` (HV_091 → HV_100) có `source_pages` luôn để trống và `source_quote` hầu hết để trống — **đây là thiết kế có chủ đích** vì câu hỏi nằm ngoài phạm vi tài liệu.
- Một số mẫu `out_of_scope` (ví dụ: HV_096, HV_098, HV_099) vẫn có `source_section` trỏ tới mục liên quan trong cẩm nang, vì đây là câu hỏi hỏi **chi tiết không được đề cập** dù chủ đề có tồn tại (ví dụ: hỏi mức tiền cụ thể khi cẩm nang chỉ nói chung chung).
- File CSV có **BOM** (`\xEF\xBB\xBF`) ở đầu file — khi đọc bằng Python nên dùng encoding `utf-8-sig`.
