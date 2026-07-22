# 07. Kiểm tra chất lượng

## Mức độ lỗi

### Blocker

- sai số field;
- mất ID;
- mất tag hoặc placeholder;
- thiếu/trùng dòng;
- ghi nhầm file;
- sai người nói;
- nội dung H-18 có nhân vật chưa xác định trưởng thành.

### Major

- sai nghĩa;
- sai xưng hô;
- sai thuật ngữ đã khóa;
- sai lore làm thay đổi cảnh;
- làm đổi mức độ cảm xúc hoặc consent.

### Minor

- câu hơi cứng;
- dấu câu;
- lặp từ;
- độ dài UI;
- lựa chọn từ chưa tối ưu nhưng không sai nghĩa.

Không bàn giao khi còn blocker.

## Structural QA

- So sánh số file.
- So sánh số dòng.
- So sánh số field từng dòng.
- So sánh ID/key.
- So sánh tag.
- So sánh placeholder.
- Kiểm tra encoding/newline.
- Kiểm tra parser hoặc import thử nếu có công cụ.

## Linguistic QA

Mỗi câu phải trả lời được:

- Ai nói?
- Nói với ai?
- Ý chính là gì?
- Sắc thái gì?
- Câu Việt có tự nhiên khi đọc thành tiếng không?
- Có dấu hiệu dịch từng chữ không?

## Character Voice QA

Theo từng nhân vật:

- tự xưng có đổi vô cớ không;
- cách gọi Chỉ Huy có đúng không;
- mức trang trọng có ổn định không;
- catchphrase có nhất quán không;
- lời thoại có phù hợp tính cách đã xác minh không.

## Consistency QA

Tìm toàn bộ biến thể của:

- Chỉ Huy;
- tên nhân vật;
- tên skill;
- vật phẩm;
- địa danh;
- tổ chức;
- cách gọi đặc biệt;
- thuật ngữ H-18 đã khóa.

Không “sửa đồng loạt” khi cùng từ Nhật có nghĩa khác theo ngữ cảnh.

## Diff Review

Diff cuối phải cho thấy:

- chỉ field dịch thay đổi;
- không có whitespace churn hàng loạt;
- không đổi encoding;
- không đổi ID;
- không thay file ngoài phạm vi.

## QA Log

Mỗi mục:

```text
File:
Dòng/ID:
Loại lỗi:
Nguồn:
Bản dịch hiện tại:
Đề xuất:
Mức độ:
Trạng thái:
```

## Tiêu chí hoàn tất

Một batch hoàn tất khi:

- không còn blocker;
- major đã sửa hoặc được người dùng chấp nhận;
- minor được ghi log nếu chưa sửa;
- glossary và registry được cập nhật;
- có thể tiếp tục batch sau mà không mất ngữ cảnh.
