#!/usr/bin/env python3
"""
Build VI asset for hmn_10490100003.txt
EN-asset-is-English case. Corrected sequence order.
107 records: 1 title + 104 message + 2 messageTextCenter
"""

import re, sys, json, os

ROOT = r'E:/AgentTranslation'
EN_PATH = ROOT + r'/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100003.txt'
VI_PATH = ROOT + r'/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100003.txt'
WORK = r'E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10490100003_full'

# ---- VI TRANSLATIONS in exact file order (SEQ 0..106) ----
# Format: (command_type, vi_text)
VI = [
    # SEQ 0: title
    ('title', 'Hâm Mộ Kỵ Sĩ Có Gì Sai Sao?'),
    # SEQ 1: message,クロエ,Ugh... I never thought...
    ('message', 'Hự... không ngờ lại đến nông nỗi này...<br> '),
    # SEQ 2: message,<user>,Alicia may seem calm...
    ('message', 'Alicia nhìn thì có vẻ điềm tĩnh‚ nhưng thỉnh thoảng lại nói mấy chuyện<br>động trời...<br> '),
    # SEQ 3: message,クロエ,I hate being in a place...
    ('message', 'Ghét cái chỗ không có Kỵ Sĩ Công Chúa nào hết!<br> '),
    # SEQ 4: messageTextCenter
    ('messageTextCenter', '<size=48>——Một Lúc Trước</size>'),
    # SEQ 5: message,アリシア,Since the date didn't work out...
    ('message', 'Vì buổi hẹn hò không thành‚ nên tôi cần Chỉ Huy và chị Chloe cùng<br>trải qua khoảng thời gian đặc biệt hơn nữa!<br> '),
    # SEQ 6: message,アリシア,A space where you won't be distracted...
    ('message', 'Một không gian mà anh sẽ không bị phân tâm bởi các nữ kỵ sĩ‚ chỉ<br>riêng hai người. Phải‚ một chuyến du lịch cho hai người!<br> '),
    # SEQ 7: message,クロエ,A trip with Commander!
    ('message', 'Du lịch cùng Chỉ Huy ư!<br> '),
    # SEQ 8: message,<user>,Wait, that's impossible...
    ('message', 'Khoan‚ chuyện đó không thể được. Tôi không thể rời Căn Cứ Tiền Tuyến được.<br> '),
    # SEQ 9: message,アリシア,It's not far at all...
    ('message', 'Cũng không xa lắm đâu. Tôi muốn anh hái mấy bông hoa mọc gần<br>đỉnh một ngọn núi cạnh căn cứ!<br> '),
    # SEQ 10: message,クロエ,To the mountain! B-but I'm a mage...
    ('message', 'Lên núi ư!? N-nhưng mà em là pháp sư‚ đâu có sức<br>leo núi đâu...<br> '),
    # SEQ 11: message,<user>,I have work too...
    ('message', 'Tôi cũng có việc mà. Làm gì có thời gian leo núi...<br> '),
    # SEQ 12: message,アリシア,Well then, take care and off you go!
    ('message', 'Vậy thì xin hãy cẩn thận và đi đi!<br> '),
    # SEQ 13: message,クロエ,Please listen to us!
    ('message', 'Nghe tụi em nói này!<br> '),
    # SEQ 14: message,<user>,That was truly high-handed...
    ('message', 'Đúng là độc đoán quá mức mà...<br> '),
    # SEQ 15: message,クロエ,I was so surprised! Are my knightivities really that bad...?
    ('message', 'Em bất ngờ quá! Việc hâm mộ kỵ sĩ của em thực sự tệ đến vậy sao...?<br> '),
    # SEQ 16: message,<user>,Well, being so wrapped up in knights...
    ('message', 'Ừm‚ mê mẩn nữ kỵ sĩ đến nỗi không nghe chỉ thị thì đúng là vấn đề.<br>Con bé cũng lo cho cô đấy.<br> '),
    # SEQ 17: message,クロエ,I know Miss Alicia is saying it for my sake...
    ('message', 'Em biết chị Alicia nói vì tốt cho em‚ nhưng cuộc đời em là dành cho<br>việc hâm mộ kỵ sĩ mà~.<br> '),
    # SEQ 18: message,クロエ,And the point of this trip...
    ('message', 'Và ý nghĩa của chuyến du lịch này là để em quan tâm đến Chỉ Huy<br>thay vì thần tượng của mình‚ đúng không~?<br> '),
    # SEQ 19: message,クロエ,My oshis are strong, glamorous, noble Princess Knights...
    ('message', 'Thần tượng của em là những Kỵ Sĩ Công Chúa mạnh mẽ‚ lộng lẫy‚ cao quý.<br>Em không ghét Chỉ Huy‚ nhưng không thấy có gì để hâm mộ cả...<br> '),
    # SEQ 20: message,クロエ,Besides, I seriously can't even imagine...
    ('message', 'Hơn nữa em thực sự không thể tưởng tượng nổi chuyện yêu đương<br>gì đó luôn.<br> '),
    # SEQ 21: message,<user>,Don't rope me into that...
    ('message', 'Đừng có kéo tôi vào chuyện đó khi tôi chưa nói gì. Mà nói thật thì<br>cô không cần phải hâm mộ tôi đâu.<br> '),
    # SEQ 22: message,<user>,I get why you support female knights...
    ('message', 'Tôi hiểu cảm giác ủng hộ nữ kỵ sĩ mà. Họ là nòng cốt của<br>chiến trường‚ đáng tin cậy nhưng cũng đáng lo—một sự hiện diện đầy quan tâm.<br> '),
    # SEQ 23: message,クロエ,R-right! They're so beautiful...
    ('message', 'Đ-đúng vậy! Họ đẹp đến thế mà vẫn dùng thân mình bảo vệ<br>chúng ta trong chiến đấu...<br> '),
    # SEQ 24: message,クロエ,They're noble and full of compassion...
    ('message', 'Cao quý và đầy lòng trắc ẩn‚ lại còn có sức mạnh kéo mọi người đi lên—<br>sao em có thể không hâm mộ họ được chứ!<br> '),
    # SEQ 25: message,<user>,Ahaha, nobility, compassion...
    ('message', 'Hà hà‚ cao quý‚ trắc ẩn‚ sức mạnh kéo người ta đi lên. Khác hẳn với tôi nhỉ.<br>Thôi‚ cô cứ sống với đam mê đi. Mấy chuyện lặt vặt tôi lo.<br> '),
    # SEQ 26: message,クロエ,...You're okay with that?
    ('message', '...Anh không sao chứ?<br> '),
    # SEQ 27: message,<user>,The front lines are a dangerous place...
    ('message', 'Mặt trận là nơi nguy hiểm‚ có một sở thích mà mình có thể dành cả<br>tính mạng để theo đuổi thì tôi mới yên tâm.<br> '),
    # SEQ 28: message,<user>,Strong feelings give you the strength to get up...
    ('message', 'Cảm xúc mạnh mẽ sẽ cho cô sức mạnh để đứng dậy vào giây phút cuối cùng.<br>Một thuộc hạ cứng đầu như thế là gu của tôi đấy.<br> '),
    # SEQ 29: message,<user>,A Chloe who wouldn't back down an inch...
    ('message', 'Một Chloe vì nữ kỵ sĩ mà không lùi bước dù chỉ một bước trước quái vật—<br>đó mới là thần tượng của tôi.<br> '),
    # SEQ 30: message,クロエ,I'm Commander's favorite...!
    ('message', 'Em là thần tượng của Chỉ Huy...!? A-ưu... em đâu phải đứa đáng được<br>ủng hộ đến vậy đâu...<br> '),
    # SEQ 31: message,<user>,Oh? Well then, what if Sophia suddenly said...
    ('message', 'Hử? Vậy nếu Sophia tự nhiên nói \"Em chẳng có giá trị gì để ai đó<br>hâm mộ cả\" thì sao?<br> '),
    # SEQ 32: message,クロエ,That can't be true!
    ('message', 'Sao có thể chứ! Em sẽ bực mình vì không thể truyền tải hết<br>được giá trị của chị ấy!<br> '),
    # SEQ 33: message,<user>,That's right. Chloe, you're a woman worth being a fan of...
    ('message', 'Đúng vậy đấy. Chloe‚ cô là người phụ nữ đáng để hâm mộ. Hãy<br>ngẩng cao đầu.<br> '),
    # SEQ 34: message,クロエ,Commander...
    ('message', 'Chỉ Huy...<br> '),
    # SEQ 35: message,,Without a word...
    ('message', 'Không một lời nào‚ chỉ có tiếng bước chân vang vọng khi hai người<br>bước tiếp.<br> '),
    # SEQ 36: message,クロエ,(W-what do I do...!)
    ('message', '(M-mình phải làm sao...! Lần đầu tiên có ai đó nói mình là thần tượng<br>của họ‚ lại còn chỉ có hai người nữa chứ!)<br> '),
    # SEQ 37: message,クロエ,(Huh, should I do fan service or something?)
    ('message', '(Hử‚ mình có nên làm fan service gì không nhỉ?<br>Liệu liếc mắt đưa tình một cái thì anh ấy có vui không?)<br> '),
    # SEQ 38: message,クロエ,...Peek.
    ('message', '...Liếc.<br> '),
    # SEQ 39: message,<user>,What's wrong? Are you tired?
    ('message', 'Sao thế? Mệt à?<br> '),
    # SEQ 40: message,クロエ,N-no, I'm fine!
    ('message', 'K-không‚ em ổn mà!<br> '),
    # SEQ 41: message,クロエ,(I-I got caught right away!)
    ('message', '(B-bị phát hiện ngay rồi!<br>Anh ấy đang nhìn‚ anh ấy đang nhìn mình kìa!)<br> '),
    # SEQ 42: message,クロエ,(Calm down. I'm sure Commander isn't a single-oshi...)
    ('message', '(Bình tĩnh nào. Chắc Chỉ Huy không phải chỉ hâm mộ mỗi mình Chloe đâu.<br>Đúng hơn là ảnh hâm mộ cả Căn Cứ Tiền Tuyến.)<br> '),
    # SEQ 43: message,クロエ,(But even so, it's certain that I'm one of his oshis...)
    ('message', '(Nhưng dù vậy‚ chắc chắn mình là một trong những thần tượng của ảnh...<br>Phư ơ ơ ơ!!!)<br> '),
    # SEQ 44: message,クロエ,(So this is how a Princess Knight feels...)
    ('message', '(Thì ra được hâm mộ là cảm giác thế này đây...!<br>Vui nhưng ngượng‚ và sao mà chua chua ngọt ngọt thế này!)<br> '),
    # SEQ 45: message,クロエ,(I can't handle this atmosphere!)
    ('message', '(Không chịu nổi bầu không khí này nữa!<br>Không về sớm là mình sẽ có mấy cảm giác kỳ lạ mất!)<br> '),
    # SEQ 46: message,クロエ,S-so, the flowers we're searching for...
    ('message', 'V-vậy‚ bông hoa chúng ta tìm mọc trên đỉnh núi phải không?<br>Tìm nhanh lên rồi kết thúc nhiệm vụ thôi!<br> '),
    # SEQ 47: message,<user>,Hey, don't run so fast!
    ('message', 'Này‚ đừng chạy nhanh thế!<br>Phía trước đường hẹp đấy!<br> '),
    # SEQ 48: message,クロエ,It's okay, I can handle this much...
    ('message', 'Không sao đâu‚ mức này em vẫn ổn...<br> '),
    # SEQ 49: message,,As Chloe ran and set foot on the narrow path...
    ('message', 'Khi Chloe chạy và đặt chân lên con đường hẹp‚<br>mặt đất dưới chân cô vỡ ra với một tiếng răng rắc.<br> '),
    # SEQ 50: message,クロエ,...! Kyaa!
    ('message', '...! Kyaaa!<br> '),
    # SEQ 51: message,クロエ,(It gave way... no way, I'm falling...!)
    ('message', '(Sụp mất rồi... không thể nào‚ mình đang rơi...!)<br> '),
    # SEQ 52: message,クロエ,(I won't be able to do my oshi activities anymore...)
    ('message', '(Không thể hâm mộ thần tượng nữa rồi... xin lỗi các Kỵ Sĩ Công Chúa...<br>Chỉ Huy...!)<br> '),
    # SEQ 53: message,<user>,Chloe!
    ('message', 'Chloe ơi!<br> '),
    # SEQ 54: message,,Chloe's falling arm was grabbed firmly by %user%...
    ('message', 'Cánh tay đang rơi của Chloe bị %user% nắm chặt lấy‚<br>và toàn thân cô lơ lửng trên không trung không điểm tựa.<br> '),
    # SEQ 55: message,<user>,That was close!
    ('message', 'Suýt thì nguy!<br> '),
    # SEQ 56: message,クロエ,Commander...?!
    ('message', 'Chỉ Huy...?!<br> '),
    # SEQ 57: message,<user>,Touching your oshi is strictly forbidden, right?
    ('message', 'Đụng vào thần tượng là nghiêm cấm nhỉ?<br>Lần này thì thông cảm cho tôi nhé!<br> '),
    # SEQ 58: message,クロエ,F-forget that, please let go...!
    ('message', 'B-bỏ qua chuyện đó đi‚ hãy buông em ra...!<br>Chỉ Huy cũng sẽ rơi theo mất!<br> '),
    # SEQ 59: message,<user>,Sh-shut up!
    ('message', 'I-im đi!<br>Tôi sẽ kéo cô lên ngay‚ chờ đấy!<br> '),
    # SEQ 60: message,,%user%'s hand, gripping Chloe's arm...
    ('message', 'Tay của %user% nắm chặt cánh tay Chloe run lên bần bật;<br>rõ ràng là anh đã đến giới hạn.<br> '),
    # SEQ 61: message,クロエ,I'm too fat and heavy—it's impossible!
    ('message', 'Em mập và nặng quá—không được đâu! Không sao‚ tại em cả thôi!<br> '),
    # SEQ 62: message,クロエ,I'd risk my life for my favorite knight too...
    ('message', 'Em cũng có thể liều mạng vì kỵ sĩ yêu thích của mình‚ nhưng—!<br>Anh thực sự không được chết...!<br> '),
    # SEQ 63: message,<user>,Shut up! I don't care about your favorite knight...
    ('message', 'Im đi! Thần tượng gì đó chẳng liên quan!<br> '),
    # SEQ 64: message,<user>,I'm the Commander! As long as I live...
    ('message', 'Ta là Chỉ Huy! Còn sống ngày nào thì sẽ không để thuộc hạ chết<br>trước mặt ta! Dù có gãy tay cũng sẽ cứu cô‚ Chloe!<br> '),
    # SEQ 65: message,クロエ,Commander...
    ('message', 'Chỉ Huy...<br> '),
    # SEQ 66: message,クロエ,(The nobility of a Commander who would never let his subordinates die...!)
    ('message', '(Sự cao quý của một Chỉ Huy không bao giờ để thuộc hạ mình chết...!<br>Lòng trắc ẩn khi nói sẽ cứu em dù có gãy tay!)<br> '),
    # SEQ 67: message,<user>,Don't give up, Chloe!
    ('message', 'Đừng bỏ cuộc‚ Chloe!<br> '),
    # SEQ 68: message,クロエ,(The warmth of Commander's hand...)
    ('message', '(Hơi ấm bàn tay của Chỉ Huy‚ kéo em lên khi tinh thần em<br>đã gục ngã...!)<br> '),
    # SEQ 69: message,クロエ,(What do I do? He's not a female knight...)
    ('message', '(Phải làm sao đây? Anh ấy không phải nữ kỵ sĩ‚ không phải thần tượng của em‚<br>nhưng tim em đập loạn xạ không ngừng được...!)<br> '),
    # SEQ 70: message,,Magic power swirled within Chloe...
    ('message', 'Ma lực cuộn xoáy bên trong Chloe. Ma Thuật Hỗ Trợ được kích hoạt<br>vô thức bao bọc lấy %user% trong một luồng ánh sáng dịu dàng.<br> '),
    # SEQ 71: message,<user>,I feel strength surging...
    ('message', 'Sức mạnh... đang trào dâng? Là nhờ Ma Thuật Hỗ Trợ của Chloe sao!<br>Vậy thì...<br> '),
    # SEQ 72: message,<user>,Uoooooh!
    ('message', 'Uớoooooh!<br> '),
    # SEQ 73: message,クロエ,W-we made it back... This is the base, Commander!
    ('message', 'V-về được rồi... Đây là căn cứ‚ Chỉ Huy!<br> '),
    # SEQ 74: message,<user>,*sigh*... we made it back somehow.
    ('message', '*thở dài*... cuối cùng cũng về được.<br> '),
    # SEQ 75: message,アリシア,Welcome back, you two! Are you both alright?
    ('message', 'Chào mừng hai người về! Cả hai có ổn không?<br> '),
    # SEQ 76: message,<user>,Safe? Hardly. We went through hell...
    ('message', 'Ổn? Chả ổn tí nào. Suýt thì đi đời rồi đây này.<br> '),
    # SEQ 77: message,<user>,But the mission succeeded...
    ('message', 'Nhưng nhiệm vụ thành công. Đây là hoa cô cần đúng không?<br> '),
    # SEQ 78: message,アリシア,Yes, I've confirmed it. Good work!
    ('message', 'Vâng‚ tôi đã kiểm tra rồi. Cảm ơn các anh chị!<br> '),
    # SEQ 79: message,<user>,No kidding... I'm never taking a trip like this again.
    ('message', 'Không sai... Không đời nào có chuyến du lịch như thế này nữa.<br> '),
    # SEQ 80: message,クロエ,It was quite an adventure...
    ('message', 'Đúng là một cuộc phiêu lưu ghê.<br>Suýt thì không thể hâm mộ kỵ sĩ nữa rồi.<br> '),
    # SEQ 81: message,<user>,You could've just said "I thought I was dead."
    ('message', 'Cô chỉ cần nói \"Tưởng chết rồi\" là được. Đừng biến cả cuộc đời<br>mình thành chuyện hâm mộ.<br> '),
    # SEQ 82: message,クロエ,...Yes, that's true...
    ('message', '...Phải‚ đúng thế... Ngoài việc hâm mộ ra chắc cũng có<br>mấy chuyện vui khác nhỉ...<br> '),
    # SEQ 83: message,アリシア,...Oh?
    ('message', '...Hử?<br>Có chuyện gì với Chloe à?<br> '),
    # SEQ 84: message,クロエ,W-what are you talking about?
    ('message', 'C-chị nói gì vậy?<br>Không có gì hết đâu!<br> '),
    # SEQ 85: message,クロエ,I'm sorry, Alicia, but...
    ('message', 'Xin lỗi chị Alicia‚ nhưng mà<br>em không thể hâm mộ Chỉ Huy làm thần tượng được!<br> '),
    # SEQ 86: message,アリシア,...Fufu, is that so?
    ('message', '...Phù phù‚ vậy sao?<br>Có vẻ kế hoạch đã thành công rồi nhỉ.<br> '),
    # SEQ 87: message,クロエ,Uuh... This is so embarrassing...
    ('message', 'Ự... Ngượng quá nên đừng nhìn em với ánh mắt đó!<br> '),
    # SEQ 88: messageTextCenter
    ('messageTextCenter', '<size=48>——Một Vài Ngày Sau</size>'),
    # SEQ 89: message,アリシア,According to the reports...
    ('message', 'Theo báo cáo từ các nữ kỵ sĩ‚<br>có vẻ ánh mắt của Chloe đã dịu lại một chút.<br> '),
    # SEQ 90: message,<user>,That's good.
    ('message', 'Vậy tốt quá.<br>Có lẽ hứng thú với việc hâm mộ đã lắng xuống rồi nhỉ.<br> '),
    # SEQ 91: message,アリシア,Don't you think she's found something else to focus on?
    ('message', 'Chẳng phải chị ấy đã tìm được điều khác để quan tâm sao?<br>Phải không‚ Chỉ Huy?<br> '),
    # SEQ 92: message,<user>,I don't know about that.
    ('message', 'Tôi có biết đâu.<br>Tôi là người ủng hộ việc hâm mộ của cô ấy mà.<br> '),
    # SEQ 93: message,アリシア,...Huh?
    ('message', '...Hử?<br>Đằng kia có phải là...<br> '),
    # SEQ 94: message,クロエ,S-Sophia!
    ('message', 'S-Sophia!<br>Chị đi nhiệm vụ vất vả rồi! Đây này‚ nếu chị thích thì...!<br> '),
    # SEQ 95: message,ソフィア,Oh, what a lovely bouquet...
    ('message', 'Ôi bó hoa đẹp quá... Cảm ơn chị Chloe.<br>Em ít thấy loại hoa này nhỉ.<br> '),
    # SEQ 96: message,クロエ,I picked them from the top of a nearby mountain...
    ('message', 'Em hái từ đỉnh một ngọn núi gần đây ạ.<br>Hy vọng chị thích nó...<br> '),
    # SEQ 97: message,ソフィア,Yes, I'm very pleased.
    ('message', 'Vâng‚ em rất thích.<br>Em sẽ treo ở phòng mình.<br> '),
    # SEQ 98: message,クロエ,Ah, my idol is so precious today...
    ('message', 'A‚ hôm nay thần tượng của em thật cao quý quá...<br> '),
    # SEQ 99: message,アリシア,W-Wait, Chloe!
    ('message', 'C-Chloe này!<br>Chị vẫn còn hâm mộ sao?<br> '),
    # SEQ 100: message,クロエ,Yes, of course.
    ('message', 'Vâng‚ tất nhiên.<br>Không có lý do gì để dừng lại cả~.<br> '),
    # SEQ 101: message,アリシア,But what about the Commander...?
    ('message', 'Nhưng còn Chỉ Huy thì sao...?<br> '),
    # SEQ 102: message,クロエ,That's... well, fandom and love are different things...
    ('message', 'Cái đó... thì thần tượng và tình yêu là hai chuyện khác nhau mà?<br> '),
    # SEQ 103: message,クロエ,Actually, now that my personal life is more fulfilling...
    ('message', 'Đúng hơn là từ khi đời sống riêng phong phú hơn‚<br>việc hâm mộ kỵ sĩ còn vui hơn ấy chứ! Cân bằng là quan trọng đấy!<br> '),
    # SEQ 104: message,アリシア,Both are part of your personal life, Chloe...
    ('message', 'Cả hai đều là chuyện riêng tư của chị hết đấy‚ chị Chloe...<br> '),
    # SEQ 105: message,<user>,Come on, it wouldn't be like you...
    ('message', 'Thôi nào‚ Chloe không hâm mộ nữ kỵ sĩ chẳng giống chút nào.<br>Hôm khác kể cho tôi nghe về thần tượng của cô nhé.<br> '),
    # SEQ 106: message,クロエ,Of course, Commander. Anytime.
    ('message', 'Tất nhiên rồi‚ Chỉ Huy. Bất cứ lúc nào.<br>Cùng nhau nói chuyện về thần tượng nhé!<br> '),
]

