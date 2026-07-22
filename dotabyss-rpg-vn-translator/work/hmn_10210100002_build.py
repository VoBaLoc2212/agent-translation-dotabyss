#!/usr/bin/env python
# Build VI asset for hmn_10210100002 via exact-field substring replacement.
import io, sys

EN = r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10210100002.txt"
OUT = r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10210100002.txt"

# Title case Vietnamese title (Title Case per rules)
TITLE_VI = "Humena Đang Bị Truy Đuổi!!"

# Mapping: original exact EN text field -> Vietnamese text field.
# Internal commas use U+201A (‚). <br> tokens preserved exactly.
M = {
"ヒュメナ逃走中！！": TITLE_VI,
"No Abyss exploration scheduled，no monster sighting reports. For a<br>Frontline Base，this is a peaceful day.<br> ":
"Không có kế hoạch thám hiểm Đại Huyệt‚ cũng chẳng có báo cáo bắt gặp quái vật. Với một<br>Căn Cứ Tiền Tuyến‚ đây đúng là một ngày yên bình.<br> ",
"Ahh... I've been working nonstop lately，so today I'll just laze around<br>and enjoy this peace.<br> ":
"Ahh... dạo này tôi làm việc liên tục không nghỉ‚ nên hôm nay cứ thong thả<br>tận hưởng sự bình yên này thôi.<br> ",
"Commander!<br> ":"Chỉ Huy!<br> ",
"...A short-lived peace. What's wrong，Humena? You seem so<br>panicked...<br> ":
"...Một khoảng bình yên ngắn ngủi. Sao thế‚ Humena? Em trông hoảng loạn<br>thế kia...<br> ",
"I'm being chased! Please，help me!<br> ":"Em bị truy đuổi rồi! Làm ơn‚ cứu em với!<br> ",
"Who's chasing you? Don't tell me it's monsters!<br> ":"Ai đang đuổi em? Đừng nói với tôi là quái vật nhé!<br> ",
"No! Soldiers and martial artists!<br> ":"Không! Là lính và mấy người võ thuật!<br> ",
"...Why is that? Did you challenge a dojo and make enemies or<br>something?<br> ":
"...Tại sao lại thế? Hay là em đã tấn công một võ đường và sinh ra thù<br>chuốc oán hay gì đó?<br> ",
"I didn't do anything like that! L-look! We did that tile breaking<br>together the other day，right?<br> ":
"Em đâu có làm chuyện đó! N-nhìn này! Hôm trước mình đã cùng nhau bẻ ngói<br>mà‚ phải không?<br> ",
"Yeah，the one where you broke a hundred tiles，Humena.<br> ":
"Ừ‚ lần em đập vỡ một trăm viên ngói đấy‚ Humena.<br> ",
"Do you remember what I said after breaking them?<br> ":"Anh có nhớ điều em nói sau khi bẻ xong không?<br> ",
"Fufufu! This is the power of my water spirit!<br> ":"Fufufu! Đây là sức mạnh của tinh linh nước của em đấy!<br> ",
"I think I recall you saying something like that. So what about it?<br> ":
"Tôi nghĩ mình có nhớ em nói đại loại thế. Thế thì sao?<br> ",
"Actually，everyone who heard that got the wrong idea—they thought<br>they could become strong with the blessing of the water spirit，Upachan!<br> ":
"Thật ra‚ ai nghe thấy điều đó cũng hiểu lầm—họ nghĩ mình sẽ trở nên mạnh<br>mẽ nhờ vào sự phù hộ của tinh linh nước‚ Upa-chan!<br> ",
"And so they're all chasing me，demanding \"\"Hand over the water<br>spirit!\"\"<br> ":
"Thế là tất cả bọn họ đuổi theo em‚ đòi \"\"Giao con tinh linh nước ra!<br>\"\"<br> ",
"Huh! That's ridiculous—! Ah，no，I can't say that for sure.<br> ":
"Hử! Nực cười làm sao—! Á‚ không‚ tôi cũng chẳng dám chắc.<br> ",
"It's hard to believe that power came from Humena's slender arms. It's<br>almost more natural to think it's a spirit's blessing.<br> ":
"Khó tin nổi sức mạnh ấy lại phát ra từ đôi tay mảnh khảnh của Humena. Hầu như<br>tự nhiên hơn nếu nghĩ đó là sự phù hộ của tinh linh.<br> ",
"Ugh... I only said that because I've been training with a powerful<br>water spirit，but they don't have a blessing like that...<br> ":
"Ưgh... em chỉ nói vậy vì đã cùng luyện tập với một tinh linh nước<br>mạnh mẽ‚ chứ bọn họ chẳng có sự phù hộ đó đâu...<br> ",
"Did you explain that to them? That there's no special blessing?<br> ":
"Em có giải thích cho họ không? Là không hề có sự phù hộ đặc biệt nào?<br> ",
"I tried，but they won't listen... They're just chasing me to take<br>Upachan away!<br> ":
"Em có nói rồi‚ nhưng họ không chịu nghe... Bọn họ chỉ đuổi theo để cướp<br>lấy Upa-chan thôi!<br> ",
"Man，those guys... They're probably so fixated on using the spirit's<br>blessing to make a big splash.<br> ":
"Thật tình‚ bọn đó... Chắc chúng quá chấp niệm dùng sự phù hộ của tinh linh<br>để tạo tiếng vang lớn.<br> ",
"What am I gonna do! Everyone's looking for me，and my room's being<br>watched—I've got nowhere to run! It's so terrible!<br> ":
"Em phải làm sao đây! Ai cũng đang tìm em‚ và phòng của em thì bị<br>canh chừng—em không còn chỗ nào để trốn! Tồi tệ quá!<br> ",
"...Alright，I'll hide you，Humena.<br> ":
"...Được rồi‚ để tôi giấu em‚ Humena.<br> ",
"Huh...? A-Are you sure?<br> ":"Hử...? A-Anh chắc chứ?<br> ",
"Yeah. Even if I'm a lousy commander，I'm still the Commander. I'm kind<br>of Humena's boss，so I can't just leave her，right?<br> ":
"Ừ. Dù tôi có tệ hại thì vẫn là Chỉ Huy. Tôi cũng giống như<br>cấp trên của Humena‚ nên không thể mặc kệ em được‚ đúng không?<br> ",
"C-Commander...! Thank youuu! I knew it，you're such a good boy! I'll<br>stick with you forever!<br> ":
"C-Chỉ Huy...! Cảm ơn anh nhiều! Biết ngay mà‚ anh đúng là một đứa ngoan! Em sẽ<br>ở bên anh mãi mãi!<br> ",
"You're exaggerating... And quit calling me a good boy.<br> ":
"Em phóng đại quá... Và đừng gọi tôi là đứa ngoan nữa.<br> ",
"Anyway，let's move. Soldiers might come here，so I think it's best if<br>you hide in my room for now.<br> ":
"Thôi thì‚ mình di chuyển thôi. Lính có thể tới đây‚ nên tôi nghĩ tốt nhất là<br>em trốn trong phòng tôi một lúc.<br> ",
"Go to the living quarters? But there are people after Upa all over the<br>base，you know?<br> ":
"Đi đến ký túc xá sao? Nhưng khắp căn cứ đều có người đang truy đuổi Upa<br>mà‚ anh biết mà?<br> ",
"Don't worry. I'm the Commander of this Frontline Base. Leave<br>everything inside the base to me.<br> ":
"Đừng lo. Tôi là Chỉ Huy của Căn Cứ Tiền Tuyến này. Mọi việc trong căn cứ<br>cứ giao cho tôi.<br> ",
"This way，let's hurry!<br> ":"Lối này‚ mau lên!<br> ",
"Hey，hey，Commander. We're just walking normally，so how come we<br>haven't run into anyone?<br> ":
"Này‚ này‚ Chỉ Huy. Chúng ta chỉ đi bộ bình thường thôi‚ sao lại chẳng<br>gặp ai cả?<br> ",
"This is a kind of back route off the main corridors that connect the<br>facilities. Only people who really know the base use it.<br> ":
"Đây là một lối đi phụ tách xa hành lang chính nối các khu<br>nhà. Chỉ những ai thực sự rành căn cứ mới đi lối này.<br> ",
"I see! Way to go，Commander!<br> ":"Ra thế! Giỏi quá‚ Chỉ Huy!<br> ",
"That said，we were bound to run into someone... Tch，and there they<br>are.<br> ":
"Thế nhưng‚ sớm muộn cũng gặp người... Chết tiệt‚ bọn họ ở đó<br>rồi.<br> ",
"Tch，where did that Spirit go...?<br> ":"Chết tiệt‚ con tinh linh đó đi đâu mất rồi...?<br> ",
"Eek，it's the soldier that's after Upa! Wh-what do we do?<br> ":
"Ái‚ là tên lính đang truy đuổi Upa kìa! C-chúng ta làm sao đây?<br> ",
"No problem. Just watch—he'll be here soon.<br> ":"Không sao. Cứ xem đi—anh ta sẽ tới sớm thôi.<br> ",
"He's coming...? Ah!<br> ":"Anh ấy tới...? Á!<br> ",
"What are you doing? What about your duties?<br> ":"Anh đang làm gì thế? Nhiệm vụ của anh đâu rồi?<br> ",
"Ah... M-my apologies! I'll head back right away.<br> ":"Á... T-tôi xin lỗi! Tôi sẽ quay lại ngay.<br> ",
"Honestly... don't slack off too much.<br> ":"Thật tình... đừng lười biếng quá.<br> ",
"Whoa，he's gone. Who was that?<br> ":"Whoa‚ anh ấy đi rồi. Người đó là ai vậy?<br> ",
"We're short on personnel，so he's a senior soldier assigned to patrol<br>just during this time. We can get through safely now.<br> ":
"Chúng ta thiếu nhân lực‚ nên anh ấy là lính cấp cao được điều đi tuần tra<br>chỉ trong khung giờ này. Giờ chúng ta đi qua an toàn rồi.<br> ",
"Amazing. You even know stuff like that. As expected of Commander.<br>You're a good boy and a capable one too. I'll stick with you forever!<br> ":
"Tuyệt quá. Anh còn biết cả những thứ như vậy. Đúng là Chỉ Huy có khác.<br>Anh vừa là đứa ngoan vừa có năng lực nữa. Em sẽ ở bên anh mãi mãi!<br> ",
"You're exaggerating again... and don't treat me like a kid... *sigh*，<br>whatever. Come on，let's head to my room while it's clear.<br> ":
"Em lại phóng đại rồi... và đừng coi tôi như trẻ con... *thở dài*‚<br>thôi kệ đi. Nào‚ tranh thủ lúc vắng vẻ mình vào phòng tôi.<br> ",
"Coming in. So this is Commander's room!<br> ":"Em vào nhé. Thế này là phòng của Chỉ Huy sao!<br> ",
"I'll take care of things so you can move around freely. Just relax until<br>then.<br> ":
"Tôi sẽ sắp xếp mọi thứ để em có thể đi lại tự do. Cứ nghỉ ngơi cho đến<br>lúc đó.<br> ",
"U-um，thank you...<br> ":"U-um‚ cảm ơn anh...<br> ",
"(Come to think of it，this is my first time in a man's room. It has some<br>unfamiliar scent...)<br> ":
"(Nghĩ mới nhớ‚ đây là lần đầu em vào phòng của một người đàn ông. Có một mùi<br>hương lạ lẫm...)<br> ",
"(Is this what a man smells like? Or is it Commander's...?)<br> ":
"(Đây là mùi của đàn ông sao? Hay là của Chỉ Huy...?)<br> ",
"Humena? You're spacing out，are you okay?<br> ":"Humena? Em đang thẫn thờ‚ có ổn không?<br> ",
"Hyaah! Ah，y-yeah. I'm fine. I guess I just relaxed a bit now that we're<br>somewhere safe. Ahaha.<br> ":
"Hyaah! Á‚ ư-ừ. Em ổn mà. Chắc tại vừa tới chỗ an toàn nên em hơi lơi lỏng<br>ra. Ahaha.<br> ",
"Don't worry about it. There's no chance of soldiers finding us here...<br>even if they do，I'll send them packing.<br> ":
"Đừng bận tâm. Ở đây lính không thể tìm ra chúng ta đâu...<br>mà có tìm ra‚ tôi cũng sẽ đuổi họ đi.<br> ",
"Yeah... you're really dependable，Commander.<br> ":"Ừ... anh thật sự rất đáng tin cậy‚ Chỉ Huy.<br> ",
"But I feel bad for always relying on you... Oh，I know. Let me treat<br>you to my specialty dish as thanks!<br> ":
"Nhưng em thấy áy náy vì cứ dựa dẫm vào anh... Ồ‚ em biết rồi. Để em đãi<br>anh món đặc sản của em như lời cảm ơn!<br> ",
"Oh，really?<br> ":"Ồ‚ thật sao?<br> ",
"Yeah，I'll just borrow your kitchen for a bit!<br> ":"Ừ‚ để em mượn bếp của anh một lát!<br> ",
"Here you go! Humena's homemade meatball paradise.<br> ":"Của em đây! Thiên đường viên thịt tự làm của Humena.<br> ",
"Oh，uh... well，there's no doubt it looks delicious... but aren't they<br>kinda small? If you're gonna heap them up，bigger ones might...<br> ":
"Ồ‚ ưm... ừ thì‚ trông ngon là cái chắc... nhưng sao chúng hơi<br>nhỏ thế? Nếu chất đống thì những viên to hơn chắc sẽ...<br> ",
"Upa and the others like this size! Their mouths are small，so it's easy<br>for them to eat! I'm sure you'll like them too，Commander!<br> ":
"Upa và các bạn thích cỡ này! Miệng bọn họ nhỏ‚ nên ăn rất dễ!<br>Em chắc anh cũng thích chúng‚ Chỉ Huy!<br> ",
"But I'm a human!<br> ":"Nhưng tôi là con người mà!<br> ",
"Since you went out of your way to make them，I'll have one，but—<br> ":
"Vì em đã cất công làm‚ tôi sẽ nếm một viên‚ nhưng—<br> ",
"I picked up a dumpling and put it in my mouth. The flavor and texture<br>were unique，but the taste was surprisingly good.<br> ":
"Tôi nhặt một viên thịt viên bỏ vào miệng. Hương vị và kết cấu có phần<br>độc đáo‚ nhưng vị lại ngon bất ngờ.<br> ",
"Oh，this is pretty good!<br> ":"Ồ‚ cũng ngon đấy!<br> ",
"Fufufu! It's my pride and joy!♪<br> ":"Fufufu! Đây là tác phẩm tự hào của em!♪<br> ",
"Upa!<br> ":"Upa ơi!<br> ",
"Yeah，Upa can eat too.<br>Here you go.<br> ":
"Ừ‚ Upa cũng ăn được.<br>Của em đây.<br> ",
"Upaa!<br> ":"Upaa ơi!<br> ",
"You sure are enjoying that.<br> ":"Em thưởng thức ra phết đấy.<br> ",
"Upaaa!<br> ":"Upaaa ơi!<br> ",
"～～～～♪":"Ùm ùm~♪",
"Hey，a lot of them are coming out!<br> ":"Này‚ có rất nhiều con đang bơi ra!<br> ",
"There are other spirits living in the aquarium besides Upa. Thanks to<br>the church's secret arts，this aquarium is actually a very spacious area.<br> ":
"Ngoài Upa còn có những tinh linh khác sống trong bể cá. Nhờ vào<br>bí thuật của giáo hội‚ bể cá này thực chất là một không gian rất rộng.<br> ",
"Huh，so it's a comfortable place for spirits to live.<br> ":"Hử‚ ra là nơi ở thoải mái cho các tinh linh.<br> ",
"Yeah... but even so，it can't beat nature.<br>So I take them to the sea sometimes and let them swim freely，but...<br> ":
"Ừ... nhưng dù vậy‚ vẫn không bằng thiên nhiên.<br>Nên thi thoảng em đưa bọn họ ra biển để bơi tự do‚ nhưng...<br> ",
"I want to take them to the sea soon，but it's difficult now.<br>I'm troubled... I need to resolve this soon for Upa and the others.<br> ":
"Em muốn sớm đưa bọn họ ra biển‚ nhưng hiện tại rất khó.<br>Em đang rối... cần giải quyết chuyện này sớm vì Upa và các bạn.<br> ",
"(She's thinking about Upa and the others more than herself...<br>Heh，who's the good one here?)<br> ":
"(Cô ấy đang nghĩ về Upa và các bạn nhiều hơn bản thân mình...<br>Hừm‚ rốt cuộc ai mới là người ngoan ở đây?)<br> ",
"You guys don't worry，okay? I'll definitely sort things out.<br>Come on，eat up.<br> ":
"Các em đừng lo‚ được không? Tôi nhất định sẽ lo xong chuyện này.<br>Nào‚ ăn đi.<br> ",
"Upaa!♪<br> ":"Upaa ơi!♪<br> ",
"Ah，they're eating the food you gave them!<br>Water spirits only eat from people they trust!<br> ":
"Á‚ bọn họ đang ăn thức ăn anh cho!<br>Tinh linh nước chỉ ăn từ người chúng tin tưởng!<br> ",
"They realize you're protecting them. You've earned their trust，<br>Commander.<br> ":
"Bọn họ nhận ra anh đang bảo vệ mình. Anh đã giành được sự tin tưởng<br>của họ‚ Chỉ Huy.<br> ",
"Getting chummy with spirits isn't a bad feeling. But even if water<br>spirits warm up to me，it's not like they make me stronger...<br> ":
"Kết thân với tinh linh cũng không tệ. Nhưng dù các tinh linh nước<br>có thân thiết với tôi‚ cũng chẳng khiến tôi mạnh lên...<br> ",
"No，that's it! This might just work!<br> ":"Không‚ là nó rồi! Cách này có thể thành công!<br> ",
"What is it，Commander? Did you think of something?<br> ":"Là gì thế‚ Chỉ Huy? Anh nảy ra ý tưởng gì sao?<br> ",
"Yeah，I've got a good plan. Humena，will you help me out?<br> ":"Ừ‚ tôi có kế hoạch hay. Humena‚ em sẽ giúp tôi chứ?<br> ",
"Of course! If there's anything I can do，just say the word!<br> ":"Tất nhiên! Có gì em làm được‚ cứ bảo nhé!<br> ",
"Then，Humena... hit me!<br> ":"Thế thì‚ Humena... đánh anh đi!<br> ",
"Ehhh，wh-what?<br> ":"Ehhh‚ c-cái gì?<br> ",
}

