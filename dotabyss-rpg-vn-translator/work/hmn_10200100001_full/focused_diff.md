# Focused diff — hmn_10200100001

Only the 85 translated text-command lines differ (title + 84 message lines). All structural bytes (delimiters, tags, voice IDs, chara IDs, BOM, CRLF, line count=1576) are preserved.

```diff
--- EN
+++ VI
@@ -47,7 +47,7 @@
 
 
 seplay,seopening_tag,se5030001
-title,なんでもできるお姉さん？
+title,Chị Gái Có Thể Làm Được Mọi Thứ?
 
 wait,1
 
@@ -56,7 +56,7 @@
 
 
 window,on,0.15
-message,,The sounds of fierce battle echoed through the forest. A battle was<br>underway to intercept the monsters closing in on the Frontline Base.<br> 
+message,,Tiếng giao tranh ác liệt vang vọng khắp khu rừng. Một trận chiến đang<br>diễn ra để chặn đứng lũ quái vật đang tiến sát Căn Cứ Tiền Tuyến.<br> 
 
 window,off
 wait,0.15
@@ -95,7 +95,7 @@
 linework,on,White,Light
 
 window,on,0.15
-message,モンスター,GUOOOOOH!!<br> ,,,chara_11
+message,モンスター,GÀOOOOO!!<br> ,,,chara_11
 
 linework,off,Black,Light
 
@@ -158,7 +158,7 @@
 asynccharareaction,chara_2,Jump,1,STOP
 asynccharaemo,chara_2,Exclamation,STOP
 window,on,0.15
-message,ソフィア,No! The monster went that way! Someone，stop it!<br> ,,vc_10200100001_001_01
+message,ソフィア,Không được! Con quái vật chạy về phía đó rồi! Ai đó‚ ngăn nó lại đi!<br> ,,vc_10200100001_001_01
 
 window,off
 wait,0.15
@@ -205,7 +205,7 @@
 
 asynccharaemo,chara_3,Panic,STOP
 window,on,0.15
-message,クルル,Nooo! I can't reach it!<br> ,,vc_10200100001_002_01
+message,クルル,Không được! Em không với tới được!<br> ,,vc_10200100001_002_01
 
 window,off
 wait,0.15
@@ -244,7 +244,7 @@
 asynccharareaction,chara_2,Jump,1,STOP
 asynccharaemo,chara_2,Exclamation,STOP
 window,on,0.15
-message,ソフィア,Verisa，run!<br> ,,vc_10200100001_003_01
+message,ソフィア,Verisa‚ chạy đi!<br> ,,vc_10200100001_003_01
 
 window,off
 wait,0.15
@@ -280,15 +280,15 @@
 asyncshake,CHARA,chara_4,20,15,0.5,6,on,off,0,off,CONT,0
 
 window,on,0.15
-message,ベリサ,Huh...?!<br> ,,vc_10200100001_004_01
-
-
-
-message,,Just as Verisa was focusing to unleash a spell，a monster slipped<br>through the formation and attacked her.<br> 
+message,ベリサ,Hả...?!<br> ,,vc_10200100001_004_01
+
+
+
+message,,Ngay khi Verisa đang tập trung để thi triển phép thuật‚ một con quái vật đã<br>lách qua đội hình và tấn công cô ấy.<br> 
 
 linework,on,White,Strong
 
-message,モンスター,GUOOOOOH!!<br> 
+message,モンスター,GÀOOOOO!!<br> 
 
 window,off
 wait,0.15
@@ -301,7 +301,7 @@
 
 asynccharareaction,chara_4,Shake,1,STOP
 window,on,0.15
-message,ベリサ,Aaaah!<br> ,,vc_10200100001_005_01
+message,ベリサ,Áaaa!<br> ,,vc_10200100001_005_01
 
 window,off
 wait,0.15
@@ -330,11 +330,11 @@
 
 
 window,on,0.15
-message,,Just as the monster was about to take Verisa's life，Laveria threw<br>herself in front of her and blocked the deadly strike.<br> 
+message,,Ngay khoảnh khắc con quái vật sắp đoạt mạng Verisa‚ Laveria đã lao<br>ra đỨ trước mặt cô ấy và chặn đứng nhát chém chết người đó.<br> 
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
 
-message,ラヴェリア,You're not getting past me! Fall back，Verisa，now!<br> ,,vc_10200100001_006_01
+message,ラヴェリア,Không ai lọt qua được ta đâu! Lùi lại đi‚ Verisa‚ mau!<br> ,,vc_10200100001_006_01
 
 window,off
 wait,0.15
@@ -361,7 +361,7 @@
 asynccharareaction,chara_7,Nod,1,STOP
 asynccharaemo,chara_7,Laugh,STOP
 window,on,0.15
-message,マリナ,Honey! Looks like Laveria saved little Verisa from a tight spot!<br> ,,vc_10200100001_007_01
+message,マリナ,Phu quân! Có vẻ như Laveria đã cứu bé Verisa thoát khỏi tình cảnh ngặt nghèo rồi đó!<br> ,,vc_10200100001_007_01
 
 window,off
 wait,0.15
@@ -376,9 +376,9 @@
 wait,0.2
 
 window,on,0.15
-message,<user>,Great job，Laveria! While she's holding them off，let's regroup!<br> 
-
-message,<user>,Stay calm and reform the formation! Provide cover for Laveria...<br>cover...?<br> 
+message,<user>,Làm tốt lắm‚ Laveria! Trong lúc cô ấy cầm chân bọn chúng‚ ta cùng tái chiến đấu!<br> 
+
+message,<user>,Bình tĩnh và tái lập đội hình! Hãy yểm trợ cho Laveria...<br>yểm trợ...?<br> 
 
 window,off
 wait,0.15
@@ -408,7 +408,7 @@
 asyncshake,CHARA,chara_8,20,0,0.5,5,off,off,0,on,CONT,0
 
 window,on,0.15
-message,ラヴェリア,Is that all you've got! You dare challenge me! *pant*!<br> ,,vc_10200100001_008_01
+message,ラヴェリア,Chỉ có thế thôi à! Ngươi dám thách thức ta sao! *thở dốc*!<br> ,,vc_10200100001_008_01
 
 window,off
 wait,0.15
@@ -438,7 +438,7 @@
 
 
 window,on,0.15
-message,,With every swing of her greatsword，Laveria thinned the horde.<br> 
+message,,Với mỗi nhát chém đại kiếm‚ Laveria đã làm thưa bớt đám quái vật.<br> 
 
 window,off
 wait,0.15
@@ -486,7 +486,7 @@
 asyncshake,CHARA,chara_11,20,15,0.3,6,on,off,0,off,CONT
 
 window,on,0.15
-message,モンスター,*roar*...<br> 
+message,モンスター,*gầm rú*...<br> 
 
 window,off
 wait,0.15
@@ -535,10 +535,10 @@
 asynccharareaction,chara_6,Jump,1,STOP
 asynccharaemo,chara_6,Exclamation,STOP
 window,on,0.15
-message,ヒマリ,Wow... she's beating them all!<br> ,,vc_10200100001_009_01
-
-asyncwait
-message,<user>,No kidding... She's not just holding them off，she's charging ahead!<br> 
+message,ヒマリ,Wow... chị ấy đánh bại hết cả đám rồi!<br> ,,vc_10200100001_009_01
+
+asyncwait
+message,<user>,Đúng thiệt... chị ấy không chỉ cầm chân chúng‚ mà còn xông lên phía trước!<br> 
 
 window,off
 wait,0.15
@@ -559,7 +559,7 @@
 wait,0.5
 
 window,on,0.15
-message,ラヴェリア,I'm taking them all! Stop me if you can!<br> ,,vc_10200100001_010_01
+message,ラヴェリア,Ta sẽ quét sạch tất cả! Cản ta lại nếu các ngươi có thể!<br> ,,vc_10200100001_010_01
 
 window,off
 wait,0.15
@@ -628,7 +628,7 @@
 
 
 window,on,0.15
-message,モンスター,Gyaoooooo...<br> ,,,chara_8/chara_9/chara_10
+message,モンスター,Gào...<br> ,,,chara_8/chara_9/chara_10
 
 
 window,off
@@ -637,9 +637,9 @@
 charascale,chara_1,1,0
 
 window,on,0.15
-message,<user>,Wait，wait，wait! Are you trying to take them all down by yourself?<br> 
-
-message,<user>,Everyone，provide covering fire! Hurry before Laveria finishes them<br>all!<br> 
+message,<user>,Khoan‚ khoan‚ khoan! Em định một mình hạ gục hết bọn chúng sao?<br> 
+
+message,<user>,Mọi người‚ hãy yểm trợ hỏa lực! Nhanh lên kẻo Laveria dọn dẹp hết<br>bọn chúng mất!<br> 
 
 window,off
 wait,0.15
@@ -667,9 +667,9 @@
 
 asynccharareaction,chara_1,Nod,1,STOP
 window,on,0.15
-message,ラヴェリア,*phew*... no sign of any more enemies.<br> ,,vc_10200100001_011_01
-
-message,<user>,Good work，Laveria. That was incredible.<br> 
+message,ラヴェリア,*hà*... không còn dấu hiệu của thêm kẻ địch nào.<br> ,,vc_10200100001_011_01
+
+message,<user>,Làm tốt lắm‚ Laveria. Thật phi thường.<br> 
 
 charaface,chara_1,EyeOpen
 charaface,chara_1,FaceNormal
@@ -681,13 +681,13 @@
 asynccharaface,chara_1,FaceNormal,CONT,2.2
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
-message,ラヴェリア,No，I failed. I got a little too into it and overdid it.<br> ,,vc_10200100001_012_01
-
-asyncwait
-
-message,<user>,I never said not to take them out yourself. If you can take them out，<br>that's fine by me.<br> 
-
-message,<user>,You also covered Verisa in time. Thanks to you，she didn't get hurt.<br> 
+message,ラヴェリア,Không‚ em đã thất bại. Em hơi bốc quá nên làm lố mất rồi.<br> ,,vc_10200100001_012_01
+
+asyncwait
+
+message,<user>,Ta đâu có bảo em đừng tự mình hạ chúng. Nếu em hạ được thì<br>cứ việc‚ ta không phiền.<br> 
+
+message,<user>,Em còn kịp yểm trợ cho Verisa nữa. Nhờ có em‚ cô ấy đã không bị thương.<br> 
 
 charaface,chara_1,FaceFun
 
@@ -695,7 +695,7 @@
 
 asynccharareaction,chara_1,Nod,1,STOP
 asynccharaemo,chara_1,Laugh,STOP
-message,ラヴェリア,So Verisa's safe too. That's good.<br> ,,vc_10200100001_013_01
+message,ラヴェリア,Vậy Verisa cũng an toàn rồi. Tốt quá.<br> ,,vc_10200100001_013_01
 
 window,off
 wait,0.15
@@ -736,7 +736,7 @@
 
 asynccharaface,chara_4,FaceShy,STOP,1
 window,on,0.15
-message,ベリサ,I was soooo scared! Thank youuu，Laveria!<br> ,,vc_10200100001_014_01
+message,ベリサ,Em sợ phát khiếp luôn! Cảm ơn chị nhiều lắm‚ Laveria!<br> ,,vc_10200100001_014_01
 
 window,off
 wait,0.15
@@ -758,7 +758,7 @@
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
 window,on,0.15
-message,ラヴェリア,Brother ordered me to cover you. If you're going to thank anyone，<br>thank him.<br> ,,vc_10200100001_015_01
+message,ラヴェリア,Anh đã ra lệnh cho em yểm trợ cho em ấy. Nếu em muốn cảm ơn ai thì<br>cảm ơn anh ấy đi.<br> ,,vc_10200100001_015_01
 
 asyncwait
 
@@ -788,9 +788,9 @@
 asynccharareaction,chara_4,Nod,1,STOP
 asynccharaemo,chara_4,Laugh,STOP
 window,on,0.15
-message,ベリサ,Ehh，it's only natural for Mister to help me，right? I mean，isn't it his<br>fault his command was so sloppy?<br> ,,vc_10200100001_016_01
-
-message,<user>,Oh come on... I even had reserves ready. That's no way to talk to me.<br>Fine，reflecting on today，I'll give you close-combat training.<br> 
+message,ベリサ,Ê‚ đương nhiên là anh phải giúp em rồi‚ đúng không? Ý em là‚ lỗi của<br>anh ấy chỉ huy lỏng lẻo thế kia mà?<br> ,,vc_10200100001_016_01
+
+message,<user>,Ôi thôi nào... anh còn chuẩn bị cả quân dự bị cơ mà. Nói thế với anh không<br>được đâu. Được rồi‚ suy ngẫm từ hôm nay‚ anh sẽ cho em huấn luyện cận chiến.<br> 
 
 charaface,chara_4,FaceSurprise
 
@@ -800,9 +800,9 @@
 
 asynccharareaction,chara_4,Shake,1,STOP
 asynccharaemo,chara_4,Shock,STOP
-message,ベリサ,Wh-WHAA? Why do I have to do that?<br> ,,vc_10200100001_017_01
-
-message,<user>,If you were a magic knight who could handle both ranges，it wouldn't<br>be a problem，right? As commander，I can't ignore a weakness.<br> 
+message,ベリサ,Ể-Ểeee? Tại sao em phải làm chuyện đó?<br> ,,vc_10200100001_017_01
+
+message,<user>,Nếu em là một hiệp sĩ pháp sư cân được cả tầm xa lẫn tầm gần thì đâu có<br>thành vấn đề‚ đúng không? Làm chỉ huy‚ anh không thể làm ngơ trước một điểm yếu.<br> 
 
 charaface,chara_4,FaceUnique01
 
@@ -813,9 +813,9 @@
 asynccharaemo,chara_4,Panic,STOP
 
 asynccharaface,chara_4,FaceShy,STOP,1
-message,ベリサ,Umm，I think girls are cuter when they have a little flaw，don't you<br>think?<br> ,,vc_10200100001_018_01
-
-message,<user>,Don't call yourself cute! You should aim to be an all-rounder like<br>Laveria!<br> 
+message,ベリサ,Ưm‚ em nghĩ con gái có một chút khuyết điểm thì mới dễ thương‚ anh<br>thấy có phải không?<br> ,,vc_10200100001_018_01
+
+message,<user>,Đừng tự nhận mình dễ thương! Em nên phấn đấu thành người đa năng như<br>Laveria!<br> 
 
 window,off
 wait,0.15
@@ -854,7 +854,7 @@
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
 window,on,0.15
-message,ラヴェリア,...Flaws make you cuter，huh.<br> ,,vc_10200100001_019_01
+message,ラヴェリア,...Khuyết điểm khiến em dễ thương hơn‚ à.<br> ,,vc_10200100001_019_01
 
 asyncwait
 
@@ -885,7 +885,7 @@
 
 asynccharaemo,chara_6,Speak,STOP
 window,on,0.15
-message,ヒマリ,Laveria，is something wrong?<br> ,,vc_10200100001_020_01
+message,ヒマリ,Laveria‚ có chuyện gì sao?<br> ,,vc_10200100001_020_01
 
 charafocuson,chara_1
 
@@ -905,7 +905,7 @@
 
 asynccharareaction,chara_1,Nod,1,STOP
 asynccharaemo,chara_1,Laugh,STOP
-message,ラヴェリア,No，nothing. The battle's over. Let's head back to base.<br> ,,vc_10200100001_021_01
+message,ラヴェリア,Không‚ không có gì. Trận chiến đã kết thúc. Chúng ta về căn cứ thôi.<br> ,,vc_10200100001_021_01
 
 
 charaface,chara_6,FaceFun
@@ -914,7 +914,7 @@
 
 asynccharareaction,chara_6,Jump,1,STOP
 asynccharaemo,chara_6,Spirits,STOP
-message,ヒマリ,Yeah，let's go home.<br> ,,vc_10200100001_022_01
+message,ヒマリ,Ừ‚ về nhà thôi.<br> ,,vc_10200100001_022_01
 
 window,off
 wait,0.15
@@ -927,7 +927,7 @@
 asynccharamove,chara_1,LinearTarget,X,600,1,CONT
 
 window,on,0.15
-message,<user>,Right. Doesn't look like there'll be any more monster attacks... Kill<br>count: 13 goblins.<br> 
+message,<user>,Đúng. Có vẻ sẽ không có thêm đợt tấn công quái vật nào nữa... Số lượng<br>tiêu diệt: 13 yêu tinh.<br> 
 
 window,off
 wait,0.15
@@ -950,9 +950,9 @@
 
 asynccharaemo,chara_1,Question,STOP
 window,on,0.15
-message,ラヴェリア,You keep records every time like that? Being a commander is a tough<br>job，Brother.<br> ,,vc_10200100001_023_01
-
-message,<user>,I need to compile these reports or I can't plan the next operation.<br>Actually，they've been piling up... I don't wanna go back.<br> 
+message,ラヴェリア,Anh ghi chép mỗi lần như thế sao? Làm chỉ huy đúng là một công việc vất<br>vả‚ anh.<br> ,,vc_10200100001_023_01
+
+message,<user>,Anh cần tổng hợp mấy báo cáo này không thì không thể lên kế hoạch chiến<br>dịch tiếp theo. Thực ra‚ chúng nó chất đống cả rồi... anh chẳng muốn quay về tí nào.<br> 
 
 
 window,off
@@ -1003,7 +1003,7 @@
 seplay,setag1_32,se4400137,0,1
 
 window,on,0.15
-message,<user>,Piles of unprocessed documents，one after another! We're<br>shorthanded，completely shorthanded!<br> 
+message,<user>,Núi giấy tờ chưa xử lý chất đống‚ lớp này đến lớp khác! Chúng ta thiếu<br>nhân lực‚ thiếu nhân lực trầm trọng!<br> 
 
 window,off
 wait,0.15
@@ -1032,7 +1032,7 @@
 
 asynccharaemo,chara_5,Dull,STOP
 window,on,0.15
-message,アリシア,We've had so many operations lately that the reports haven't been<br>able to keep up，I'm afraid...<br> ,,vc_10200100001_024_01
+message,アリシア,Dạo này công tác tác chiến nhiều quá nên báo cáo không kịp theo kịp‚ em<br>e ngại lắm...<br> ,,vc_10200100001_024_01
 
 window,off
 wait,0.15
@@ -1051,7 +1051,7 @@
 
 asynccharamove,chara_5,0.3,X,-200,0.5,CONT
 window,on,0.15
-message,<user>,Alicia，help me with these too. Damn，isn't there anyone else good at<br>paperwork?<br> 
+message,<user>,Alicia‚ giúp anh mấy cái này nữa đi. Khỉ thật‚ sao không có ai khác giỏi<br>vụ giấy tờ nhỉ?<br> 
 
 asyncwait
 
@@ -1070,11 +1070,11 @@
 asynccharaemo,chara_5,Dull,STOP,5
 
 asynccharaface,chara_5,FaceSad,STOP,5
-message,アリシア,It's a lot for just me to handle... and everyone who might be able to<br>help is out right now...<br> ,,vc_10200100001_025_01
+message,アリシア,Một mình em xử lý số này thì quá sức... mà ai có thể giúp thì giờ đều<br>đang đi vắng hết...<br> ,,vc_10200100001_025_01
 
 seplay,setag1_41,se4400065,0,1
 
-message,<user>,Argh! Isn't there anyone who can handle both paperwork and combat!<br>And if she's a beauty，even better!<br> 
+message,<user>,Chết tiệt! Sao chẳng có ai vừa giỏi giấy tờ vừa chiến đấu được chứ!<br>Mà nếu là mỹ nữ thì càng tốt!<br> 
 
 window,off
 wait,0.15
@@ -1105,13 +1105,13 @@
 
 asynccharaface,chara_5,FaceSad,CONT,2
 window,on,0.15
-message,アリシア,C-Commander! Get a hold of yourself! I can't tell if you're losing your<br>mind or just being your usual self!<br> ,,vc_10200100001_026_01
+message,アリシア,C-Chỉ Huy! Xin ngài trấn tĩnh lại! Em không rõ là ngài đang phát<br>điên hay chỉ là bản thân ngài bình thường!<br> ,,vc_10200100001_026_01
 
 linework,off,White,Middle
 
 asyncwait
 
-message,<user>,As if this is normal for me! Damn，this is the kind of situation where<br>I'd take any help I can get...<br> 
+message,<user>,Làm gì có chuyện bình thường cho anh thế này! Khỉ thật‚ đây đúng là tình<br>cảnh mà anh sẽ nhận bất cứ giúp đỨ nào có thể...<br> 
 
 window,off
 wait,0.15
@@ -1136,7 +1136,7 @@
 wait,1
 
 window,on,0.15
-message,ラヴェリア,Brother，got a minute?<br> ,,vc_10200100001_027_01
+message,ラヴェリア,Anh ơi‚ rảnh một chút không?<br> ,,vc_10200100001_027_01
 
 window,off
 wait,0.15
@@ -1152,7 +1152,7 @@
 asyncwait
 
 window,on,0.15
-message,<user>,Oh，Laveria? Sure，what's up?<br> 
+message,<user>,Ồ‚ Laveria à? Được thôi‚ có chuyện gì?<br> 
 
 window,off
 wait,0.15
@@ -1179,9 +1179,9 @@
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
 window,on,0.15
-message,ラヴェリア,Sorry to interrupt when you're busy. There was a report from the<br>reconnaissance unit that went to the Abyss.<br> ,,vc_10200100001_028_01
-
-message,<user>,Oh，I heard about it. You came to deliver it yourself，Laveria?<br> 
+message,ラヴェリア,Xin lỗi vì làm gián đoạn khi anh đang bận. Có báo cáo từ đội trinh sát<br>được cử đi Đại Huyệt.<br> ,,vc_10200100001_028_01
+
+message,<user>,Ồ‚ anh nghe rồi. Em tự mang đến tận nơi báo cáo sao‚ Laveria?<br> 
 
 charaface,chara_1,FaceFun
 
@@ -1189,7 +1189,7 @@
 
 asynccharareaction,chara_1,Nod,1,STOP
 asynccharaemo,chara_1,Laugh,STOP
-message,ラヴェリア,And to see your face while I was at it.<br> ,,vc_10200100001_029_01
+message,ラヴェリア,Và nhân tiện ghé thăm anh luôn.<br> ,,vc_10200100001_029_01
 
 window,off
 wait,0.15
@@ -1214,18 +1214,18 @@
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
 window,on,0.15
-message,ラヴェリア,As for the Abyss，there's been nothing unusual since the last<br>operation.<br> ,,vc_10200100001_030_01
-
-message,<user>,I see，that's a relief. But there's still a lot we don't know about the<br>Abyss，so we need to stay on alert for any sudden activity.<br> 
+message,ラヴェリア,Còn về Đại Huyệt‚ kể từ chiến dịch lần trước đến giờ không có gì bất<br>thường.<br> ,,vc_10200100001_030_01
+
+message,<user>,Anh hiểu‚ thật nhẹ nhõm. Nhưng vẫn còn nhiều điều chúng ta chưa rõ về<br>Đại Huyệt‚ nên cần cảnh giác với mọi hoạt động đột xuất.<br> 
 
 charaface,chara_1,FaceSad
 
 asyncseplay,setag1_47,se4800008,0,1,CONT
 
 asynccharaemo,chara_1,Sweat,STOP
-message,ラヴェリア,That's why you look so tired，Brother—because you're always on<br>guard for so many things.<br> ,,vc_10200100001_031_01
-
-message,<user>,...Was my tired expression that obvious?<br> 
+message,ラヴェリア,Đó là lý do trông anh mệt mỏi thế đấy‚ anh—vì anh lúc nào cũng cảnh<br>giác với quá nhiều chuyện.<br> ,,vc_10200100001_031_01
+
+message,<user>,...Biểu cảm mệt mỏi của anh lộ rõ đến thế sao?<br> 
 
 charaface,chara_1,FaceFun
 
@@ -1233,10 +1233,10 @@
 
 asynccharareaction,chara_1,Nod,1,STOP
 asynccharaemo,chara_1,Laugh,STOP
-message,ラヴェリア,I'm good at looking after my comrades. Believe it or not，I'm someone<br>people rely on in Lux Nova.<br> ,,vc_10200100001_032_01
-
-
-message,<user>,I see，so you're like a big sister to them. Well，I'm just busy with<br>paperwork. Nothing to worry about.<br> 
+message,ラヴェリア,Em giỏi chăm sóc đồng đội mà. Tin hay không thì‚ em cũng là người mà<br>mọi người ở Lux Nova luôn tin cậy.<br> ,,vc_10200100001_032_01
+
+
+message,<user>,Anh hiểu‚ ra em như một người chị cả với bọn họ. À‚ anh chỉ đang bận<br>với mấy vụ giấy tờ thôi. Không có gì đáng lo.<br> 
 
 window,off
 wait,0.15
@@ -1269,11 +1269,11 @@
 
 asynccharareaction,chara_5,Nod,1,STOP
 window,on,0.15
-message,アリシア,Yes，if we get through these next few days，we'll be fine. Let's work<br>hard together，Commander...!<br> ,,vc_10200100001_033_01
+message,アリシア,Vâng‚ nếu chúng ta vượt qua được mấy ngày tới thì sẽ ổn thôi. Cùng nhau<br>cố gắng nhé‚ Chỉ Huy...!<br> ,,vc_10200100001_033_01
 
 charaface,chara_1,EyeOpen
 charaface,chara_1,FaceNormal
-message,<user>,*sigh*... it's going to take days just to process the paperwork!<br> 
+message,<user>,*thở dài*... chỉ riêng xử lý mấy tờ giấy này cũng mất cả mấy ngày!<br> 
 
 
 charaface,chara_5,FaceSad
@@ -1283,7 +1283,7 @@
 asynccharaemo,chara_5,Panic,CONT
 
 asyncshake,CHARA,chara_5,20,15,0.5,6,on,off,0,off,CONT,0
-message,アリシア,I-I'll help as much as I can! Let's sort through them little by little!<br> ,,vc_10200100001_034_01
+message,アリシア,E-em sẽ giúp hết sức mình! Chúng ta cùng dọn dẹp chúng từng chút một nhé!<br> ,,vc_10200100001_034_01
 
 window,off
 wait,0.15
@@ -1307,7 +1307,7 @@
 
 asynccharaemo,chara_1,Speak,STOP
 window,on,0.15
-message,ラヴェリア,Hmm，what's got you in trouble? If it's something I'm allowed to<br>know，tell me about it.<br> ,,vc_10200100001_035_01
+message,ラヴェリア,Ừm‚ chuyện gì làm anh rắc rối vậy? Nếu là chuyện em được phép<br>biết thì kể cho em nghe đi.<br> ,,vc_10200100001_035_01
 
 window,off
 wait,0.15
@@ -1344,7 +1344,7 @@
 
 asynccharaemo,chara_5,Sweat,STOP
 window,on,0.15
-message,アリシア,Actually，we've got a backlog of formal operation reports that need<br>to go to each country... Only the Commander can handle these.<br> ,,vc_10200100001_036_01
+message,アリシア,Thực ra‚ chúng em đang tồn đọng một đống báo cáo chiến dịch chính thức cần<br>gửi sang từng quốc gia... Chỉ có Chỉ Huy mới xử lý được mấy cái này.<br> ,,vc_10200100001_036_01
 
 asyncwait
 
@@ -1355,10 +1355,10 @@
 asyncseplay,setag1_51,se4800006,0,1,CONT
 
 asynccharaemo,chara_5,Trouble,STOP
-message,アリシア,Since we're receiving supplies，funds，and military support，we need<br>to share accurate information with them...<br> ,,vc_10200100001_037_01
-
-
-message,<user>,We don't need to fudge the content this time，so I could just report it<br>as-is... but...<br> 
+message,アリシア,Bởi vì chúng ta đang nhận vật tư‚ tiền bạc‚ và viện trợ quân sự nên cần<br>chia sẻ thông tin chính xác với họ...<br> ,,vc_10200100001_037_01
+
+
+message,<user>,Lần này không cần làm mờ nội dung đâu‚ nên anh cứ báo cáo y nguyên<br>như thế... nhưng mà...<br> 
 
 asynccharareaction,chara_5,Nod,1,CONT
 
@@ -1374,7 +1374,7 @@
 charaface,chara_1,FaceNormal
 
 
-message,<user>,All the people who are good with this kind of paperwork are out in<br>the field... The thought of having to do all this alone... *sigh*<br> 
+message,<user>,Tất cả những người giỏi vụ giấy tờ này đều đang đi ngoài tiền tuyến hết<br>rồi... Nghĩ đến chuyện phải một mình làm hết đống này... *thở dài*<br> 
 
 window,off
 wait,0.15
@@ -1412,10 +1412,10 @@
 
 asynccharareaction,chara_1,Nod,1,STOP
 window,on,0.15
-message,ラヴェリア,I see... I've got an idea of someone who could help.<br> ,,vc_10200100001_038_01
+message,ラヴェリア,Em hiểu... em đã nghĩ ra một người có thể giúp được.<br> ,,vc_10200100001_038_01
 
 charaface,chara_5,FaceSurprise
-message,<user>,Really? Who? What unit are they from?<br> 
+message,<user>,Thật sao? Là ai? Thuộc đơn vị nào?<br> 
 
 window,off
 wait,0.15
@@ -1443,7 +1443,7 @@
 
 asynccharaface,chara_1,FaceHappy,STOP,6.5
 window,on,0.15
-message,ラヴェリア,Fufu，it's me. Before I came here，I did office work. These kinds of<br>reports are a piece of cake.<br> ,,vc_10200100001_039_01
+message,ラヴェリア,Hì hì‚ là em chứ ai. Trước khi đến đây‚ em làm công việc văn phòng. Mấy<br>báo cáo kiểu này với em thì dễ như trở bàn tay.<br> ,,vc_10200100001_039_01
 
 window,off
 wait,0.15
@@ -1453,7 +1453,7 @@
 charaface,chara_5,EyeOpen
 charaface,chara_5,FaceNormal
 window,on,0.15
-message,<user>,Bingo! A beauty who can fight and handle paperwork，right here!<br> 
+message,<user>,Trúng phóc! Một mỹ nữ vừa biết đánh vừa giỏi giấy tờ‚ ngay tại đây!<br> 
 
 linework,off,White,Middle
 
@@ -1464,7 +1464,7 @@
 asynccharaemo,chara_1,Shock,STOP
 
 asyncshake,CHARA,chara_1,20,15,0.5,6,on,off,0,off,CONT,0
-message,ラヴェリア,B-beauty?<br> ,,vc_10200100001_040_01
+message,ラヴェリア,C-cái gì‚ mỹ nữ?<br> ,,vc_10200100001_040_01
 
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
@@ -1472,9 +1472,9 @@
 asyncseplay,setag1_57,se4800012,0,1,CONT
 
 asynccharaemo,chara_1,Shy,STOP
-message,ラヴェリア,Wh-what... Brother，you're saying that again...<br> ,,vc_10200100001_041_01
-
-message,<user>,Secure her，Alicia! Prepare tea and sweets! Don't let her escape!<br> 
+message,ラヴェリア,Ơ... anh lại nói thế nữa à...<br> ,,vc_10200100001_041_01
+
+message,<user>,Bắt giữ cô ấy‚ Alicia! Chuẩn bị trà và bánh ngọt đi! Tuyệt đối đừng để cô ấy trốn thoát!<br> 
 
 window,off
 wait,0.15
@@ -1511,7 +1511,7 @@
 
 asynccharaemo,chara_5,Question,CONT,2
 window,on,0.15
-message,アリシア,Yes，Commander! But are you sure it's okay，Laveria?<br> ,,vc_10200100001_042_01
+message,アリシア,Vâng‚ Chỉ Huy! Nhưng ngài chắc chắn ổn chứ‚ Laveria?<br> ,,vc_10200100001_042_01
 
 asyncwait
 
@@ -1522,7 +1522,7 @@
 asynccharareaction,chara_1,Nod,1,STOP
 asynccharaemo,chara_1,Laugh,STOP
 
-message,ラヴェリア,It's fine. I'm planning to stay here for a while anyway. I'll help if<br>you're in a bind.<br> ,,vc_10200100001_043_01
+message,ラヴェリア,Không sao. Em định ở lại đây một thời gian rồi. Nếu anh túng thiếu<br>thì em sẽ giúp.<br> ,,vc_10200100001_043_01
 
 charapose,chara_5,3
 
@@ -1535,7 +1535,7 @@
 
 asynccharaface,chara_5,EyeOpen,STOP,1
 asynccharaface,chara_5,FaceNormal,STOP,1
-message,アリシア,We really appreciate it，but if you have other things to do at the<br>Frontline Base，please prioritize those，okay?<br> ,,vc_10200100001_044_01
+message,アリシア,Bọn em thực lòng biết ơn‚ nhưng nếu chị có việc khác ở Căn Cứ Tiền Tuyến<br>thì cứ ưu tiên việc đó nhé‚ được không?<br> ,,vc_10200100001_044_01
 
 charaface,chara_1,FaceShy
 
@@ -1544,17 +1544,17 @@
 asynccharaemo,chara_1,Shy,STOP
 
 asyncshake,CHARA,chara_1,20,0,0.5,1,off,off,0,off,CONT,0
-message,ラヴェリア,Business...? Nothing，really. Just a whim，I suppose.<br> ,,vc_10200100001_045_01
+message,ラヴェリア,Công việc à...? Không có gì‚ thật sự. Chỉ là một cơn bốc đồng thôi‚ em nghĩ vậy.<br> ,,vc_10200100001_045_01
 
 charaface,chara_1,EyeOpen
 charaface,chara_1,FaceNormal
 
-message,<user>,Then I'm begging you! Help us out right now! With just Alicia and me，<br>we'll end up working all night!<br> 
+message,<user>,Thế thì anh van em đấy! Giúp anh ngay bây giờ đi! Chỉ có một mình Alicia<br>và anh thôi‚ thế nào cũng làm xuyên đêm mất!<br> 
 
 charaface,chara_1,FaceFun
 
 asyncjump,CHARA,chara_1,-30.6,0.5,1,off,0,CONT
-message,ラヴェリア,Alright，alright，I get it. Then Alicia，just pass me the documents I'm<br>allowed to see，okay?<br> ,,vc_10200100001_046_01
+message,ラヴェリア,Được rồi‚ được rồi‚ em hiểu rồi. Thế thì Alicia‚ cứ đưa em những tờ giấy<br>em được phép xem thôi nhé‚ được không?<br> ,,vc_10200100001_046_01
 
 charapose,chara_5,1
 
@@ -1564,7 +1564,7 @@
 
 asynccharareaction,chara_5,Nod,1,STOP
 asynccharaemo,chara_5,Laugh,STOP
-message,アリシア,Of course! We're counting on you，Laveria!<br> ,,vc_10200100001_047_01
+message,アリシア,Tất nhiên rồi! Bọn em trông cậy vào chị đấy‚ Laveria!<br> ,,vc_10200100001_047_01
 
 window,off
 bgmstop,bgmtag1_4,0.5
```