assert len(VI) == 107, f"Expected 107 records, got {len(VI)}"
print(f"[INFO] Loaded {len(VI)} VI translations")

# ---- PROCESS ----
with open(EN_PATH, 'rb') as f:
    raw = f.read()

has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw[:100]
print(f"[INFO] BOM={has_bom} CRLF={has_crlf}")

text = raw.decode('utf-8-sig')
lines = text.splitlines(True)  # keep line endings

output_lines = []
seq = -1
errors = []
br_errors = []
comma_errors = []
lines_processed = 0

TEXT_CMDS = ('title,', 'message,', 'messageTextCenter,', 'messageTextUnder,')

for ln in lines:
    stripped = ln.rstrip('\r\n')
    
    if stripped.startswith(TEXT_CMDS):
        seq += 1
        expected_cmd, vi_text = VI[seq]
        
        if stripped.startswith('title,'):
            # title,<text>
            parts = stripped.split(',', 2)
            old_text = parts[1]
            ending = ln[len(ln.rstrip('\r\n')):]
            new_line = f"title,{vi_text}"
            output_lines.append(new_line + ending)
            old_br = old_text.count('<br>')
            new_br = vi_text.count('<br>')
            if old_br != new_br:
                br_errors.append(f"SEQ {seq} title: BR {old_br}->{new_br}")
            if ',' in vi_text:
                comma_errors.append(f"SEQ {seq} title: ASCII comma")
            lines_processed += 1
            continue
        
        if stripped.startswith('messageTextCenter,'):
            # messageTextCenter,,<text>,,,on
            parts = stripped.split(',', 3)
            old_text = parts[2] if len(parts) > 2 else ''
            ending = ln[len(ln.rstrip('\r\n')):]
            new_line = f"messageTextCenter,,{vi_text},,,on"
            output_lines.append(new_line + ending)
            old_br = old_text.count('<br>')
            new_br = vi_text.count('<br>')
            if old_br != new_br:
                br_errors.append(f"SEQ {seq} center: BR {old_br}->{new_br}")
            if ',' in vi_text:
                comma_errors.append(f"SEQ {seq} center: ASCII comma")
            lines_processed += 1
            continue
        
        if stripped.startswith('message,'):
            # message,<speaker>,<text>[,rest...]
            parts = stripped.split(',', 5)
            if len(parts) >= 3:
                speaker = parts[1]
                old_text = parts[2]
                ending = ln[len(ln.rstrip('\r\n')):]
                suffix_parts = parts[3:]
                
                if suffix_parts:
                    new_line = f"message,{speaker},{vi_text},{','.join(suffix_parts)}"
                else:
                    new_line = f"message,{speaker},{vi_text}"
                
                output_lines.append(new_line + ending)
                old_br = old_text.count('<br>')
                new_br = vi_text.count('<br>')
                if old_br != new_br:
                    br_errors.append(f"SEQ {seq} msg: BR {old_br}->{new_br} vi='{vi_text[:50]}'")
                if ',' in vi_text:
                    comma_errors.append(f"SEQ {seq} msg: ASCII comma")
                lines_processed += 1
                continue
    
    # Non-text line, pass through
    output_lines.append(ln)