def split_text_field(line):
    # returns (prefix_with_2nd_comma, textfield, suffix_starting_with_comma) or None
    if line.startswith("title,"):
        c = line.index(",", 1) if "," in line[1:] else -1
        # title has only one field after comma
        c = line.index(",")
        prefix = line[:c+1]
        text = line[c+1:]
        return prefix, text, ""
    if line.startswith("message,"):
        c1 = line.index(",")
        c2 = line.index(",", c1+1)
        prefix = line[:c2+1]
        rest = line[c2+1:]
        # text field has no ASCII comma; it ends at next comma if one exists
        if "," in rest:
            nc = rest.index(",")
            text = rest[:nc]
            suffix = rest[nc:]
        else:
            text = rest
            suffix = ""
        return prefix, text, suffix
    return None

raw = open(EN, "rb").read()
text = raw.decode("utf-8-sig")
has_crlf = b"\r\n" in raw
lines = text.split("\n")
# drop trailing empty from final newline
if lines and lines[-1] == "":
    lines = lines[:-1]

out_lines = []
hits = 0
for line in lines:
    l = line.rstrip("\r")
    key = split_text_field(l)
    if key is None:
        out_lines.append(l)
        continue
    prefix, textf, suffix = key
    if textf in M:
        out_lines.append(prefix + M[textf] + suffix)
        hits += 1
        # guard: no ASCII comma in VI text field
        if "," in M[textf]:
            raise SystemExit(f"ASCII comma in VI text field for: {textf!r}")
    else:
        # text-field line but not in map -> keep original (should not happen for text cmds)
        out_lines.append(l)

print("translated text fields:", hits, "of", len(M))
assert hits == len(M), f"Expected {len(M)} hits, got {hits}"

result = "\r\n".join(out_lines) + "\r\n"
data = b"\xef\xbb\xbf" + result.encode("utf-8")
open(OUT, "wb").write(data)
print("WROTE", OUT, "bytes:", len(data))
