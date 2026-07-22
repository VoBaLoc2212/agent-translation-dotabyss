# 04. Định dạng file, tag và placeholder

## Nguyên tắc tuyệt đối

Phần kỹ thuật là bất biến. Chỉ dịch field văn bản đã xác định.

Ví dụ dạng dòng:

```text
message,CHARACTER_NAME,DIALOGUE,SCENE_ID,VOICE_ID,CHARACTER_ID
```

Thông thường chỉ `DIALOGUE` được dịch. Tên nhân vật có thể giữ nguyên hoặc được xử lý theo mapping riêng; ID và key không được đổi.

## Delimiter và dấu phẩy

Trước khi dịch phải xác định file có quote field hay không.

### Quy tắc bắt buộc của dự án

Trong các file asset bundle hiện tại, dấu phẩy ASCII `,` được dùng để phân tách field. Vì vậy:

- **Dấu phẩy delimiter giữa các field phải được giữ nguyên tuyệt đối.**
- **Dấu phẩy cần xuất hiện bên trong câu tiếng Việt phải đổi thành dấu `‚` (U+201A).**
- Không thay delimiter `,` thành `‚`.
- Không dùng ký tự `，` full-width thay cho quy tắc này.
- Không tự đổi toàn bộ file bằng Find/Replace mù quáng.
- Chỉ thay dấu phẩy thuộc nội dung field được dịch.

Ví dụ nguồn:

```text
message,A,そうね、でも急ぎましょう,100,voice_01,chara_01
```

Bản dịch đúng:

```text
message,A,Ừ‚ nhưng chúng ta phải nhanh lên,100,voice_01,chara_01
```

Trong ví dụ trên:

- năm dấu phẩy ASCII `,` vẫn là delimiter;
- dấu ngắt câu trong lời thoại được viết bằng `‚`.

### Nếu file là CSV có quote

Nếu một loại file khác được xác nhận là CSV chuẩn có quote field, có thể giữ dấu phẩy ASCII bên trong field theo chuẩn CSV. Tuy nhiên, **đối với pipeline RedirectedResources của dự án này, mặc định vẫn áp dụng quy tắc `,` delimiter và `‚` trong lời dịch**, trừ khi người dùng xác nhận parser khác.

### Kiểm tra sau dịch

Sau mỗi dòng:

1. Đếm số delimiter ASCII `,`.
2. So sánh với dòng nguồn.
3. Kiểm tra không có dấu phẩy ASCII mới trong field tiếng Việt.
4. Kiểm tra ký tự `‚` chỉ xuất hiện trong field dịch, không xuất hiện ở vị trí delimiter.

Không coi file “trông giống CSV” là bằng chứng parser hỗ trợ CSV chuẩn.

## Thành phần phải giữ nguyên

- `message`, key hoặc loại record;
- scene ID;
- line ID;
- voice ID;
- character ID;
- asset key;
- đường dẫn;
- placeholder;
- tag;
- escape sequence;
- mã màu;
- biến nội suy;
- thứ tự field.

## Tag thường gặp

Giữ nguyên cú pháp chính xác:

```text
<br>
<size=80%>
<size\=80%>
<line-height=...>
<align=...>
<color=...>
<b>
<i>
```

Không:

- dịch tên tag;
- đổi `=` thành `\=` hoặc ngược lại nếu nguồn không đổi;
- thêm khoảng trắng vào tag;
- tự đóng/mở tag;
- di chuyển tag qua đoạn văn nếu chưa kiểm tra hiệu ứng.

## Placeholder thường gặp

Giữ nguyên:

```text
%s
%d
{0}
{1}
{name}
${variable}
\n
\r\n
\t
%%
```

Kiểm tra số lần xuất hiện trước và sau dịch. Placeholder có thể đổi vị trí để đúng ngữ pháp tiếng Việt nếu engine hỗ trợ positional placeholders; nếu không chắc, giữ thứ tự.

## Encoding và newline

- Giữ encoding gốc khi có thể.
- Không tự thêm hoặc xóa BOM.
- Giữ CRLF/LF theo nguồn.
- Không normalize Unicode nếu engine nhạy.
- Không đổi ký tự full-width hoặc escape khi chưa hiểu parser.

## Kiểm tra cấu trúc tối thiểu

Với mỗi file:

1. số dòng trước = số dòng sau;
2. số field từng dòng trước = sau;
3. tập ID trước = sau;
4. tổng số tag theo loại trước = sau;
5. tổng số placeholder trước = sau;
6. không có dòng rỗng mới ngoài dự kiến;
7. số dấu phẩy delimiter ASCII `,` trên từng dòng không đổi;
8. không có dấu phẩy ASCII mới trong field tiếng Việt; dấu ngắt bằng phẩy trong lời dịch dùng `‚`;
9. file có thể được parser của dự án đọc.

Nếu một câu dịch cần dấu phẩy nhưng delimiter không cho phép, ưu tiên viết lại câu thay vì phá file.
