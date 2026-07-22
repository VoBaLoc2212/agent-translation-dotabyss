# 10. Prompt bắt đầu dịch

## Prompt chính cho Hermes

```text
/dotabyss-rpg-vn-translator

Hãy chú tâm đọc các folder sau:
- AgentTranslation\dotabyss-translation-main\translations\novels
- AgentTranslation\Translation\vi

Đây là hai khu vực dữ liệu liên quan đến bản dịch. Mục tiêu là dịch từ tiếng Nhật sang tiếng Việt.

Trong folder:
AgentTranslation\Translation\vi

có output RedirectedResources tại:
AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle

Đây là nơi đưa ra kết quả cuối cùng.

Nguồn đối chiếu tiếng Anh nằm tại:
AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle

Quy trình thực hiện:

1. Đọc và lập chỉ mục toàn bộ:
   AgentTranslation\dotabyss-translation-main\translations\novels

   Đây là kho cốt truyện có bản JP và EN. Hãy hiểu cách từng câu JP được ánh xạ sang EN.
   Ví dụ:
   タイトルを設定してください
   Please Set a Title.

   Không cần tải toàn bộ file vào một prompt duy nhất. Hãy lập manifest/index và đọc scene tương ứng theo từng file để không mất ngữ cảnh.

2. Đọc:
   AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle

   Hãy bắt đúng từng chuỗi EN trong từng file TXT. Các chuỗi này phải được đối chiếu với phần EN tương ứng trong `novels`.

3. Với mỗi file TXT cần dịch:
   a. Copy file từ asset bundle EN sang:
      AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle

   b. Dùng tên file không có `.txt` để tìm folder/scene tương ứng trong `novels`.
      Ví dụ:
      evs_10200010101.txt
      phải đối chiếu với scene/folder:
      evs_10200010101

   c. Xây mapping JP -> EN từ `novels`.

   d. Đối chiếu từng EN trong asset bundle với EN trong `novels`.
      - Ưu tiên exact match.
      - Nếu cần thì dùng speaker, ID, thứ tự và các dòng lân cận.
      - Nếu trùng khớp, lấy JP tương ứng để dịch sang VI.
      - Sau đó thay đúng field EN trong file đã copy bằng VI.
      - Nếu không chắc chắn, không tự đoán; giữ nguyên EN và ghi vào QA log.

4. Mục tiêu cuối cùng:
   AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle

   phải chứa các file TXT đã được dịch sang tiếng Việt và vẫn giữ nguyên cấu trúc để tool/game đọc được.

Quy tắc dịch:

- Dịch theo phong cách RPG và visual novel.
- Thuần Việt hóa, trừ tên nhân vật.
- Nhân vật chính là nam và là Commander; dịch Commander thành Chỉ Huy.
- Các nhân vật có lời thoại còn lại mặc định là nữ, trừ khi dữ liệu xác nhận khác.
- Mặc định nữ nói với Chỉ Huy dùng em–anh; Chỉ Huy đáp lại dùng anh–em.
- Các cách gọi đặc biệt như onii-chan, danna-sama, biệt danh, chức danh hoặc lối nói cổ phải dựa vào hồ sơ nhân vật và ngữ cảnh.
- Được phép tham khảo https://gamewith.jp/dotabyss/ để xác minh nhân vật và lore.
- JP là nguồn dịch chính; EN là nguồn đối chiếu và hỗ trợ giải nghĩa.
- Giữ nguyên toàn bộ ID, key, voice ID, character ID, tag, placeholder, delimiter, encoding, newline và thứ tự dòng.
- Không dịch hoặc sửa field kỹ thuật.
- Không ghi đè file nguồn EN.
- Chỉ thao tác trong thư mục tương đối `AgentTranslation`; không gắn ổ đĩa như E: hoặc D:.

Quy tắc dấu phẩy bắt buộc:

- Dấu phẩy ASCII `,` giữa các field là delimiter và phải giữ nguyên.
- Mọi dấu phẩy cần dùng bên trong câu tiếng Việt phải thay bằng dấu `‚` (U+201A).
- Không được thêm dấu phẩy ASCII mới vào field tiếng Việt.
- Không được đổi delimiter `,` thành `‚`.

Quy tắc an toàn:

- Nếu file VI đã tồn tại, tạo diff/backup và chỉ cập nhật phần cần thiết.
- Trước khi dịch hàng loạt, chỉ làm thử một file và tối đa 20 dòng liên tiếp.
- Tạo manifest mapping với trạng thái EXACT, CONTEXT_MATCH, UNMATCHED, AMBIGUOUS, TRANSLATED hoặc REVIEW.
- Chạy structural QA và addressing QA.
- Dừng lại để tôi duyệt batch thử trước khi tiếp tục.
- Không hiển thị API key, token Telegram/Discord hoặc nội dung file .env.
```

## Prompt tiếp tục sau khi duyệt batch thử

```text
/dotabyss-rpg-vn-translator

Tiếp tục pipeline AgentTranslation đã được duyệt.

- Chỉ xử lý file/batch chưa hoàn tất trong manifest.
- Dùng JP trong `novels` làm nguồn dịch chính.
- Dùng EN trong `novels` để đối chiếu với EN asset bundle.
- Copy EN sang VI trước rồi chỉ thay field EN đã khớp bằng VI.
- Không ghi đè file nguồn EN.
- Dùng đường dẫn tương đối, không gắn ổ đĩa.
- Trong field tiếng Việt, thay mọi dấu phẩy ngắt câu bằng `‚`.
- Giữ delimiter ASCII `,` giữa các field.
- Không tự dịch dòng UNMATCHED hoặc AMBIGUOUS.
- Mỗi batch phải qua structural QA, terminology QA và addressing QA.
- Sau mỗi 10 batch, báo tiến độ, số dòng EXACT, CONTEXT_MATCH, UNMATCHED, AMBIGUOUS và TRANSLATED.
```