# ---- FINAL CHECKS ----
print(f"\n[INFO] Processed {lines_processed} text records")
print(f"[INFO] Total output lines: {len(output_lines)}")

if errors:
    for e in errors:
        print(f"[ERROR] {e}")
    sys.exit(1)

if br_errors:
    print(f"[ERROR] {len(br_errors)} BR count mismatches:")
    for e in br_errors:
        print(f"  {e}")
    sys.exit(1)

if comma_errors:
    print(f"[ERROR] {len(comma_errors)} ASCII comma in VI:")
    for e in comma_errors:
        print(f"  {e}")
    sys.exit(1)

# ---- WRITE ----
output_text = ''.join(output_lines)
if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_text.encode('utf-8')
else:
    output_bytes = output_text.encode('utf-8')

if has_crlf:
    output_bytes = output_bytes.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')

os.makedirs(os.path.dirname(VI_PATH), exist_ok=True)
with open(VI_PATH, 'wb') as f:
    f.write(output_bytes)

print(f"\n[PASS] Wrote VI to: {VI_PATH}")
print(f"[PASS] {lines_processed} text records translated")

# ---- POST-VERIFY ----
print("\n--- Post-build verification ---")
with open(EN_PATH, 'rb') as f:
    en_raw = f.read()
with open(VI_PATH, 'rb') as f:
    vi_raw = f.read()

