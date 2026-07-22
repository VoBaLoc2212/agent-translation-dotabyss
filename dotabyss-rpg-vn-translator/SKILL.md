---
name: dotabyss-rpg-vn-translator
description: Use when translating Dot Abyss game text into Vietnamese.
version: 1.0.0
author: Local User
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [gaming, translation, japanese, vietnamese, rpg, visual-novel]
    related_skills: []
---

# Dot Abyss RPG/VN Vietnamese Translator

## Overview

Dùng skill này để dịch nội dung game Dot Abyss từ tiếng Nhật hoặc tiếng Anh sang tiếng Việt theo phong cách RPG kết hợp visual novel. Bản dịch phải tự nhiên, thuần Việt, nhất quán nhân vật và không phá cấu trúc file game.

Tên riêng của nhân vật được giữ nguyên theo glossary của dự án. Nhân vật chính là nam, giữ vai trò **Commander**, dịch thống nhất là **Chỉ Huy**. Các nhân vật có lời thoại còn lại mặc định là nữ, trừ khi dữ liệu dự án chứng minh khác.

## When to Use

Kích hoạt skill khi người dùng yêu cầu:

- Dịch cốt truyện, sự kiện, hội thoại, mô tả hoặc cảnh H-18 của Dot Abyss.
- Dịch file trong thư mục BepInEx Translation hoặc asset text tương tự.
- Kiểm tra, hiệu đính hoặc đồng bộ cách xưng hô trong bản dịch.
- Nghiên cứu nhân vật trên GameWith để cải thiện giọng văn và quan hệ nhân vật.

## Mandatory Reading Order

Trước khi dịch, đọc các tài liệu sau theo thứ tự:

1. `${HERMES_SKILL_DIR}/docs/01-translation-workflow.md`
2. `${HERMES_SKILL_DIR}/docs/02-vietnamese-style-guide.md`
3. `${HERMES_SKILL_DIR}/docs/03-character-addressing.md`
4. `${HERMES_SKILL_DIR}/docs/04-file-format-and-tags.md`
5. `${HERMES_SKILL_DIR}/docs/05-wiki-research.md`
6. `${HERMES_SKILL_DIR}/docs/06-h18-scenes.md`
7. `${HERMES_SKILL_DIR}/docs/07-quality-assurance.md`
8. `${HERMES_SKILL_DIR}/docs/08-nemotron-free-workflow.md`
9. `${HERMES_SKILL_DIR}/docs/09-project-folder-pipeline.md`
10. `${HERMES_SKILL_DIR}/docs/10-start-translation-prompts.md`

Chỉ đọc thêm template hoặc ví dụ khi cần. Không bỏ qua tài liệu định dạng file.

## Non-Negotiable Rules

1. **Không dịch tên nhân vật** trừ khi glossary dự án chỉ định cách viết chính thức.
2. **Commander → Chỉ Huy** trong toàn bộ nội dung.
3. **Mặc định nữ ↔ Chỉ Huy dùng em–anh / anh–em**, nhưng hồ sơ nhân vật và ngữ cảnh có quyền ghi đè.
4. Không tự động biến mọi cách gọi đặc biệt thành anh–em. Các cách gọi như `onii-chan`, `danna-sama`, chức danh, biệt danh hoặc lối nói cổ phải được xử lý theo hồ sơ nhân vật.
5. Không thêm, bớt hoặc đảo ý. Có thể tái cấu trúc câu để tiếng Việt tự nhiên nhưng phải giữ thông tin, cảm xúc, mức độ thân mật và hàm ý.
6. Không phá delimiter, số cột, ID, tag, placeholder, mã điều khiển, xuống dòng hoặc encoding của file. Với file dùng dấu phẩy ASCII `,` làm delimiter mà không quote field, mọi dấu phẩy cần dùng bên trong câu tiếng Việt phải đổi thành dấu `‚` (U+201A); tuyệt đối không đổi các dấu phẩy delimiter giữa các field.
7. Không ghi đè file nguồn nếu người dùng chưa cho phép. Mặc định ghi vào thư mục staging/output.
8. GameWith là nguồn tham khảo phụ. File game và ngữ cảnh cốt truyện hiện tại là nguồn chính.
9. Không bịa thông tin nhân vật khi wiki không có hoặc mâu thuẫn với game.
10. Với nội dung H-18, dịch trung thành về sắc thái và mức độ trực diện; không tự làm thô hơn, không tự làm nhẹ đi.
11. Với dự án AgentTranslation, dùng đường dẫn tương đối, không ghi ổ đĩa như `E:` hoặc `D:`:
    - `AgentTranslation\dotabyss-translation-main\translations\novels`
    - `AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle`
    - `AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle`
