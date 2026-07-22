import os
import json

# Full translation dictionary: EN asset text -> VI translation
VI = {
    # Title
    "くすんだ石ころ": "Viên Đá Nhòe",
    
    # MessageTextCenter
    "<size=48>—A few months later.</size>": "<size=48>—Vài Tháng Sau</size>",
    
    # Messages
    "There was a knock at the door.<br> ": "Có tiếng gõ cửa.<br> ",
    "Come in.<br> ": "Vào đi.<br> ",
    "Yes! Pardon the intrusion!<br> ": "Vâng! Phiền rắc chút ạ!<br> ",
    "So you're the volunteer who arrived today.<br> ": "Ngươi là tân binh vừa đến hôm nay à.<br> ",
    "Yes! I am Betty of Milesgard!<br> ": "Vâng! Em là Betty từ Milesgard ạ!<br> ",
    "Haha, you're a lively one. I heard you requested assignment to the<br>Frontline Base—why's that?<br> ": "Haha, nhỏ này nhiệt tình đấy. Nghe nói ngươi xin về Căn Cứ Tiền Tuyến, tại sao vậy?<br> ",
    "Yes! My family has been knights for generations. Since childhood, I've<br>witnessed my father and brother's heroic deeds on the battlefield!<br> ": "Vâng! Gia gia em đời đời quân nhân, từ nhỏ em đã chứng kiến cha anh em anh oai phong trên chiến trường!<br> ",
    "That's why my goal is to become a great soldier like my father and<br>brother, and to make a name for myself!<br> ": "Vì thế mục tiêu của em là trở thành binh sĩ xuất sắc như cha anh, để tên tuổi em được biết đến!<br> ",
    "I see. Your family must be expecting great things from you.<br> ": "Thôi hiểu. Gia đình chắc mong to lớn ở em lắm.<br> ",
    "Huh? Th-that is... um...<br> ": "Ủa? Thì th-thì là ừm...<br> ",
    "What's wrong?<br> ": "Sự việc thế nào?<br> ",
    "Actually, my family has opposed my becoming a soldier...<br> ": "Thực ra... gia đình em phản đối em làm binh sĩ...<br> ",
    "Oh? Why is that?<br> ": "Ồ? Tại sao vậy?<br> ",
    "They said that a small woman like me could never handle dangerous<br>battlefield duties...<br> ": "Bọn họ nói con gái nhỏ nhạy như em không thể gánh nổi nhiệm vụ chiến trường nguy hiểm...<br> ",
    "...I see. Then you came to the right place.<br> ": "...Hiểu rồi. Đến đây là đúng chỗ.<br> ",
    "Huh?<br> ": "Ủa?<br> ",
    "This is the front line. Chances to prove yourself are everywhere. Earn<br>merits here and show your family you've got what it takes.<br> ": "Đây là tiền tuyến. Cơ hội dựng công khắp nơi. Làm công đến đây để gia đình thấy em xứng đáng làm binh sĩ.<br> ",
    "Yes, sir! I will surely meet your expectations, Commander! Now, I shall<br>take my leave!<br> ": "Vâng, ạ! Em chắc chắn sẽ đáp ứng kỳ vọng của Chỉ Huy! Em xin phép lui!<br> ",
    "She is quite spirited, and seems like a fine girl.<br> ": "Cô ấy rất hăng hái, lại còn là cô gái tốt.<br> ",
    "Yeah. Having someone like that around really lifts the mood.<br> ": "Ừ. Có người như thế không khí nơi đây dễ chịu hơn.<br> ",
    "I hope she does well!<br> ": "Hy vọng cô ấy làm tốt!<br> ",
    "Yeah.<br> ": "Ừ.<br> ",
    "So, excavation inside the Abyss is proving difficult. We had high<br>hopes for the Engineer Corps with their specialized skills, but...<br> ": "Vậy thì... khai quật trong Đại Huyệt đang gặp khó khăn. Đội Kỹ Sư chuyên môn ta kỳ vọng cao nhưng...<br> ",
    "When we actually looked into it, they've been fighting endlessly over<br>who should take charge as captain, and work has hardly progressed.<br> ": "Mở ra xem thì toàn tranh giành ai làm đội trưởng dẫn việc, công việc không tiến được chút nào.<br> ",
    "So they'll only listen to someone they acknowledge. These<br>craftsman-types can be a real handful at times like this.<br> ": "Chỉ nghe người mình công nhận thôi. Nhóm thủ công kiểu này lúc khó xử lắm.<br> ",
    "The captain, huh... Should I just appoint one myself? No, if I take a<br>high-handed approach, they'll only resist more...<br> ": "Đội trưởng à... có nên ta chỉ định luôn không? Không, đập đầu cho bọn nó chỉ khiến bọn nó phản kháng mạnh hơn thôi...<br> ",
    "Thinking about it isn't getting me anywhere. I'm going out to get some<br>fresh air.<br> ": "Tưởng cũng chẳng ra gì. Ta ra ngoài hít chút không khí cho thoáng.<br> ",
    "A leader for that rowdy bunch of engineers, huh... What to do... Hmm?<br> ": "Cầm đầu đám kỹ sư man rợ ấy à... Làm sao cho ổn... Ủa?<br> ",
    "*sigh*... What should I do...<br> ": "*Thở dài*... Làm sao bây giờ...<br> ",
    "Betty, long time no see.<br> ": "Betty, lâu không gặp.<br> ",
    "Ah, Lord Commander...!<br> ": "A, Chỉ Huy...!?<br> ",
    "To think you remembered my name, Lord Commander... I'm deeply<br>honored!<br> ": "Không ngờ Chỉ Huy nhớ tên em... Em xúc động lắm ạ!<br> ",
    "You're exaggerating. But anyway... Did something happen?<br> ": "Nói lớn thật. Thôi không nói nữa... Có chuyện gì à?<br> ",
    "You were sighing with a gloomy face, weren't you?<br> ": "Người ta đang thở dài mặt mũi chán nản mà.<br> ",
    "...Haha, you caught me. That's the Lord Commander for you.<br> ": "...Haha, bị bắt quả tang. Thiệt là Chỉ Huy ạ.<br> ",
    "Actually... I was assigned to a monster-hunting squad, but I froze up<br>in a cave and caused trouble for my comrades.<br> ": "Thực ra... em được phân vào đội săn quái, nhưng trong hang động sợ tới mức đóng băng, làm phiền đồng đội...<br> ",
    "You froze? Were you injured?<br> ": "Đóng băng? Có bị thương không?<br> ",
    "Well, um... I'm not good with dark places. I got scared and couldn't<br>move.<br> ": "Đó, ừm... em sợ chỗ tối. Sợ nên không nhúc nhích được.<br> ",
    "That's tough... If so, why not request a transfer?<br> ": "Khó xử nhỉ... Thế thì xin điều động đi.<br> ",
    "That's why I had myself reassigned as a quartermaster. I thought that<br>as a quartermaster handling supplies and cooking, I could be of use.<br> ": "Em nghĩ vậy nên xin điều động làm Binh Quân Nhu. Quản lý tiêu hao nấu nướng là Binh Quân Nhu, nghĩ là có ích.<br> ",
    "But even there, I failed...<br> ": "Nhưng ngay đó cũng thất bại...<br> ",
    "What, you're bad at cooking?<br> ": "Gì, nấu ăn dở à?<br> ",
    "No, cooking is actually my strong suit. But...<br> ": "Không, nấu ăn đúng là thế mạnh của em. Nhưng...<br> ",
    "I served a full-course meal, and they got angry, saying, 'Who's got<br>the leisure to eat something like this on the battlefield!'<br> ": "Em trình bày món đầy đủ, bọn họ giận 'Ai rảnh mà ăn thứ này trên chiến trường!'<br> ",
    "A f-full-course meal?<br> ": "Mó, món đầy đủ à?<br> ",
    "I thought a tasty meal would cheer them up, but it backfired.<br> ": "Em nghĩ ăn ngon cho vui mà thành ra đắc tội.<br> ",
    "After a string of such failures, I was eventually told I was a failure as<br>a soldier, and they stopped giving me any tasks...<br> ": "Nhiều lần như vậy, cuối cùng bảo em là binh sĩ thất格為, không giao việc gì nữa...<br> ",
    "A useless soldier like me earning merits? A pipe dream. How can I<br>write home? *sigh*...<br> ": "Binh sĩ vô dụng như em dựng công? Mộng tưởng. Viết thư về gia đình làm sao? *Thở dài*...<br> ",
    "(She's really down... Huh?)<br> ": "(Cô ấy thực sự chán nản... Ủa?)<br> ",
    "She scrubbed at the stone.<br> ": "Cô ấy chà xát viên đá.<br> ",
    "Betty, what have you been doing?<br> ": "Betty, từ đầu làm gì vậy?<br> ",
    "Ah, sorry, it's a habit... I was polishing this.<br> ": "A, xin lỗi, thói quen... Em đang mài cái này.<br> ",
    "This... is a stone? Why would you do that?<br> ": "Đây... là đá à? Tại sao lại làm thế?<br> ",
    "It's my hobby!<br> ": "Đó là sở thích của em!<br> ",
    "Polishing stones?<br> ": "Mài đá à?<br> ",
    "Yes!<br> ": "Vâng!<br> ",
    "The stone sparkled.<br> ": "Viên đá lấp lánh.<br> ",
    "Huh? That stone, it's shining awfully bright, isn't it?<br> ": "Ủa? Viên đá kia, sáng rỡ thật, sao?<br> ",
    "Eheh! That's right.<br> ": "Ehe! Đúng vậy.<br> ",
    "Even a dull pebble buried in the earth for years can shine like a<br>beautiful gem if you polish it carefully and patiently!<br> ": "Ngay cả viên sỏi nhòe chôn đất nhiều năm, mài kỹ kiên nhẫn cũng lấp lánh như đá quý đẹp đẽ!<br> ",
    "Speaking of stones, I am sure there are all sorts of stones in the<br>Abyss that you cannot see on the surface!<br> ": "Nói đến đá, trong Đại Huyệt chắc có đủ loại đá không thấy trên mặt đất!<br> ",
    "Ah... I wonder just what kind of stones are in the Abyss...<br> ": "A... Chẳng biết trong Đại Huyệt có đá gì...<br> ",
    "...<br> ": "…<br> ",
    "Wah! I-I'm sorry, I got carried away all by myself! In front of the Lord<br>Commander, I ended up lost in my own world...<br> ": "Wa! Em-em xin lỗi, tự dưng hăng hái một mình! Trước mặt Chỉ Huy, lỡ đưa vào thế giới riêng...<br> ",
    "No, it's fine. Having something you can get so into is a good thing.<br> ": "Không, không sao. Có thứ làm say mê là tốt.<br> ",
    "So you know all about stones, then?<br> ": "Vậy ngươi rành hết về đá à?<br> ",
    "Of course! But a hobby like this is completely useless on the<br>battlefield...<br> ": "Tất nhiên! Nhưng sở thích kiểu này trên chiến trường hoàn toàn vô dụng...<br> ",
    "...Betty.<br> ": "...Betty.<br> ",
    "I mean, I cannot be moping around, right! I have to work hard again<br>starting tomorrow!<br> ": "Ý là, không thể chán nản mãi đâu! Từ mai phải cố gắng lại!<br> ",
    "Are you sure you're okay?<br> ": "Chắc chắn ổn chứ?<br> ",
    "Of course! Enthusiasm is the only thing I have going for me! So you<br>too must give it your all with a smile, Lord Commander!<br> ": "Tất nhiên! Chỉ có nhiệt huyết là cái em có! Chỉ Huy cũng phải cười tươi mà chiến đấu nhé!<br> ",
    "Heh. Yeah, I guess so.<br> ": "Hê. Ừ, đoán vậy.<br> ",
    "Well then, I shall take my leave!<br> ": "Vậy em xin phép lui!<br> ",
    "...Hold on a second.<br> ": "...Chờ đã.<br> ",
    "Yes? What is it?<br> ": "Vâng? Có chuyện gì?<br> ",
    "Betty, would you come with me for a bit?<br> ": "Betty, ngươi theo ta một chút?<br> ",
    "...?<br> ": "...?<br> ",
}

# Print summary
print(f"Total translations: {len(VI)}")
print("\nSample entries:")
for k, v in list(VI.items())[:5]:
    print(f"  EN: {k[:60]}...")
    print(f"  VI: {v[:60]}...")
    print()