# 05. Tra cứu GameWith và quản lý lore

## Nguồn tham khảo

Trang chính:

```text
https://gamewith.jp/dotabyss/
```

Danh sách nhân vật:

```text
https://gamewith.jp/dotabyss/563116
```

Danh sách sự kiện:

```text
https://gamewith.jp/dotabyss/561389
```

Hướng dẫn main story:

```text
https://gamewith.jp/dotabyss/561672
```

## Mục đích tra cứu

GameWith được dùng để xác nhận:

- tên Nhật chính thức;
- vai trò;
- thuộc tính;
- stance;
- vũ khí;
- mô tả tính cách;
- kỹ năng hoặc motif;
- event xuất hiện;
- thông tin có ích cho giọng nói.

Không dùng xếp hạng sức mạnh làm căn cứ dịch tính cách.

## Quy trình tra một nhân vật

1. Lấy tên Nhật chính xác từ file game.
2. Tìm trong trang danh sách nhân vật.
3. Mở trang riêng của nhân vật.
4. Ghi lại dữ kiện liên quan trực tiếp đến câu đang dịch.
5. Ghi URL và ngày truy cập.
6. So sánh với file game.
7. Nếu mâu thuẫn, ưu tiên nội dung game của scene hiện tại và ghi QA note.

## Quy tắc chống bịa

- Không suy ra tính cách chỉ từ ngoại hình.
- Không suy ra quan hệ tình cảm chỉ từ costume hoặc banner.
- Không coi gameplay role là vai trò cốt truyện.
- Không suy ra tuổi.
- Không lấy comment người dùng làm dữ kiện chính thức.
- Không dùng machine translation của trang làm câu dịch cuối.

## Research log

Mỗi mục nên có:

```text
Nhân vật:
Tên Nhật:
URL:
Ngày truy cập:
Dữ kiện dùng:
Dòng/cảnh áp dụng:
Mức tin cậy: cao / vừa / thấp
Ghi chú mâu thuẫn:
```

## Khi không truy cập được wiki

Tiếp tục bằng:

1. file game;
2. character registry;
3. translation memory;
4. ngữ cảnh lân cận.

Gắn `[[CẦN XÁC NHẬN LORE]]` trong QA log, không chèn tag này vào file đầu ra chính thức.
