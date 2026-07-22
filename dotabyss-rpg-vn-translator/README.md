# Dot Abyss RPG/VN Vietnamese Translator

Gói này là một Hermes skill cục bộ dành cho quy trình Việt hóa Dot Abyss theo phong cách RPG và visual novel.

## Cấu trúc

```text
dotabyss-rpg-vn-translator/
├── SKILL.md
├── README.md
├── install.ps1
├── docs/
├── references/
├── templates/
└── examples/
```

## Cài trên Windows

Mở PowerShell tại thư mục này:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

Nếu Hermes Home nằm trên ổ cứng rời:

```powershell
.\install.ps1 -HermesHome "E:\Hermes"
```

Sau đó mở **phiên Hermes mới** và kiểm tra:

```powershell
hermes skills list
hermes chat -q "/dotabyss-rpg-vn-translator Hãy mô tả quy trình dịch."
```

Hermes nạp danh sách skill lúc bắt đầu phiên, vì vậy phiên đang mở trước khi cài có thể chưa nhìn thấy skill.

## Bắt đầu dịch

Sao chép prompt trong:

```text
docs/10-start-translation-prompts.md
```

Trước lần chạy đầu tiên, điền:

- thư mục nguồn;
- thư mục output;
- định dạng file;
- glossary hiện có;
- quy tắc tên nhân vật;
- mức độ cho phép ghi đè.

## Nguyên tắc an toàn

- Mặc định không ghi đè nguồn.
- Không đặt API key, token Telegram/Discord hoặc mật khẩu trong file cần dịch.
- Kiểm tra diff trước khi thay thế file game.

## Quy tắc dấu phẩy của asset bundle

Trong phần lời dịch, không dùng dấu phẩy ASCII `,` vì ký tự đó có thể bị parser hiểu là delimiter. Dùng dấu:

```text
‚
```

Dấu `‚` chỉ thay dấu phẩy trong nội dung lời thoại. Các dấu phẩy ASCII `,` ngăn cách field phải giữ nguyên.

## Pipeline thư mục tương đối

Skill dùng các đường dẫn tương đối dưới thư mục làm việc:

```text
AgentTranslation\dotabyss-translation-main\translations\novels
AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle
AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle
```

Không cần ghi ổ đĩa `E:` hoặc `D:` trong prompt.
