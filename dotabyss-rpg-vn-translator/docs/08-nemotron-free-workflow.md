# 08. Quy trình tối ưu cho Nemotron 3 Ultra bản miễn phí

Model mục tiêu:

```text
nvidia/nemotron-3-ultra-550b-a55b:free
```

## Nguyên tắc vận hành

Endpoint miễn phí có thể chậm, quá tải hoặc ngắt giữa lô. Quy trình phải có khả năng tiếp tục mà không dịch lại toàn bộ.

## Kích thước lô

Khuyến nghị ban đầu:

- 20–40 dòng hội thoại thường;
- 10–25 dòng lore;
- 10–20 dòng H-18;
- giảm lô khi nhiều người nói hoặc nhiều tag.

Không đưa hàng nghìn dòng vào một prompt chỉ vì context window cho phép. Mục tiêu là độ nhất quán và khả năng phục hồi, không phải dùng hết context.

## Prompt contract

Mỗi request phải có thứ tự:

1. vai trò;
2. luật bất biến;
3. context scene;
4. character registry trích yếu;
5. glossary liên quan;
6. input;
7. định dạng output bắt buộc;
8. checklist im lặng.

Dòng cuối nên nhắc:

```text
Chỉ xuất dữ liệu đã dịch đúng định dạng. Không giải thích, không dùng code fence.
```

## Hai lượt xử lý

### Lượt 1 — Translation

Dịch và giữ cấu trúc.

### Lượt 2 — Review

Đưa nguồn + bản dịch vào một request riêng, yêu cầu chỉ trả về các dòng cần sửa hoặc toàn batch đã sửa. Không yêu cầu model tự khen/chấm điểm chung chung.

## Context carry-over

Batch mới mang theo:

- 5–10 dòng cuối batch trước;
- glossary delta;
- character voice delta;
- scene summary tối đa 5 câu;
- danh sách unresolved items.

Không mang lại toàn bộ lịch sử chat nếu không cần.

## Resume manifest

Sau mỗi batch lưu:

```text
file
start_line
end_line
first_id
last_id
status
output_path
qa_status
timestamp
```

Khi lỗi mạng:

- không dịch lại batch đã ghi thành công;
- kiểm tra output có đủ dòng;
- tiếp tục từ batch chưa hoàn tất;
- không ghép hai response chưa xác minh.

## Cấu hình sinh

Nếu provider/Hermes hỗ trợ:

- temperature khoảng 0.2–0.4 cho bản dịch nhất quán;
- tránh temperature cao trong file kỹ thuật;
- giới hạn output đủ cho batch, không quá ngắn.

Đây là gợi ý, không phải điều kiện bắt buộc. Chất lượng phải được xác nhận bằng QA.

## Khi model bắt đầu lan man

Rút gọn prompt nhưng giữ:

- field contract;
- glossary;
- xưng hô;
- output-only;
- ví dụ một dòng đúng;
- batch nhỏ hơn.

Nếu model thêm giải thích, không chèn response đó vào file. Chạy lại batch với output contract nghiêm ngặt.
