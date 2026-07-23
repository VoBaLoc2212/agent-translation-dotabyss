# Dot Abyss Novel Translation - Progress Report
**Updated**: 2026-07-23

## Workspace
- **Working Dir**: `C:/Users/asaga`
- **Translation Root**: `E:/AgentTranslation/dotabyss-translation-main/translations/novels/`
- **Report Dir**: `E:/AgentTranslation/dotabyss-rpg-vn-translator/work/`

## Current Progress
| Metric | Value |
|---|---:|
| Total folders in tracker | 965 |
| `vi.json` currently present on disk | 32 |
| Tracker marked `SKIPPED_OVERLAP` | 165 |
| Tracker marked `COMPLETED` | 9 |
| Tracker marked `PENDING` | 791 |
| Tracker completed-like total (`COMPLETED + SKIPPED_OVERLAP`) | 174 |

## Current State Summary
- Pipeline đang dùng là **dịch trực tiếp `ja.json` -> `vi.json`** cho novels.
- Các scene đã có `.txt` ở pipeline cũ được đánh dấu **`SKIPPED_OVERLAP`** và không cần tạo `vi.json` nữa.
- Đã hoàn thành một đợt **cleanup toàn bộ lỗi nhiễm chữ Hán trong các `vi.json` đã scan**.
- Kết quả audit cuối: **0 file `vi.json` còn nhiễm chữ Hán** trong tập đã quét.

## Key Rules Being Enforced
- `司令官` / `Commander` -> `Chỉ Huy` khi là danh xưng
- `%user%` phải được giữ nguyên
- `<user>` -> `%user%`
- Giữ nguyên `<br>` và tag cấu trúc
- Ưu tiên dấu phẩy fullwidth `，`
- Không dùng Google Translate / DeepL

## Work Completed So Far
1. Cập nhật workflow sang tạo `vi.json` trực tiếp thay vì tiếp tục pipeline `.txt` mới.
2. Tạo tracker cho toàn bộ 965 folder novels.
3. Phân tích overlap và đánh dấu 165 scene là `SKIPPED_OVERLAP`.
4. Tạo và verify 32 file `vi.json` hiện có trên disk.
5. Quét toàn bộ các `vi.json` đã tạo để tìm lỗi nhiễm chữ Hán.
6. Dịch lại và apply toàn bộ các artifact cleanup để đưa số file nhiễm chữ Hán về **0**.
7. Xóa các file artifact trung gian kiểu `retranslate_task_*`, `residual_han_*`, `build_residual_han_*` sau khi đã apply xong.

## Notes
- `progress_tracker_vi_json.json` vẫn được giữ lại làm **tracker nội bộ** cho tiến trình, không phải file báo cáo cho người đọc.
- File report này là bản Markdown chính cho tiến trình hiện tại.