en_text = en_raw.decode('utf-8-sig')
vi_text_all = vi_raw.decode('utf-8-sig')

en_lines = en_text.splitlines(True)
vi_lines = vi_text_all.splitlines(True)

print(f"EN lines: {len(en_lines)}, VI lines: {len(vi_lines)}")
if len(en_lines) != len(vi_lines):
    print(f"[WARN] Line count mismatch!")

# Count VI text records
vi_title = vi_text_all.count('[\\n\\r]?title,')  # rough
vi_title = sum(1 for l in vi_lines if l.startswith('title,'))
vi_msg = sum(1 for l in vi_lines if l.startswith('message,'))
vi_center = sum(1 for l in vi_lines if l.startswith('messageTextCenter,'))
vi_under = sum(1 for l in vi_lines if l.startswith('messageTextUnder,'))
print(f"VI: title={vi_title} message={vi_msg} center={vi_center} under={vi_under} total={vi_title+vi_msg+vi_center+vi_under}")

# Check for unchanged records
en_tl = [(i, l) for i, l in enumerate(en_lines) if l.startswith(TEXT_CMDS)]
vi_tl = [(i, l) for i, l in enumerate(vi_lines) if l.startswith(TEXT_CMDS)]
changed = 0
unchanged = []
for (ei, el), (vi, vl) in zip(en_tl, vi_tl):
    if el.rstrip('\r\n') == vl.rstrip('\r\n'):
        unchanged.append(ei)
    else:
        changed += 1
