# 03. Xưng hô và giọng nhân vật

## Quy tắc nền

Nhân vật chính:

- giới tính: nam;
- vai trò: Commander;
- cách dịch chức danh: **Chỉ Huy**.

Các nhân vật có lời thoại còn lại mặc định là nữ, trừ khi metadata hoặc nguồn chính thức xác nhận khác. Không áp giới tính cho narrator, system message hoặc người nói chưa xác định.

## Ma trận mặc định

| Hướng giao tiếp | Tự xưng | Gọi đối phương |
|---|---|---|
| Nữ → Chỉ Huy, thân mật thông thường | em | anh |
| Chỉ Huy → nữ, thân mật thông thường | anh | em |
| Nữ → Chỉ Huy, trang trọng | tôi/em | Chỉ Huy/anh |
| Chỉ Huy → nữ, trang trọng | tôi/anh | cô/tên nhân vật |
| Nữ ↔ nữ, chưa rõ quan hệ | tôi/mình | cô/cậu/tên |
| Kẻ thù hoặc đối đầu | ta/tôi | ngươi/cô/tên |
| Thần linh/cổ đại | ta | ngươi/con/kẻ… |

Ma trận chỉ là mặc định. Character registry có quyền ghi đè.

## Cách gọi đặc biệt

### Onii-chan / お兄ちゃん

Không tự động giữ nguyên tiếng Nhật.

Chọn theo bối cảnh:

- quan hệ anh em thật hoặc vai trò anh trai: `anh hai`, `anh trai`;
- nũng nịu với Chỉ Huy nhưng không phải anh ruột: `anh ơi`, `anh yêu` hoặc cách gọi riêng đã khóa;
- nếu đây là catchphrase Nhật được người dùng yêu cầu giữ: `Onii-chan`.

Ghi quyết định cố định vào character registry.

### Dan-sama / Danna-sama / 旦那様

Xác định ý nghĩa trong cảnh trước khi dịch:

- quan hệ hôn nhân hoặc nhập vai cổ phong: `phu quân`;
- thân mật hiện đại: `chồng yêu`, `ông xã`;
- cách gọi chủ nhân/khách hàng trong bối cảnh khác: dịch theo chức năng;
- không mặc định dịch thành `ngài`.

### Sama, Master, Lord, Captain và chức danh

Dịch theo vai trò trong thế giới game, không theo từng chữ. Khi chức danh dùng như tên gọi, viết hoa nhất quán.

## Character registry bắt buộc

Mỗi nhân vật quan trọng cần có:

- tên Nhật;
- tên giữ nguyên;
- giới tính;
- vai trò;
- quan hệ với Chỉ Huy;
- tự xưng;
- gọi Chỉ Huy;
- Chỉ Huy gọi lại;
- mức trang trọng;
- catchphrase;
- cách gọi đặc biệt;
- từ không được dùng;
- ví dụ đã duyệt;
- nguồn wiki/file game.

Dùng template:

```text
templates/character-profile.md
```

## Quy tắc thay đổi xưng hô

Xưng hô có thể thay đổi khi:

- quan hệ phát triển;
- nhân vật giận dữ hoặc xa cách;
- nhân vật đóng vai;
- cảnh công khai khác cảnh riêng tư;
- event diễn ra ở timeline khác;
- nhân vật cố tình dùng một biệt danh.

Khi thay đổi, ghi `scene override` thay vì sửa mặc định toàn nhân vật.

## Dòng không rõ người nói

Không tự đoán từ ID nếu chưa có mapping. Thực hiện:

1. đọc các dòng liền trước/sau;
2. kiểm tra voice ID hoặc character ID;
3. tra mapping của dự án;
4. nếu vẫn chưa rõ, giữ đại từ trung tính hoặc đánh dấu QA.

Không dùng anh–em chỉ vì toàn game có một nam chính.