12. Thư mục `novels` là nguồn đối chiếu JP–EN; asset bundle EN là nguồn để bắt đúng chuỗi EN; asset bundle VI là output cuối.

13. Chỉ xử lý nội dung tình dục khi nhân vật được xác định rõ là người trưởng thành. Nếu tuổi không rõ hoặc có dấu hiệu vị thành niên, dừng phần đó và báo người dùng.
14. Khi thiếu ngữ cảnh ảnh hưởng đến xưng hô, đánh dấu `[[CẦN NGỮ CẢNH]]` trong bản nháp hoặc ghi vào QA log; không đoán chắc chắn.

## Translation Procedure

1. **Khảo sát đầu vào**
   - Liệt kê file, định dạng, encoding, newline và delimiter.
   - Xác định field nào được phép dịch.
   - Hoàn tất khi có manifest file và quy tắc cấu trúc rõ ràng.

2. **Nạp ngữ cảnh**
   - Đọc glossary, character registry, các dòng trước/sau và bản dịch cũ nếu có.
   - Hoàn tất khi xác định được người nói, người nghe và mục đích cảnh cho từng cụm.

3. **Nghiên cứu có chọn lọc**
   - Tra GameWith bằng đúng tên Nhật của nhân vật khi giọng nói, vai trò hoặc quan hệ chưa rõ.
   - Ghi URL và ngày truy cập vào research log.
   - Hoàn tất khi mọi kết luận dùng để dịch đều có nguồn hoặc được đánh dấu là suy luận.

4. **Dịch theo lô nhỏ**
   - Áp dụng glossary và addressing matrix.
   - Giữ nguyên mọi thành phần kỹ thuật.
   - Hoàn tất khi số dòng đầu ra bằng số dòng đầu vào và mọi field không dịch vẫn byte-equivalent nếu có thể.

5. **Tự kiểm tra**
   - Thực hiện structural QA, linguistic QA, character voice QA và lore QA.
   - Hoàn tất khi không còn lỗi blocker trong checklist.

6. **Ghi kết quả**
   - Ghi vào staging/output hoặc patch theo yêu cầu.
   - Tạo diff và summary; không ghi đè nguồn ngoài phạm vi được cho phép.
   - Hoàn tất khi mọi file sửa đổi được liệt kê và có thể khôi phục.

7. **Cập nhật bộ nhớ dự án**
   - Cập nhật glossary, character registry, translation memory và QA log.
   - Hoàn tất khi các quyết định mới có ví dụ và nguồn ngữ cảnh.

## Output Contract

Khi người dùng yêu cầu dịch file:

- Chỉ thay đổi phần văn bản được phép dịch.
- Không thêm giải thích vào file game.
- Báo cáo ngoài file gồm:
  - số file và số dòng đã dịch;
  - các dòng bị bỏ qua;
  - các điểm cần người dùng quyết định;
  - lỗi cấu trúc hoặc tag;
  - đường dẫn output/diff.

Khi người dùng yêu cầu bản dịch trực tiếp trong chat, ưu tiên định dạng:

```text
Tiếng Nhật=Tiếng Việt
```

trừ khi họ chỉ định định dạng khác.

## Common Pitfalls

- Dịch từng dòng độc lập khiến đại từ thay đổi liên tục.
- Dùng dấu phẩy trong field không được quote làm tăng số cột.
- Dịch nhầm ID, voice key, character key hoặc tag.
- Giữ nguyên trật tự câu tiếng Nhật khiến tiếng Việt cứng và tối nghĩa.
- Lạm dụng “ngươi”, “ta”, “cô”, “tôi” cho mọi nhân vật.
- Biến `onii-chan` thành một cách gọi cố định mà không xét quan hệ.
- Tin tuyệt đối vào wiki dù file game mới hơn.
- Gửi lô quá lớn cho model miễn phí và mất nhất quán ở cuối lô.

## Verification Checklist

- [ ] Đã đọc đủ tài liệu bắt buộc.
- [ ] Đã xác định field được dịch và delimiter.
- [ ] Tên nhân vật được giữ nguyên.
- [ ] Commander được dịch là Chỉ Huy.
- [ ] Xưng hô đúng character registry và ngữ cảnh.
- [ ] Tag, placeholder, ID, voice key và số cột không đổi.
- [ ] Số dòng đầu ra bằng số dòng đầu vào, trừ khi có lý do được ghi log.
- [ ] Không có thêm lời giải thích trong file game.
- [ ] Cảnh H-18 không bị tăng/giảm mức độ so với nguồn.
- [ ] Đã tạo diff, QA log và danh sách điểm chưa chắc chắn.
