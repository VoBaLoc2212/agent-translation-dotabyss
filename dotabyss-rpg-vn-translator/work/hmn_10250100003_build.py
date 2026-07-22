#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI output for hmn_10250100003 (EN-asset-is-English case).

Strategy: EN text field is authoritative for structure (BOM, CRLF, <br> counts,
fullwidth ，commas, speaker labels, trailing technical fields). We translate each
text field EN->VI and replace only parts[2] (or parts[1] for title) per line,
keeping every delimiter / technical byte identical.
"""
import io

ROOT = "E:/AgentTranslation"
EN = f"{ROOT}/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10250100003.txt"
VI_OUT = f"{ROOT}/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10250100003.txt"

# line_no (1-based, matching the asset) -> VI text field (incl. <br> suffix)
# Addressing matrix:
#   Wendy(ウェンディ)=em / Chỉ Huy ; Verisa(ベリサ)=chị(tự xưng)/anh ơi(おにーさん) ;
#   Veera(ヴィーラ)=em / chị ; Commander(<user>)=anh ; お姉ちゃん=Sis->chị ơi / Big Sis->chị lớn
VI_MAP = {
    23:  'Chiến Công Của Wendy Giữa Biển Lửa',
    36:  'RẦM!<br> ',
    61:  'Một tiếng nổ kinh hoàng bỗng vọng tới tai Wendy đang ngủ. Cô ấy<br>bàng hoàng tỉnh dậy trong hoảng loạn.<br> ',
    78:  'C-cái gì，cái gì，cái gì! Cái rung chấn khổng lồ này là sao!?<br> ',
    89:  'Không lẽ... Tiền Tuyến Căn Cứ đang bị tập kích!? Chỉ Huy<br>có thể đang gặp nguy hiểm!<br> ',
    100: 'Khẩn cấp xuất kích! Chỉ Huy，hãy đợi em nhé!<br> ',
    133: 'Chết... phải làm sao đây...<br> ',
    164: 'Chỉ Huy! Ngài không sao chứ!?<br> ',
    166: 'Wendy? Sao em lại ở đây?<br> ',
    177: 'Em nghe một tiếng nổ cực lớn! Em lo không biết có chuyện gì xảy ra với<br>ngài，Chỉ Huy...<br> ',
    179: 'Như ngài thấy đấy，anh vẫn khỏe như bình thường.<br> ',
    190: 'Ôi，may quá...<br> ',
    201: 'Nhưng mà，nguyên nhân vụ nổ lúc nãy là do đâu...?<br> ',
    203: 'Hình như có vụ nổ xảy ra bên trong xưởng chế tác.<br> ',
    205: 'May thay，lúc đó chưa tới giờ đi làm nên không có nhân viên nào bị<br>thương，nhưng...<br> ',
    207: 'Anh nhận được báo cáo rằng Verisa và Veera，những người đang thí<br>nghiệm bên trong，đã bị mắc kẹt trong xưởng.<br> ',
    218: 'Verisa và Veera!? T-thật là tồi tệ!<br> ',
    245: '(Nghĩ lại thì，hôm qua họ có nói là sẽ làm thí<br>nghiệm trong xưởng mà...!)<br> ',
    271: 'Hai người họ có an toàn không!?<br> ',
    273: 'Anh không rõ. Anh định đi cứu họ，nhưng lửa cháy quá<br>dữ khiến anh bất lực...<br> ',
    275: 'Anh đã gọi mọi người và họ đang chuẩn bị cứu hộ. Anh chỉ mong<br>họ bình an...<br> ',
    286: 'Mất bao lâu nữa!?<br> ',
    288: 'Anh phải chuẩn bị đồ chịu nhiệt và dụng cụ chữa cháy. Sớm nhất thì<br>cũng mất mười phút.<br> ',
    299: 'Chậm quá! Xin hãy để em đi cứu họ!<br> ',
    308: 'Em nắm rõ cấu trúc bên trong xưởng，lại chẳng hề ngại lửa!<br> ',
    310: 'Em nói cái gì vậy! Anh không thể để em làm thế! Nếu có chuyện gì xảy ra với<br>em thì sao!<br> ',
    319: 'Verisa và Veera là những người bạn thân quý của em! Vì thế em mới muốn đi cứu<br>họ!<br> ',
    321: 'Chết... công tác chuẩn bị vẫn mất thời gian... Thôi được. Anh giao phó cho em đấy，Wendy.<br> ',
    330: 'Vâng! Em nhất định sẽ cứu được họ!<br> ',
    358: 'Wendy đã đến xưởng đang bốc cháy. Cô bắt đầu tìm kiếm<br>Verisa và Veera giữa biển lửa.<br> ',
    389: 'Lửa đã lan rộng tới mức này rồi...!<br> ',
    400: 'Cơ sở xưởng đã hỏng hoàn toàn vì vụ nổ... Chắc là nhiên liệu<br>đã bị bắt lửa...!<br> ',
    423: 'Em phải tìm thấy họ nhanh! Verisa! Veera! Hai người ở đâu!<br> ',
    432: 'Là em，Wendy! Em tới cứu rồi! Mau trả lời em đi!<br> ',
    464: 'Ưm! Ở đây này!',
    506: '...! Em tưởng mình nghe thấy tiếng nói từ phía đó...!<br> ',
    517: 'Không lẽ... Verisa! Veera! Hai người ở trong đó sao!<br> ',
    536: 'Đợi đó! Em sẽ kéo hai người ra...!<br> ',
    581: 'Gh... băng của em đang tan...! Ma lực cũng sắp cạn kiệt rồi...!<br> ',
    590: 'Tránh ra đi，Veera! Đám lửa tẻo tẻo này để ma pháp của chị<br>xử lý...!<br> ',
    602: 'Chị đánh lửa bằng lửa thì có ích gì đâu!<br> ',
    613: 'Chết... ư，vậy thì chúng ta phải làm sao!<br> ',
    656: 'Verisa! Veera ơi!',
    708: 'Giọng nói đó... không thể nào...!<br> ',
    762: 'Tìm thấy rồi! Hai người có an toàn không!?<br> ',
    828: 'Wendy! Em làm gì ở đây thế?<br> ',
    835: 'Em tới cứu hai người rồi!<br> ',
    844: 'Đ-đồ ngốc! Đồ ngốc!<br> ',
    855: 'Em biết nguy hiểm thế nào mà vẫn xông vào...!<br> ',
    866: 'Em là một búp bê tự động nên không sao cả!<br> ',
    877: 'Thấy chưa? Dù giữa lửa ngọn，em vẫn bình yên vô sự!<br> ',
    890: 'Nhưng quan trọng hơn，mau ra khỏi đây thôi! Lâu nữa chúng ta sẽ<br>thành than mất!<br> ',
    901: 'Thế nhưng，làm sao ra ngoài được? Lửa đã chặn mất hết các<br>lối thoát...<br> ',
    912: 'Cứ giao cho em! Em sẽ phá tường chui ra ngoài!<br> ',
    924: 'Lùi lại chút nha! Em sợ vung kiếm trúng hai người!<br> ',
    993: '*hừ*... Aaaaaah!<br> ',
    1046: '*rầm!*<br> ',
    1048: 'Wendy vung đại kiếm，đập tan bức tường xưởng. Một lỗ hổng<br>khổng lồ mở ra，và ngọn lửa cuồn cuộn phún ra ngoài cùng không khí.<br> ',
    1087: 'Thành công rồi! Mau ra khỏi đây thôi!<br> ',
    1149: 'Em... em điên thật sự đấy，biết không...<br> ',
    1160: 'Cả hai，bám lấy em nhé! Em sẽ xông thẳng qua biển lửa!<br> ',
    1171: 'Hả? Xông thẳng qua á...?<br> ',
    1215: 'Lên nào! Oa!<br> ',
    1246: 'Này，nhanh quá... Iyyy!<br> ',
    1308: '*phù*! Thoát thành công!<br> ',
    1373: '*ực*... Đầu em quay cuồng... em thấy buồn nôn...<br> ',
    1384: 'Ah，cảm ơn em，Wendy. Em đã cứu bọn chị...<br> ',
    1395: 'Em mừng quá hai người đều bình an!<br> ',
    1406: '...Ôi chao，em đầy than đen thế kìa.<br> ',
    1418: 'Để chị lau mặt cho em... này. Quay lại đây nào.<br> ',
    1487: '*ùm!*<br> ',
    1512: 'Xong rồi đấy... Thiệt tình，em bất cẩn thật sự.<br> ',
    1539: 'Nhưng nhờ em mà bọn chị được cứu! Cảm ơn em!♪<br> ',
    1587: 'Ủa? Chị ơi，chị có thể thật lòng với Wendy đến thế cơ à? Chị nên đối xử với<br>Chỉ Huy như vậy mới phải...<br> ',
    1653: 'C-chuyện đó bây giờ chẳng liên quan!<br> ',
    1670: 'Dù sao đi nữa! Chị nợ Wendy một lần cứu mạng. Chị không phải kiểu để món nợ<br>mãi chưa trả đâu，nên...<br> ',
    1681: 'Có chuyện gì cứ nói với chị. Chị sẽ dùng ma pháp giúp em<br>đấy!♪<br> ',
    1692: 'Vâng! Hư hư. Em nên xin chị điều gì nhỉ~♪<br> ',
    1706: '...Nhưng mà chị đang tính báo cáo gì với Chỉ Huy đây，chị<br>ơi?<br> ',
    1717: 'Làm sao chị dám nói rằng chị，vì ngủ mớ，đã lỡ tay làm sai sức mạnh ma pháp và<br>thổi bay cả cơ sở chứ...<br> ',
    1767: 'Khỏi lo! Chị cứ nói đại cái gì đó nghe có lý với anh ơi rồi lấp liếm là xong<br>thôi!<br> ',
    1779: 'Anh ơi lúc nào cũng chiều chuộng em mà.<br> ',
    1790: 'Nếu em khóc lóc bảo là em sợ hãi，chắc chắn anh ơi sẽ tha thứ cho em thôi!<br> ',
    1794: 'Hơ. Đó là một câu đùa thú vị đấy.<br> ',
    1870: 'A-anh ơi! Từ bao giờ anh ở đó rồi...?<br> ',
    1872: 'Từ khoảnh khắc Wendy bục ra khỏi xưởng ấy.<br> ',
    1916: 'Làm tốt lắm，Wendy. Em đã rất cố gắng.<br> ',
    1927: 'Cảm ơn ngài，Chỉ Huy!<br> ',
    1929: 'Nhân sự và trang bị đã tập hợp đủ. Bên trong không còn ai cần cứu hộ<br>nên công tác chữa cháy sớm xong thôi.<br> ',
    1940: 'Nghe vậy em mừng quá!<br> ',
    1942: 'Giờ chỉ cần tìm nguyên nhân thôi. Anh định hỏi Verisa và mọi người cho<br>chi tiết vì họ có mặt ở hiện trường...<br> ',
    1997: 'Nhưng có vẻ việc đó không cần thiết nữa.<br> ',
    2008: 'Ư，ưm，cái đó... a，em không biết gì hết!<br> ',
    2024: 'Ai mà thả em đi được?<br> ',
    2072: 'Íi... L-lui ra đi~!<br> ',
    2074: 'Veera. Để anh mượn đứa nhóc này một lát.<br> ',
    2128: 'Vâng! Anh cứ tự nhiên!♪<br> ',
    2139: 'Veera! Mau giúp chị với chứ!<br> ',
    2150: 'Lần này tại chị là người có lỗi，nên đành chịu thôi.<br> ',
    2152: 'Đúng thế. Nào，đi thôi.<br> ',
    2163: 'Khôôông! Wendy，cứu chị với~!<br> ',
    2218: 'A，ahaha...<br> ',
    2272: 'Wendy，sau này làm ơn dỗ dành chị lớn giúp chị nhé.<br> ',
    2283: 'Chị chắc chắn chị ấy sẽ về trong nước mắt thôi.<br> ',
    2292: 'Ư，ừ! Bọn em là bạn mà. Phải động viên chị ấy chứ!<br> ',
    2337: 'Nhưng được ở riêng với Chỉ Huy... em hơi ghen tị với<br>Verisa đấy!<br> ',
    2348: 'Biết đâu nếu em trở thành một cô gái hư hỏng hơn chút nữa，em sẽ thu<br>hút được sự chú ý của Chỉ Huy...<br> ',
}

def main():
    raw = open(EN, 'rb').read()
    assert raw[:3] == b'\xef\xbb\xbf', "EN missing BOM"
    has_crlf = b'\r\n' in raw
    text = raw.decode('utf-8-sig')
    lines = text.split('\n')
    # strip trailing '' from final newline
    if lines and lines[-1] == '':
        lines = lines[:-1]

    en_text_fields = {}
    out_lines = []
    for i, line in enumerate(lines, 1):
        s = line.rstrip('\r')
        is_title = s.startswith('title,')
        is_msg = s.startswith(('message,', 'messageTextUnder,', 'messageTextCenter,'))
        if is_title:
            parts = s.split(',', 1)
            en_text_fields[i] = parts[1]
            if i in VI_MAP:
                parts[1] = VI_MAP[i]
            out_lines.append(','.join(parts))
        elif is_msg:
            # parts: cmd,label,text,trailing...  (text has no ASCII comma)
            parts = s.split(',')
            en_text_fields[i] = parts[2]
            if i in VI_MAP:
                parts[2] = VI_MAP[i]
            out_lines.append(','.join(parts))
        else:
            out_lines.append(s)

    # ---- structural assertions ----
    errors = []
    for ln, vi in VI_MAP.items():
        # no ASCII comma allowed inside VI text field
        if ',' in vi:
            errors.append(f"ASCII_COMMA in line {ln}: {vi!r}")
        # <br> count must match EN text field
        en_tf = en_text_fields.get(ln, '')
        if en_tf.count('<br>') != vi.count('<br>'):
            errors.append(f"BR_COUNT line {ln}: en={en_tf.count('<br>')} vi={vi.count('<br>')}  en={en_tf!r} vi={vi!r}")
    if errors:
        print("BUILD ERRORS:")
        for e in errors:
            print("  ", e)
        raise SystemExit(1)

    # rebuild bytes preserving CRLF + BOM
    body = '\r\n'.join(out_lines)
    if has_crlf:
        body += '\r\n'
    out_bytes = b'\xef\xbb\xbf' + body.encode('utf-8')
    with open(VI_OUT, 'wb') as f:
        f.write(out_bytes)
    print(f"Wrote {VI_OUT}")
    print(f"lines={len(out_lines)} crlf={has_crlf} bom=True translated_records={len(VI_MAP)}")

if __name__ == '__main__':
    main()
