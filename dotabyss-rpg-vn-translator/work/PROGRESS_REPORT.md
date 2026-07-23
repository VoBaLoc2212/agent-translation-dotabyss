# Dot Abyss Novel Translation - Progress Report
**Updated**: 2026-07-23

## Workspace
- **Working Dir**: `C:/Users/asaga`
- **Translation Root**: `E:/AgentTranslation/dotabyss-translation-main/translations/novels/`
- **Old TXT Root**: `E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/`
- **Report Dir**: `E:/AgentTranslation/dotabyss-rpg-vn-translator/work/`

## Current Progress
| Metric | Value |
|---|---:|
| Total folders in tracker | 965 |
| `vi.json` currently present on disk | 32 |
| Previously translated `.txt` files | 165 |
| Tracker marked `SKIPPED_OVERLAP` | 165 |
| Tracker marked `COMPLETED` | 9 |
| Tracker marked `PENDING` | 791 |
| Tracker completed-like total (`COMPLETED + SKIPPED_OVERLAP`) | 174 |

## Current State Summary
- Pipeline đang dùng là **dịch trực tiếp `ja.json` -> `vi.json`** cho novels.
- Các scene đã có `.txt` ở pipeline cũ được đánh dấu **`SKIPPED_OVERLAP`** và không cần tạo `vi.json` nữa.
- Đã hoàn thành một đợt **cleanup toàn bộ lỗi nhiễm chữ Hán trong các `vi.json` đã scan**.
- Kết quả audit cuối: **0 file `vi.json` còn nhiễm chữ Hán** trong tập đã quét.

## Key Rules Being Enforced
- `司令官` / `Commander` -> `Chỉ Huy` khi là danh xưng
- `%user%` phải được giữ nguyên
- `<user>` -> `%user%`
- Giữ nguyên `<br>` và tag cấu trúc
- Ưu tiên dấu phẩy fullwidth `，`
- Không dùng Google Translate / DeepL

## Work Completed So Far
1. Cập nhật workflow sang tạo `vi.json` trực tiếp thay vì tiếp tục pipeline `.txt` mới.
2. Tạo tracker cho toàn bộ 965 folder novels.
3. Phân tích overlap và đánh dấu 165 scene là `SKIPPED_OVERLAP`.
4. Tạo và verify các file `vi.json` hiện có trên disk.
5. Quét toàn bộ các `vi.json` đã tạo để tìm lỗi nhiễm chữ Hán.
6. Dịch lại và apply toàn bộ các artifact cleanup để đưa số file nhiễm chữ Hán về **0**.
7. Xóa các file artifact trung gian kiểu `retranslate_task_*`, `residual_han_*`, `build_residual_han_*`, `vi_retranslate_work.json` sau khi đã apply xong.

## Detailed List of Translated Files (`vi.json` currently on disk)
Tổng số file `vi.json` hiện có trên disk: **32**

### EVS (19)
1. `evs_10200010101/vi.json`
2. `evs_10200010201/vi.json`
3. `evs_10200010301/vi.json`
4. `evs_10200010401/vi.json`
5. `evs_10200010501/vi.json`
6. `evs_10200010601/vi.json`
7. `evs_10200010701/vi.json`
8. `evs_10200010801/vi.json`
9. `evs_10200020101/vi.json`
10. `evs_10200020201/vi.json`
11. `evs_10200020301/vi.json`
12. `evs_10200020401/vi.json`
13. `evs_10200020501/vi.json`
14. `evs_10200020601/vi.json`
15. `evs_10200020701/vi.json`
16. `evs_10200020801/vi.json`
17. `evs_10300010101/vi.json`
18. `evs_10300010201/vi.json`
19. `evs_10300010401/vi.json`

### HMN (13)
1. `hmn_10010100001/vi.json`
2. `hmn_10010100002/vi.json`
3. `hmn_10010100003/vi.json`
4. `hmn_10500100001/vi.json`
5. `hmn_10560100001/vi.json`
6. `hmn_10560100002/vi.json`
7. `hmn_10560100003/vi.json`
8. `hmn_10600100003/vi.json`
9. `hmn_10630100001/vi.json`
10. `hmn_10630100002/vi.json`
11. `hmn_10630100003/vi.json`
12. `hmn_10640100001/vi.json`
13. `hmn_10640100002/vi.json`

## Detailed List of Previously Translated TXT Files
Tổng số file `.txt` đã dịch từ pipeline trước: **165**

### EVS (16)
1. `evs_10200010101.txt`
2. `evs_10200010201.txt`
3. `evs_10200010301.txt`
4. `evs_10200010401.txt`
5. `evs_10200010501.txt`
6. `evs_10200010601.txt`
7. `evs_10200010701.txt`
8. `evs_10200010801.txt`
9. `evs_10200020101.txt`
10. `evs_10200020201.txt`
11. `evs_10200020301.txt`
12. `evs_10200020401.txt`
13. `evs_10200020501.txt`
14. `evs_10200020601.txt`
15. `evs_10200020701.txt`
16. `evs_10200020801.txt`

