# -*- coding: utf-8 -*-
# Deterministic VI builder for hmn_10200100001.
# Substring-replace exact EN text-field substring with VI translation.
# Preserves delimiters, tags, IDs, empty fields, BOM, CRLF, line count.
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10200100001"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# line_no -> (exact EN text-field substring, VI translation)
# All comma-like pauses use U+201A (‚), never ASCII comma.
MAP = {
    50: ("なんでもできるお姉さん？", "Chị Gái Có Thể Làm Được Mọi Thứ?"),
    59: ("The sounds of fierce battle echoed through the forest. A battle was<br>underway to intercept the monsters closing in on the Frontline Base.<br> ",
         "Tiếng giao tranh ác liệt vang vọng khắp khu rừng. Một trận chiến đang<br>diễn ra để chặn đứng lũ quái vật đang tiến sát Căn Cứ Tiền Tuyến.<br> "),
    98: ("GUOOOOOH!!<br> ", "GÀOOOOO!!<br> "),
    161: ("No! The monster went that way! Someone，stop it!<br> ",
          "Không được! Con quái vật chạy về phía đó rồi! Ai đó‚ ngăn nó lại đi!<br> "),
    208: ("Nooo! I can't reach it!<br> ", "Không được! Em không với tới được!<br> "),
    247: ("Verisa，run!<br> ", "Verisa‚ chạy đi!<br> "),
    283: ("Huh...?!<br> ", "Hả...?!<br> "),
    287: ("Just as Verisa was focusing to unleash a spell，a monster slipped<br>through the formation and attacked her.<br> ",
          "Ngay khi Verisa đang tập trung để thi triển phép thuật‚ một con quái vật đã<br>lách qua đội hình và tấn công cô ấy.<br> "),
    291: ("GUOOOOOH!!<br> ", "GÀOOOOO!!<br> "),
    304: ("Aaaah!<br> ", "Áaaa!<br> "),
    333: ("Just as the monster was about to take Verisa's life，Laveria threw<br>herself in front of her and blocked the deadly strike.<br> ",
          "Ngay khoảnh khắc con quái vật sắp đoạt mạng Verisa‚ Laveria đã lao<br>ra đỨ trước mặt cô ấy và chặn đứng nhát chém chết người đó.<br> "),
    337: ("You're not getting past me! Fall back，Verisa，now!<br> ",
          "Không ai lọt qua được ta đâu! Lùi lại đi‚ Verisa‚ mau!<br> "),
    364: ("Honey! Looks like Laveria saved little Verisa from a tight spot!<br> ",
          "Phu quân! Có vẻ như Laveria đã cứu bé Verisa thoát khỏi tình cảnh ngặt nghèo rồi đó!<br> "),
    379: ("Great job，Laveria! While she's holding them off，let's regroup!<br> ",
          "Làm tốt lắm‚ Laveria! Trong lúc cô ấy cầm chân bọn chúng‚ ta cùng tái chiến đấu!<br> "),
    381: ("Stay calm and reform the formation! Provide cover for Laveria...<br>cover...?<br> ",
          "Bình tĩnh và tái lập đội hình! Hãy yểm trợ cho Laveria...<br>yểm trợ...?<br> "),
    411: ("Is that all you've got! You dare challenge me! *pant*!<br> ",
          "Chỉ có thế thôi à! Ngươi dám thách thức ta sao! *thở dốc*!<br> "),
    441: ("With every swing of her greatsword，Laveria thinned the horde.<br> ",
          "Với mỗi nhát chém đại kiếm‚ Laveria đã làm thưa bớt đám quái vật.<br> "),
    489: ("*roar*...<br> ", "*gầm rú*...<br> "),
    538: ("Wow... she's beating them all!<br> ", "Wow... chị ấy đánh bại hết cả đám rồi!<br> "),
    541: ("No kidding... She's not just holding them off，she's charging ahead!<br> ",
          "Đúng thiệt... chị ấy không chỉ cầm chân chúng‚ mà còn xông lên phía trước!<br> "),
    562: ("I'm taking them all! Stop me if you can!<br> ",
          "Ta sẽ quét sạch tất cả! Cản ta lại nếu các ngươi có thể!<br> "),
    631: ("Gyaoooooo...<br> ", "Gào...<br> "),
    640: ("Wait，wait，wait! Are you trying to take them all down by yourself?<br> ",
          "Khoan‚ khoan‚ khoan! Em định một mình hạ gục hết bọn chúng sao?<br> "),
    642: ("Everyone，provide covering fire! Hurry before Laveria finishes them<br>all!<br> ",
          "Mọi người‚ hãy yểm trợ hỏa lực! Nhanh lên kẻo Laveria dọn dẹp hết<br>bọn chúng mất!<br> "),
    670: ("*phew*... no sign of any more enemies.<br> ",
          "*hà*... không còn dấu hiệu của thêm kẻ địch nào.<br> "),
    672: ("Good work，Laveria. That was incredible.<br> ",
          "Làm tốt lắm‚ Laveria. Thật phi thường.<br> "),
    684: ("No，I failed. I got a little too into it and overdid it.<br> ",
          "Không‚ em đã thất bại. Em hơi bốc quá nên làm lố mất rồi.<br> "),
    688: ("I never said not to take them out yourself. If you can take them out，<br>that's fine by me.<br> ",
          "Ta đâu có bảo em đừng tự mình hạ chúng. Nếu em hạ được thì<br>cứ việc‚ ta không phiền.<br> "),
    690: ("You also covered Verisa in time. Thanks to you，she didn't get hurt.<br> ",
          "Em còn kịp yểm trợ cho Verisa nữa. Nhờ có em‚ cô ấy đã không bị thương.<br> "),
    698: ("So Verisa's safe too. That's good.<br> ", "Vậy Verisa cũng an toàn rồi. Tốt quá.<br> "),
    739: ("I was soooo scared! Thank youuu，Laveria!<br> ",
          "Em sợ phát khiếp luôn! Cảm ơn chị nhiều lắm‚ Laveria!<br> "),
    761: ("Brother ordered me to cover you. If you're going to thank anyone，<br>thank him.<br> ",
          "Anh đã ra lệnh cho em yểm trợ cho em ấy. Nếu em muốn cảm ơn ai thì<br>cảm ơn anh ấy đi.<br> "),
    791: ("Ehh，it's only natural for Mister to help me，right? I mean，isn't it his<br>fault his command was so sloppy?<br> ",
          "Ê‚ đương nhiên là anh phải giúp em rồi‚ đúng không? Ý em là‚ lỗi của<br>anh ấy chỉ huy lỏng lẻo thế kia mà?<br> "),
    793: ("Oh come on... I even had reserves ready. That's no way to talk to me.<br>Fine，reflecting on today，I'll give you close-combat training.<br> ",
          "Ôi thôi nào... anh còn chuẩn bị cả quân dự bị cơ mà. Nói thế với anh không<br>được đâu. Được rồi‚ suy ngẫm từ hôm nay‚ anh sẽ cho em huấn luyện cận chiến.<br> "),
    803: ("Wh-WHAA? Why do I have to do that?<br> ", "Ể-Ểeee? Tại sao em phải làm chuyện đó?<br> "),
    805: ("If you were a magic knight who could handle both ranges，it wouldn't<br>be a problem，right? As commander，I can't ignore a weakness.<br> ",
          "Nếu em là một hiệp sĩ pháp sư cân được cả tầm xa lẫn tầm gần thì đâu có<br>thành vấn đề‚ đúng không? Làm chỉ huy‚ anh không thể làm ngơ trước một điểm yếu.<br> "),
    816: ("Umm，I think girls are cuter when they have a little flaw，don't you<br>think?<br> ",
          "Ưm‚ em nghĩ con gái có một chút khuyết điểm thì mới dễ thương‚ anh<br>thấy có phải không?<br> "),
    818: ("Don't call yourself cute! You should aim to be an all-rounder like<br>Laveria!<br> ",
          "Đừng tự nhận mình dễ thương! Em nên phấn đấu thành người đa năng như<br>Laveria!<br> "),
    857: ("...Flaws make you cuter，huh.<br> ", "...Khuyết điểm khiến em dễ thương hơn‚ à.<br> "),
    888: ("Laveria，is something wrong?<br> ", "Laveria‚ có chuyện gì sao?<br> "),
    908: ("No，nothing. The battle's over. Let's head back to base.<br> ",
          "Không‚ không có gì. Trận chiến đã kết thúc. Chúng ta về căn cứ thôi.<br> "),
    917: ("Yeah，let's go home.<br> ", "Ừ‚ về nhà thôi.<br> "),
    930: ("Right. Doesn't look like there'll be any more monster attacks... Kill<br>count: 13 goblins.<br> ",
          "Đúng. Có vẻ sẽ không có thêm đợt tấn công quái vật nào nữa... Số lượng<br>tiêu diệt: 13 yêu tinh.<br> "),
    953: ("You keep records every time like that? Being a commander is a tough<br>job，Brother.<br> ",
          "Anh ghi chép mỗi lần như thế sao? Làm chỉ huy đúng là một công việc vất<br>vả‚ anh.<br> "),
    955: ("I need to compile these reports or I can't plan the next operation.<br>Actually，they've been piling up... I don't wanna go back.<br> ",
          "Anh cần tổng hợp mấy báo cáo này không thì không thể lên kế hoạch chiến<br>dịch tiếp theo. Thực ra‚ chúng nó chất đống cả rồi... anh chẳng muốn quay về tí nào.<br> "),
    1006: ("Piles of unprocessed documents，one after another! We're<br>shorthanded，completely shorthanded!<br> ",
           "Núi giấy tờ chưa xử lý chất đống‚ lớp này đến lớp khác! Chúng ta thiếu<br>nhân lực‚ thiếu nhân lực trầm trọng!<br> "),
    1035: ("We've had so many operations lately that the reports haven't been<br>able to keep up，I'm afraid...<br> ",
           "Dạo này công tác tác chiến nhiều quá nên báo cáo không kịp theo kịp‚ em<br>e ngại lắm...<br> "),
    1054: ("Alicia，help me with these too. Damn，isn't there anyone else good at<br>paperwork?<br> ",
           "Alicia‚ giúp anh mấy cái này nữa đi. Khỉ thật‚ sao không có ai khác giỏi<br>vụ giấy tờ nhỉ?<br> "),
    1073: ("It's a lot for just me to handle... and everyone who might be able to<br>help is out right now...<br> ",
           "Một mình em xử lý số này thì quá sức... mà ai có thể giúp thì giờ đều<br>đang đi vắng hết...<br> "),
    1077: ("Argh! Isn't there anyone who can handle both paperwork and combat!<br>And if she's a beauty，even better!<br> ",
           "Chết tiệt! Sao chẳng có ai vừa giỏi giấy tờ vừa chiến đấu được chứ!<br>Mà nếu là mỹ nữ thì càng tốt!<br> "),
    1108: ("C-Commander! Get a hold of yourself! I can't tell if you're losing your<br>mind or just being your usual self!<br> ",
           "C-Chỉ Huy! Xin ngài trấn tĩnh lại! Em không rõ là ngài đang phát<br>điên hay chỉ là bản thân ngài bình thường!<br> "),
    1114: ("As if this is normal for me! Damn，this is the kind of situation where<br>I'd take any help I can get...<br> ",
           "Làm gì có chuyện bình thường cho anh thế này! Khỉ thật‚ đây đúng là tình<br>cảnh mà anh sẽ nhận bất cứ giúp đỨ nào có thể...<br> "),
    1139: ("Brother，got a minute?<br> ", "Anh ơi‚ rảnh một chút không?<br> "),
    1155: ("Oh，Laveria? Sure，what's up?<br> ", "Ồ‚ Laveria à? Được thôi‚ có chuyện gì?<br> "),
    1182: ("Sorry to interrupt when you're busy. There was a report from the<br>reconnaissance unit that went to the Abyss.<br> ",
           "Xin lỗi vì làm gián đoạn khi anh đang bận. Có báo cáo từ đội trinh sát<br>được cử đi Đại Huyệt.<br> "),
    1184: ("Oh，I heard about it. You came to deliver it yourself，Laveria?<br> ",
           "Ồ‚ anh nghe rồi. Em tự mang đến tận nơi báo cáo sao‚ Laveria?<br> "),
    1192: ("And to see your face while I was at it.<br> ", "Và nhân tiện ghé thăm anh luôn.<br> "),
    1217: ("As for the Abyss，there's been nothing unusual since the last<br>operation.<br> ",
           "Còn về Đại Huyệt‚ kể từ chiến dịch lần trước đến giờ không có gì bất<br>thường.<br> "),
    1219: ("I see，that's a relief. But there's still a lot we don't know about the<br>Abyss，so we need to stay on alert for any sudden activity.<br> ",
           "Anh hiểu‚ thật nhẹ nhõm. Nhưng vẫn còn nhiều điều chúng ta chưa rõ về<br>Đại Huyệt‚ nên cần cảnh giác với mọi hoạt động đột xuất.<br> "),
    1226: ("That's why you look so tired，Brother—because you're always on<br>guard for so many things.<br> ",
           "Đó là lý do trông anh mệt mỏi thế đấy‚ anh—vì anh lúc nào cũng cảnh<br>giác với quá nhiều chuyện.<br> "),
    1228: ("...Was my tired expression that obvious?<br> ", "...Biểu cảm mệt mỏi của anh lộ rõ đến thế sao?<br> "),
    1236: ("I'm good at looking after my comrades. Believe it or not，I'm someone<br>people rely on in Lux Nova.<br> ",
           "Em giỏi chăm sóc đồng đội mà. Tin hay không thì‚ em cũng là người mà<br>mọi người ở Lux Nova luôn tin cậy.<br> "),
    1239: ("I see，so you're like a big sister to them. Well，I'm just busy with<br>paperwork. Nothing to worry about.<br> ",
           "Anh hiểu‚ ra em như một người chị cả với bọn họ. À‚ anh chỉ đang bận<br>với mấy vụ giấy tờ thôi. Không có gì đáng lo.<br> "),
    1272: ("Yes，if we get through these next few days，we'll be fine. Let's work<br>hard together，Commander...!<br> ",
           "Vâng‚ nếu chúng ta vượt qua được mấy ngày tới thì sẽ ổn thôi. Cùng nhau<br>cố gắng nhé‚ Chỉ Huy...!<br> "),
    1276: ("*sigh*... it's going to take days just to process the paperwork!<br> ",
           "*thở dài*... chỉ riêng xử lý mấy tờ giấy này cũng mất cả mấy ngày!<br> "),
    1286: ("I-I'll help as much as I can! Let's sort through them little by little!<br> ",
           "E-em sẽ giúp hết sức mình! Chúng ta cùng dọn dẹp chúng từng chút một nhé!<br> "),
    1310: ("Hmm，what's got you in trouble? If it's something I'm allowed to<br>know，tell me about it.<br> ",
           "Ừm‚ chuyện gì làm anh rắc rối vậy? Nếu là chuyện em được phép<br>biết thì kể cho em nghe đi.<br> "),
    1347: ("Actually，we've got a backlog of formal operation reports that need<br>to go to each country... Only the Commander can handle these.<br> ",
           "Thực ra‚ chúng em đang tồn đọng một đống báo cáo chiến dịch chính thức cần<br>gửi sang từng quốc gia... Chỉ có Chỉ Huy mới xử lý được mấy cái này.<br> "),
    1358: ("Since we're receiving supplies，funds，and military support，we need<br>to share accurate information with them...<br> ",
           "Bởi vì chúng ta đang nhận vật tư‚ tiền bạc‚ và viện trợ quân sự nên cần<br>chia sẻ thông tin chính xác với họ...<br> "),
    1361: ("We don't need to fudge the content this time，so I could just report it<br>as-is... but...<br> ",
           "Lần này không cần làm mờ nội dung đâu‚ nên anh cứ báo cáo y nguyên<br>như thế... nhưng mà...<br> "),
    1377: ("All the people who are good with this kind of paperwork are out in<br>the field... The thought of having to do all this alone... *sigh*<br> ",
           "Tất cả những người giỏi vụ giấy tờ này đều đang đi ngoài tiền tuyến hết<br>rồi... Nghĩ đến chuyện phải một mình làm hết đống này... *thở dài*<br> "),
    1415: ("I see... I've got an idea of someone who could help.<br> ",
           "Em hiểu... em đã nghĩ ra một người có thể giúp được.<br> "),
    1418: ("Really? Who? What unit are they from?<br> ", "Thật sao? Là ai? Thuộc đơn vị nào?<br> "),
    1446: ("Fufu，it's me. Before I came here，I did office work. These kinds of<br>reports are a piece of cake.<br> ",
           "Hì hì‚ là em chứ ai. Trước khi đến đây‚ em làm công việc văn phòng. Mấy<br>báo cáo kiểu này với em thì dễ như trở bàn tay.<br> "),
    1456: ("Bingo! A beauty who can fight and handle paperwork，right here!<br> ",
           "Trúng phóc! Một mỹ nữ vừa biết đánh vừa giỏi giấy tờ‚ ngay tại đây!<br> "),
    1467: ("B-beauty?<br> ", "C-cái gì‚ mỹ nữ?<br> "),
    1475: ("Wh-what... Brother，you're saying that again...<br> ", "Ơ... anh lại nói thế nữa à...<br> "),
    1477: ("Secure her，Alicia! Prepare tea and sweets! Don't let her escape!<br> ",
           "Bắt giữ cô ấy‚ Alicia! Chuẩn bị trà và bánh ngọt đi! Tuyệt đối đừng để cô ấy trốn thoát!<br> "),
    1514: ("Yes，Commander! But are you sure it's okay，Laveria?<br> ",
           "Vâng‚ Chỉ Huy! Nhưng ngài chắc chắn ổn chứ‚ Laveria?<br> "),
    1525: ("It's fine. I'm planning to stay here for a while anyway. I'll help if<br>you're in a bind.<br> ",
           "Không sao. Em định ở lại đây một thời gian rồi. Nếu anh túng thiếu<br>thì em sẽ giúp.<br> "),
    1538: ("We really appreciate it，but if you have other things to do at the<br>Frontline Base，please prioritize those，okay?<br> ",
           "Bọn em thực lòng biết ơn‚ nhưng nếu chị có việc khác ở Căn Cứ Tiền Tuyến<br>thì cứ ưu tiên việc đó nhé‚ được không?<br> "),
    1547: ("Business...? Nothing，really. Just a whim，I suppose.<br> ",
           "Công việc à...? Không có gì‚ thật sự. Chỉ là một cơn bốc đồng thôi‚ em nghĩ vậy.<br> "),
    1552: ("Then I'm begging you! Help us out right now! With just Alicia and me，<br>we'll end up working all night!<br> ",
           "Thế thì anh van em đấy! Giúp anh ngay bây giờ đi! Chỉ có một mình Alicia<br>và anh thôi‚ thế nào cũng làm xuyên đêm mất!<br> "),
    1557: ("Alright，alright，I get it. Then Alicia，just pass me the documents I'm<br>allowed to see，okay?<br> ",
           "Được rồi‚ được rồi‚ em hiểu rồi. Thế thì Alicia‚ cứ đưa em những tờ giấy<br>em được phép xem thôi nhé‚ được không?<br> "),
    1567: ("Of course! We're counting on you，Laveria!<br> ",
           "Tất nhiên rồi! Bọn em trông cậy vào chị đấy‚ Laveria!<br> "),
}


def main():
    for ln, (old, vi) in MAP.items():
        assert "," not in vi, f"ASCII comma in VI for line {ln}: use U+201A ‚"
    data = EN.read_bytes()
    text = data.decode("utf-8-sig")
    lines = text.splitlines(True)

    out, translated = [], 0
    for idx, line in enumerate(lines, 1):
        if idx in MAP:
            old, vi = MAP[idx]
            assert old in line, f"EN key not found on line {idx}:\n{line!r}"
            new = line.replace(old, vi, 1)
            assert new != line, f"no change on line {idx}"
            out.append(new)
            translated += 1
        else:
            out.append(line)

    out_bytes = ("\ufeff" + "".join(out)).encode("utf-8")
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(out_bytes)
    print(f"translated {translated}/{len(lines)} lines -> {VI}")


if __name__ == "__main__":
    main()
