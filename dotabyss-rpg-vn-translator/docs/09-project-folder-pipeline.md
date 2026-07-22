# 09. Pipeline thư mục AgentTranslation

## Mục tiêu

Dịch cốt truyện từ tiếng Nhật sang tiếng Việt bằng cách đối chiếu ba nguồn:

1. JP–EN trong `novels`;
2. chuỗi EN thực tế trong asset bundle EN;
3. file output tương ứng trong asset bundle VI.

Tất cả đường dẫn trong skill phải là **đường dẫn tương đối**, không gắn ổ đĩa như `E:` hoặc `D:`. Thư mục làm việc được giả định là thư mục cha chứa `AgentTranslation`.

## Các thư mục bắt buộc phải đọc

```text
AgentTranslation\dotabyss-translation-main\translations\novels
AgentTranslation\Translation\vi
```

Trong đó, các thư mục trọng tâm là:

```text
AgentTranslation\dotabyss-translation-main\translations\novels
AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle
AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle
```

## Vai trò của từng thư mục

### `novels`

Đây là kho cốt truyện có dữ liệu JP và EN. Hermes phải lập chỉ mục toàn bộ file bên trong để biết từng câu tiếng Nhật đã được ánh xạ sang tiếng Anh thế nào.

Ví dụ:

```text
タイトルを設定してください
Please Set a Title.
```

Không cần nhồi toàn bộ kho truyện vào một request. Phải:

1. liệt kê toàn bộ file;
2. tạo index theo tên scene/folder;
3. đọc file tương ứng khi xử lý từng asset;
4. lưu mapping JP → EN → VI vào translation memory.

### Asset bundle EN

```text
AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle
```

Đây là nguồn chứa chuỗi EN thực tế mà game/tool đang dùng. Hermes phải bắt đúng từng chuỗi EN trong file TXT để đối chiếu với EN trong `novels`.

### Asset bundle VI

```text
AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle
```

Đây là output cuối cùng. Không dịch trực tiếp trên file EN. Quy trình là copy file EN sang VI rồi chỉ thay field tiếng Anh tương ứng bằng tiếng Việt.

## Quy trình xử lý một file

Ví dụ:

```text
evs_10200010101.txt
```

### Bước 1 — Xác định file nguồn EN

Tìm:

```text
AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle\evs_10200010101.txt
```

Nếu không có, ghi lỗi vào QA log và không tạo file rỗng.

### Bước 2 — Copy sang output VI

Copy nguyên file sang:

```text
AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle\evs_10200010101.txt
```

Nếu file VI đã tồn tại:

- không ghi đè mù quáng;
- tạo backup hoặc diff;
- chỉ cập nhật các field chưa dịch hoặc được yêu cầu dịch lại.

### Bước 3 — Tìm scene tương ứng trong `novels`

Tìm folder hoặc file có tên tương ứng:

```text
evs_10200010101
```

Dùng tên file không có `.txt` làm khóa tra cứu. Nếu có nhiều kết quả, dùng nội dung EN và ID để phân giải.

### Bước 4 — Xây mapping JP–EN

Đọc nội dung JP và EN trong scene `novels`, tạo mapping:

```text
JP source -> EN reference
```

Mapping phải giữ thứ tự, speaker và context. Không chỉ khớp bằng một câu rời nếu cùng câu EN xuất hiện nhiều lần.

### Bước 5 — Đối chiếu EN

Với từng field EN trong asset bundle:

1. chuẩn hóa chỉ để so khớp tạm thời, không sửa file;
2. tìm câu EN tương ứng trong mapping của `novels`;
3. ưu tiên exact match;
4. nếu không exact match, dùng context, speaker, ID và vị trí;
5. không fuzzy-replace khi có nhiều ứng viên ngang nhau;
6. nếu chưa chắc chắn, giữ nguyên EN và ghi `UNMATCHED`.

### Bước 6 — Dịch JP sang VI

Khi EN asset bundle đã khớp với EN trong `novels`, lấy JP tương ứng làm nguồn chính để dịch sang VI. EN chỉ dùng để đối chiếu và giải nghĩa phụ.

Áp dụng:

- phong cách RPG/visual novel;
- glossary;
- character registry;
- xưng hô;
- lore;
- quy tắc H-18;
- quy tắc dấu phẩy.

### Bước 7 — Thay EN bằng VI

Chỉ thay field EN đã khớp bằng bản VI. Giữ nguyên:

- record type;
- tên nhân vật;
- scene/line ID;
- voice ID;
- character ID;
- tag;
- placeholder;
- delimiter;
- thứ tự dòng.

Trong field tiếng Việt, mọi dấu phẩy ngắt câu phải viết là:

```text
‚
```

Không dùng dấu phẩy ASCII `,` bên trong lời dịch.

### Bước 8 — QA

Kiểm tra:

- file EN và VI có cùng số dòng;
- từng dòng có cùng số delimiter ASCII `,`;
- ID và key không đổi;
- tất cả tag/placeholder còn nguyên;
- các EN đã khớp được thay bằng VI;
- EN chưa khớp vẫn được giữ và có log;
- không có dấu phẩy ASCII mới trong field VI;
- dấu `‚` không thay nhầm delimiter.

## Trạng thái mapping

Mỗi dòng phải có một trạng thái:

- `EXACT`: EN asset = EN novel.
- `CONTEXT_MATCH`: khớp nhờ context/ID/speaker.
- `UNMATCHED`: chưa tìm thấy.
- `AMBIGUOUS`: có nhiều ứng viên.
- `TRANSLATED`: đã điền VI và qua QA.
- `REVIEW`: cần người dùng kiểm tra.

Không tự đánh dấu `TRANSLATED` cho `UNMATCHED` hoặc `AMBIGUOUS`.

## Bảo vệ tool và dữ liệu

RedirectedResources được đặt trong `AgentTranslation` để tách khỏi thư mục game đang chạy. Hermes phải:

- chỉ thao tác trong `AgentTranslation`;
- không truy cập hoặc sửa trực tiếp thư mục cài game thật nếu chưa được phép;
- dùng đường dẫn tương đối;
- không ghi đè file nguồn EN;
- không xóa file VI cũ;
- tạo diff trước khi thay hàng loạt.