if unchanged:
    print(f"[WARN] {len(unchanged)} unchanged text records (EN lines: {unchanged[:5]}...)")
else:
    print(f"[OK] All {len(en_tl)} text records changed")

# Check for leftover EN words in VI text fields
en_words_check = ['Commander', 'Frontline Base', 'Princess Knight', 'knightivities', 'oshi', 'fan service', 'Fan', 'idol', 'knight']
for vi_ln in vi_lines:
    s = vi_ln.rstrip('\r\n')
    if s.startswith(TEXT_CMDS):
        parts = s.split(',', 3)
        field = parts[2] if len(parts) > 2 else parts[1] if len(parts) > 1 else ''
        for w in en_words_check:
            if w in field and w not in ['Chloe', 'Sophia', 'Alicia', 'Kyaa']:
                pass  # We'll scan more carefully

found_en = []
for vi_ln in vi_lines:
    s = vi_ln.rstrip('\r\n')
    if s.startswith(TEXT_CMDS):
        parts = s.split(',', 3)
        field = parts[2] if len(parts) > 2 else parts[1] if len(parts) > 1 else ''
        for w in ['Commander', 'Frontline Base', 'Princess Knight', 'knightivities', 'Fan', 'fan', 'oshi']:
            if w in field:
                found_en.append(f"'{w}' in field: '{field[:60]}'")

if found_en[:3]:
    print(f"[WARN] EN leftovers sample: {found_en[:3]}")
else:
    print("[OK] No EN leftovers in VI text fields")

print("\n[DONE] Build complete")
