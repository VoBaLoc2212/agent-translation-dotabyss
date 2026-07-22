# Ví dụ minh họa

Các câu dưới đây là ví dụ tự tạo, không phải trích từ game.

## Mặc định anh–em

```text
少女,指揮官、今日も一緒に行こう！=少女,Chỉ Huy, hôm nay anh lại đi cùng em nhé!
主人公,ああ。無理はするなよ。=主人公,Ừ. Nhưng em đừng cố quá nhé.
```

## Cách gọi đặc biệt

Nguồn:

```text
妹役,お兄ちゃん、待ってよ！
```

Không dịch máy móc trước khi biết quan hệ. Hai khả năng:

```text
妹役,Anh hai, chờ em với!
```

hoặc nếu đây là biệt danh nhập vai đã khóa:

```text
妹役,Onii-chan, chờ em với!
```

## Delimiter không quote

Nguồn có sáu field ngăn bởi dấu phẩy và không hỗ trợ quote:

```text
message,A,そうね、でも急ぎましょう,100,voice_01,chara_01
```

Bản dịch không được thêm dấu phẩy trong field thoại. Có thể viết:

```text
message,A,Ừ‚ nhưng chúng ta phải nhanh lên,100,voice_01,chara_01
```

Sau dịch vẫn phải có đúng số field như parser kỳ vọng.


## Quy tắc dấu phẩy chính thức của dự án

Sai:

```text
message,A,Ừ, nhưng chúng ta phải nhanh lên,100,voice_01,chara_01
```

Dấu phẩy sau `Ừ` có thể bị hiểu thành delimiter mới.

Đúng:

```text
message,A,Ừ‚ nhưng chúng ta phải nhanh lên,100,voice_01,chara_01
```

Chỉ dấu phẩy trong lời thoại được đổi thành `‚`; delimiter giữa các field vẫn là `,`.
