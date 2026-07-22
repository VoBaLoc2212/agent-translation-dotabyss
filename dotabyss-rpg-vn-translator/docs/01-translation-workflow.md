# 01. Quy trình dịch thuật

## Mục tiêu

Tạo bản dịch tiếng Việt tự nhiên, đồng nhất và có thể nhập trở lại game mà không phá cấu trúc dữ liệu.

## Giai đoạn A — Chuẩn bị

### A1. Bảo vệ dữ liệu

- Không sửa trực tiếp file nguồn trong lần chạy đầu tiên.
- Tạo thư mục `output` hoặc `staging`.
- Ghi lại hash, kích thước, encoding và newline của file nguồn khi công cụ cho phép.
- Nếu người dùng yêu cầu ghi đè, vẫn tạo backup hoặc patch trước.

**Điều kiện hoàn tất:** Có đường dẫn nguồn, đường dẫn output và cách khôi phục rõ ràng.

### A2. Nhận diện định dạng

Với mỗi loại file, xác định:

- delimiter;
- field được dịch;
- field kỹ thuật;
- quy tắc quote/escape;
- encoding;
- BOM;
- newline;
- tag hoặc placeholder;
- liệu một câu có thể trải qua nhiều dòng hay không.

**Điều kiện hoàn tất:** Có ít nhất một dòng được phân tích field-by-field và số cột kỳ vọng.

### A3. Tạo context pack

Mỗi lô dịch phải có:

- tên cảnh hoặc event;
- 5–10 dòng trước và sau;
- người nói;
- người nghe;
- quan hệ;
- glossary liên quan;
- quyết định xưng hô;
- bản dịch gần nhất của cùng nhân vật.

**Điều kiện hoàn tất:** Không còn dòng quan trọng bị dịch hoàn toàn cô lập.

## Giai đoạn B — Nghiên cứu

Chỉ tra cứu khi nó làm thay đổi một trong các yếu tố:

- giới tính hoặc vai trò;
- quan hệ với Chỉ Huy;
- tính cách;
- chức danh;
- năng lực, vũ khí, phe phái;
- bối cảnh event;
- cách gọi đặc biệt.

Ưu tiên:

1. File game và nội dung cùng event.
2. Glossary/character registry đã được người dùng duyệt.
3. Wiki GameWith.
4. Suy luận có gắn nhãn.

**Điều kiện hoàn tất:** Mọi quyết định không hiển nhiên đều có nguồn hoặc cờ `CẦN XÁC NHẬN`.

## Giai đoạn C — Dịch

### C1. Dịch ý trước, trau chuốt sau

Pass 1:

- giữ đủ nội dung;
- xác định chủ thể;
- giữ sắc thái;
- giữ cấu trúc kỹ thuật.

Pass 2:

- Việt hóa trật tự câu;
- sửa nhịp hội thoại;
- làm rõ chủ ngữ khi tiếng Việt cần;
- loại bỏ lối dịch máy;
- đồng bộ xưng hô.

### C2. Độ dài

Không ép độ dài bằng mọi giá. Tuy nhiên:

- Tránh câu dài bất thường trong hộp thoại.
- Dùng `<br>` theo giới hạn UI hiện có.
- Không tự thêm tag nếu chưa biết game hỗ trợ.
- Nếu bản dịch dài hơn nhiều, ghi vào QA log để kiểm tra hiển thị.

### C3. Dịch theo lô

Khuyến nghị:

- Hội thoại thường: 20–40 dòng/lô.
- Lore hoặc cảnh thay đổi người nói nhanh: 10–25 dòng/lô.
- H-18 hoặc cảnh cần sắc thái cao: 10–20 dòng/lô.
- Luôn mang theo 5–10 dòng cuối lô trước.

**Điều kiện hoàn tất:** Không có dòng bị thiếu, trùng hoặc chuyển vị.

## Giai đoạn D — QA

Thực hiện theo thứ tự:

1. Structural QA.
2. Terminology QA.
3. Addressing QA.
4. Naturalness QA.
5. Lore QA.
6. H-18 fidelity QA khi có.
7. Diff review.

Không sửa lỗi ngôn ngữ bằng cách làm thay đổi field kỹ thuật.

## Giai đoạn E — Ghi và bàn giao

Bàn giao gồm:

- output;
- diff;
- file manifest;
- glossary cập nhật;
- character registry cập nhật;
- QA log;
- danh sách câu cần người dùng quyết định.

Không đánh dấu “hoàn tất” nếu còn lỗi blocker như sai số cột, mất tag, mất ID hoặc thiếu dòng.