### HMN (149)
1. `hmn_10010100001.txt`
2. `hmn_10010100002.txt`
3. `hmn_10010100003.txt`
4. `hmn_10020100001.txt`
5. `hmn_10020100002.txt`
6. `hmn_10020100003.txt`
7. `hmn_10030100001.txt`
8. `hmn_10030100002.txt`
9. `hmn_10030100003.txt`
10. `hmn_10040100001.txt`
11. `hmn_10040100002.txt`
12. `hmn_10040100003.txt`
13. `hmn_10050100001.txt`
14. `hmn_10050100002.txt`
15. `hmn_10050100003.txt`
16. `hmn_10060100001.txt`
17. `hmn_10060100002.txt`
18. `hmn_10060100003.txt`
19. `hmn_10070100001.txt`
20. `hmn_10070100002.txt`
21. `hmn_10070100003.txt`
22. `hmn_10080100001.txt`
23. `hmn_10080100002.txt`
24. `hmn_10080100003.txt`
25. `hmn_10090100001.txt`
26. `hmn_10090100002.txt`
27. `hmn_10090100003.txt`
28. `hmn_10100100001.txt`
29. `hmn_10100100002.txt`
30. `hmn_10100100003.txt`
31. `hmn_10120100001.txt`
32. `hmn_10120100002.txt`
33. `hmn_10120100003.txt`
34. `hmn_10130100001.txt`
35. `hmn_10130100002.txt`
36. `hmn_10130100003.txt`
37. `hmn_10140100001.txt`
38. `hmn_10140100002.txt`
39. `hmn_10140100003.txt`
40. `hmn_10160100001.txt`
41. `hmn_10160100002.txt`
42. `hmn_10160100003.txt`
43. `hmn_10180100001.txt`
44. `hmn_10180100002.txt`
45. `hmn_10180100003.txt`
46. `hmn_10190100001.txt`
47. `hmn_10190100002.txt`
48. `hmn_10190100003.txt`
49. `hmn_10200100001.txt`
50. `hmn_10200100002.txt`
51. `hmn_10200100003.txt`
52. `hmn_10210100001.txt`
53. `hmn_10210100002.txt`
54. `hmn_10210100003.txt`
55. `hmn_10240100001.txt`
56. `hmn_10240100002.txt`
57. `hmn_10240100003.txt`
58. `hmn_10250100001.txt`
59. `hmn_10250100002.txt`
60. `hmn_10250100003.txt`
61. `hmn_10260100001.txt`
62. `hmn_10260100002.txt`
63. `hmn_10260100003.txt`
64. `hmn_10280100001.txt`
65. `hmn_10280100002.txt`
66. `hmn_10280100003.txt`
67. `hmn_10290100001.txt`
68. `hmn_10290100002.txt`
69. `hmn_10290100003.txt`
70. `hmn_10310100001.txt`
71. `hmn_10310100002.txt`
72. `hmn_10310100003.txt`
73. `hmn_10320100001.txt`
74. `hmn_10320100002.txt`
75. `hmn_10320100003.txt`
76. `hmn_10330100001.txt`
77. `hmn_10330100002.txt`
78. `hmn_10330100003.txt`
79. `hmn_10340100001.txt`
80. `hmn_10340100002.txt`
81. `hmn_10340100003.txt`
82. `hmn_10360100001.txt`
83. `hmn_10360100002.txt`
84. `hmn_10360100003.txt`
85. `hmn_10390100001.txt`
86. `hmn_10390100002.txt`
87. `hmn_10390100003.txt`
88. `hmn_10400100001.txt`
89. `hmn_10400100002.txt`
90. `hmn_10400100003.txt`
91. `hmn_10410100001.txt`
92. `hmn_10410100002.txt`
93. `hmn_10410100003.txt`
94. `hmn_10420100001.txt`
95. `hmn_10420100002.txt`
96. `hmn_10420100003.txt`
97. `hmn_10430100001.txt`
98. `hmn_10430100002.txt`
99. `hmn_10430100003.txt`
100. `hmn_10440100001.txt`
101. `hmn_10440100002.txt`
102. `hmn_10440100003.txt`
103. `hmn_10450100001.txt`
104. `hmn_10450100002.txt`
105. `hmn_10450100003.txt`
106. `hmn_10460100001.txt`
107. `hmn_10460100002.txt`
108. `hmn_10460100003.txt`
109. `hmn_10470100001.txt`
110. `hmn_10470100002.txt`
111. `hmn_10470100003.txt`
112. `hmn_10480100001.txt`
113. `hmn_10480100002.txt`
114. `hmn_10480100003.txt`
115. `hmn_10490100001.txt`
116. `hmn_10490100002.txt`
117. `hmn_10490100003.txt`
118. `hmn_10500100001.txt`
119. `hmn_10500100002.txt`
120. `hmn_10500100003.txt`
121. `hmn_10510100001.txt`
122. `hmn_10510100002.txt`
123. `hmn_10510100003.txt`
124. `hmn_10520100001.txt`
125. `hmn_10520100002.txt`
126. `hmn_10520100003.txt`
127. `hmn_10530100001.txt`
128. `hmn_10530100002.txt`
129. `hmn_10530100003.txt`
130. `hmn_10540100001.txt`
131. `hmn_10540100002.txt`
132. `hmn_10540100003.txt`
133. `hmn_10550100001.txt`
134. `hmn_10550100002.txt`
135. `hmn_10550100003.txt`
136. `hmn_10580100001.txt`
137. `hmn_10580100002.txt`
138. `hmn_10580100003.txt`
139. `hmn_10590100001.txt`
140. `hmn_10590100002.txt`
141. `hmn_10590100003.txt`
142. `hmn_10600100001.txt`
143. `hmn_10600100002.txt`
144. `hmn_10610100001.txt`
145. `hmn_10610100002.txt`
146. `hmn_10610100003.txt`
147. `hmn_10620100001.txt`
148. `hmn_10620100002.txt`
149. `hmn_10620100003.txt`
## Notes
- Danh sách `vi.json` ở trên là các file hiện đang có trên disk trong pipeline novels mới.
- Danh sách `.txt` ở trên là các file đã dịch của pipeline cũ trong `RedirectedResources`.
- `progress_tracker_vi_json.json` vẫn được giữ lại làm **tracker nội bộ** cho tiến trình, không phải file báo cáo cho người đọc.
- File report này là bản Markdown chính cho tiến trình hiện tại.
