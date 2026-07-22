import re
BASE='E:/AgentTranslation/'
EN_PATH=BASE+'Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100002.txt'
VI_PATH=BASE+'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100002.txt'

# VI full field text. For 'message,' include internal <br> and trailing '<br> ' suffix exactly matching EN <br> count.
# For 'title,' just the text (no suffix). Commas inside VI use U+201A ,
C='\u201a'  # low-9 comma
VI={
 1:'Hô'+C+' Hôm Nay Trời Đẹp Nhỉ!',
 2:'(Rốt cuộc mình vẫn chưa kịp xác nhận tình hình của Hayley cùng mọi người mà đã phải lên đường mất rồi.)<br> ',
 3:'(...Ơ? Đó chẳng phải người lính hôm qua<br>ở cùng đội với Hayley hay sao.)<br> ',
 4:'Giọng điệu của Hayley hôm nay khác hẳn ấy nhỉ.<br> ',
 5:'Ừ. Không biết đã xảy ra chuyện gì nữa.<br> ',
 6:'Ờ'+C+' à mà'+C+' cho tôi hỏi một chút thôi'+C+' được không ạ?<br> ',
 7:'Hayley!? Sao thế? Cậu có việc gì với tôi à?<br> ',
 8:'Ơ'+C+' ừm thì... hô'+C+' hôm nay trời đẹp nhỉ!?<br> ',
 9:'...Ở đây là Đại Huyệt nên tôi chịu không biết thời tiết bên ngoài thế nào...<br>Trước lúc xuất phát trời chẳng phải đang u ám sao?<br> ',
 10:'...Đ'+C+' đúng vậy nhỉ?<br> ',
 11:'…………<br> ',
 12:'…………<br> ',
 13:'(...Này'+C+' câu chuyện tắc ngóm luôn rồi kìa.)<br> ',
 14:'A! À'+C+' sở thích của anh là gì ạ!?<br> ',
 15:'(Đây là buổi xem mắt à!?)<br> ',
 16:'...Nếu bắt buộc phải nói thì... cắt móng tay?<br> ',
 17:'(Đó mà là sở thích sao?)<br> ',
 18:'Th'+C+' thích thật đấy ạ~. Lần tới cho em xem thử được không...?<br> ',
 19:'Nghe rợn cả người luôn đấy nhé!?<br> ',
 20:'(...Căng thẳng đến cứng đờ'+C+' đến mức chẳng biết mình đang nói gì nữa<br>—cô Hayley đường hoàng của hôm qua biến đi đâu mất rồi?)<br> ',
 21:'Ơ'+C+' ừm... ừm...<br> ',
 22:'Gì thế? Nếu có điều muốn nói thì cứ nói thẳng ra giúp mình đi...<br> ',
 23:'Thôi nào'+C+' đợi đã mọi người.<br> ',
 24:'Hử? ...Chỉ Huy?<br> ',
 25:'Tôi là gã được cậu ấy công nhận là hiểu chuyện nhanh đây. Để tôi nói chuyện riêng với cô ấy một lát.<br>...Hayley. Em đi cùng anh nhé?<br> ',
 26:'V'+C+' vâng... Nhờ anh ạ.<br> ',
 27:'...C'+C+' cảm ơn anh'+C+' Chỉ Huy. V'+C+' vì đã cứu em...<br> ',
 28:'Đừng bận tâm. ...Mà trước khi nói'+C+' anh xác nhận chút đã:<br>Hayley bây giờ là con người thật'+C+' không tô vẽ gì'+C+' đúng không?<br> ',
 29:'...Vâng'+C+' đúng vậy ạ.<br> ',
 30:'Anh hiểu rồi. Vậy em đột nhiên đổi lại giọng nói bình thường<br>là vì hôm qua bị người hầu cận nói gì đó phải không?<br> ',
 31:'...Vâng.<br> ',
 32:'Ra vậy—sao lại thành ra như thế? Mọi người đều bối rối'+C+' còn em<br>chắc cũng thấy khó xử. Vì sao em lại đổi cách nói chuyện?<br> ',
 33:'Th'+C+' thế thì'+C+' để giải thích điều đó'+C+' em cần phải kể vì sao mình bắt đầu<br>nói năng như hôm qua'+C+' nhưng mà...<br> ',
 34:'...S'+C+' sẽ dài dòng lắm đấy ạ?<br> ',
 35:'Không sao. Việc em cứ gò bó thế này mới là vấn đề. Kể anh nghe đi.<br> ',
 36:'Hây... Cảm ơn anh đã tử tế như vậy. V'+C+' vậy thì em xin kể từ<br>thời thơ ấu của mình'+C+' theo thứ tự nhé—<br> ',
 37:'N'+C+' nói ra thì hơi ngượng'+C+' nhưng mà—<br>em sinh ra là người kế vị ngai vàng của một quốc gia nọ'+C+' tiểu thư của một gia tộc quý tộc.<br> ',
 38:'Hô. Đám lính có xì xào rằng "Hayley trông không nghèo khó gì"'+C+'<br>hóa ra là thật à. Sao em phải giấu?<br> ',
 39:'À'+C+' cái đó thì... phải nói là do em có niềm tin riêng rằng<br>một anh hùng nên biết ẩn mình chờ thời...<br> ',
 40:'À~'+C+' ra vậy... thì ra là thế. Em kể tiếp đi.<br> ',
 41:'V'+C+' vâng... T'+C+' từ nhỏ'+C+' em đã theo công việc của cha<br>mà chu du khắp các nơi ở Treslia.<br> ',
 42:'Em đã đi qua Milesgard'+C+' Perdion'+C+' Eldorana... tầm mắt mở rộng ra'+C+'<br>nhưng đ'+C+' đổi lại'+C+' em đánh mất cơ hội có được bạn bè...<br> ',
 43:'N'+C+' nhưng đâu phải là chẳng có niềm vui nào. Ánh sáng đối với em<br>chính là những người hát rong cũng chu du khắp nơi như em...!<br> ',
 44:'Thật hay hư—những khúc anh hùng ca họ kể đã khiến em say mê.<br>Và... h'+C+' họ đã gieo vào lòng em niềm khát khao trở thành anh hùng...!<br> ',
 45:'Hừm... vậy ra việc em tự xưng là anh hùng bắt nguồn từ chuyện đó.<br> ',
 46:'V'+C+' vâng. Lớn lên trong sự ngưỡng mộ những câu chuyện người hát rong kể'+C+'<br>em còn gặp thêm một thứ nữa ảnh hưởng lớn đến mình...<br> ',
 47:'Đó là sách...! Thời thiếu nữ'+C+' em mê mẩn những tiểu thuyết kỳ ảo<br>lấy anh hùng làm nhân vật chính... nhất là thể loại gọi là dark fantasy!<br> ',
 48:'Chỉ Huy'+C+' a'+C+' anh có hứng thú với loại tiểu thuyết ấy không...?<br> ',
 49:'Ừ thì'+C+' anh cũng là đàn ông mà. Anh cũng đọc qua loại thường thường rồi.<br> ',
 50:'V'+C+' vậy thì chắc anh hiểu được đôi chút'+C+'<br>mấy cái đó cựcccc kỳ ngầu phải không ạ!?<br> ',
 51:'...Ồ'+C+' ồ?<br> ',
 52:'Một nhân vật chính mang trong mình cả bóng tối lẫn ánh sáng—liệu sẽ vẫn<br>là tồn tại rực rỡ'+C+' hay sẽ sa ngã mà trở thành kẻ ác!!<br> ',
 53:'Hoặc cả hình ảnh chao đảo giữa bóng tối và ánh sáng'+C+'<br>chấp nhận chính mình như vốn có—như thế cũng được luôn!<br> ',
 54:'Hai thuộc tính trái ngược cùng tồn tại trong một người—một sự hài hòa<br>bất thường giữa cán cân điên loạn... Cái đó không phải bằng lý lẽ'+C+' mà khiến ta ngưỡng mộ đến khát khao!!<br> ',
 55:'…………<br> ',
 56:'Á!? X'+C+' xin lỗi'+C+' em lỡ mất kiểm soát... Anh chẳng hiểu gì đâu nhỉ...?<br> ',
 57:'À'+C+' không'+C+' anh chỉ hơi bất ngờ chút thôi. Em yên tâm.<br>...Thật lòng thì'+C+' điều em muốn nói'+C+' anh hiểu được đôi chút đấy.<br> ',
 58:'Hô hô hô'+C+' th'+C+' thật ạ~!?<br> ',
 59:'Ừ. Mấy thứ đó khiến người ta rạo rực nhỉ.<br>Nếu ở Đại Huyệt mà nhặt được thanh kiếm phủ ngọn lửa màu bóng tối'+C+' chắc anh cũng muốn có đấy.<br> ',
 60:'Ở Đại Huyệt có thứ như vậy sao ạ!?<br> ',
 61:'Không thể nói là không có. ...Lãng mạn đấy chứ.<br> ',
 62:'Haaa... Nếu có được thì nhất định phải cho em xem đấy... Đúng là món đồ khiến người ta thèm nhỏ dãi...<br> ',
 63:'Vậy'+C+' sau khi mê dark fantasy rồi thì sao?<br> ',
 64:'A... v'+C+' vâng. Được anh hùng ca và dark fantasy truyền cảm hứng'+C+' em<br>quyết tâm trở thành anh hùng của muôn dân... nên b'+C+' bắt đầu rèn luyện kiếm thuật.<br> ',
 65:'Cha mẹ em không phản đối à? Một gia tộc quý tộc để con gái học kiếm<br>rồi ra chiến trường... anh thấy cần khá nhiều can đảm đấy—<br> ',
 66:'À'+C+' vốn dĩ cha mẹ em theo quan niệm "Đã là quý tộc thì phải có ích cho dân"<br>nên... Săn quái vật là vì đời vì người... đúng không ạ?<br> ',
 67:'V'+C+' việc hướng đến làm anh hùng vừa là để hoàn thành trách nhiệm của người<br>sinh ra trong dòng dõi quý tộc'+C+' vừa để thực hiện lý tưởng em ngưỡng mộ từ nhỏ đến lớn!<br> ',
 68:'...Anh hùng đi săn quái vật và thế giới quan dark fantasy. Hình mẫu lý tưởng<br>dung hợp cả hai—đó chính là em mà anh thấy hôm qua ở Đại Huyệt.<br> ',
 69:'V'+C+' vâng! Em cũng tình nguyện đến Đại Huyệt để thảo phạt quái vật<br>và hoàn thành trách nhiệm của mình...!<br> ',
 70:'Nếu vậy thì anh càng thấy khó hiểu. Vì sao em bắt đầu nói năng bình thường?<br>Hôm qua người hầu cận cũ đã nói gì với em?<br> ',
 71:'Hức... à'+C+' cái đó'+C+' ông ấy bảo rằng làm một n'+C+' nữ vương tương lai'+C+'<br>em phải trở thành một con người đàng hoàng—<br> ',
 72:'R'+C+' rằng nếu em không cư xử cho xứng với người dẫn dắt kẻ khác<br>thì sẽ chẳng ai đi theo em... ông ấy đã mắng em như thế đấy...<br> ',
 73:'K'+C+' không chỉ vậy... ông ấy còn nói nếu em không chăm chỉ lập công<br>ở Căn Cứ Tiền Tuyến thì sẽ đưa em về nước...<br> ',
 74:'Hả? Nhưng cha mẹ em có phản đối đâu'+C+' đúng không?<br> ',
 75:'Đ'+C+' đúng vậy'+C+' nhưng ông Jiiya—người hầu cận cũ đó giờ đang<br>giữ chức tể tướng nên... chắc cha em cũng không cứng rắn được...<br> ',
 76:'Ra vậy. Kiểu như nỗi khổ riêng của hoàng tộc—thật gian nan.<br> ',
 77:'...Nhưng'+C+' c'+C+' cũng đành thôi. Vì điều ông Jiiya nói cũng đâu có sai...<br> ',
 78:'Th'+C+' thật ra'+C+' em từng bị cô lập đấy... Dù đã đổi lại cách nói bình thường<br>mà vẫn không ổn'+C+' cái đó thì'+C+' quả là'+C+' hơi ngoài dự đoán...<br> ',
 79:'Hừm... Hay để anh giải thích tình hình cho mọi người và làm trung gian giúp em?<br> ',
 80:'...Đ'+C+' đó là lời đề nghị vô cùng đáng quý... nhưng em xin nhận tấm lòng thôi ạ.<br>Cứ dựa dẫm mãi thì... em sẽ không thành nữ vương tốt hay anh hùng được... đâu.<br> ',
 81:'Anh hiểu rồi. Thôi'+C+' nếu cần giúp thì cứ bàn với anh bất cứ lúc nào.<br> ',
 82:'A'+C+' cảm ơn anh... Chỉ Huy...<br> ',
 83:'...Chỉ Huy'+C+' a'+C+' anh tốt bụng thật đấy.<br>Cứ như một anh hùng bước ra từ truyện fantasy chính thống vậy...<br> ',
 84:'Haha. Anh đâu tốt đẹp đến thế. Anh chẳng phải gã trong sáng gì đâu.<br>Có khi anh gần với nhân vật chính dark fantasy hơn đấy?<br> ',
 85:'...V'+C+' vậy thì'+C+' nếu đúng thế'+C+' em cũng thấy vui lắm ạ.<br> ',
 86:'Hử...?<br> ',
 87:'A'+C+' ơ'+C+' kh'+C+' không có gì đâu ạ...!<br> ',
 88:'...N'+C+' nhưng mà'+C+' em thật lòng cảm ơn anh rất nhiều.<br>K'+C+' không chỉ vì anh vừa lắng nghe em—<br> ',
 89:'M'+C+' mà cả việc hôm qua anh nghe em kể về thế giới quan của mình...<br>Em đã... vui lắm.<br> ',
 90:'...Nghĩ đến chuyện không được nghe nữa'+C+' anh thấy hơi buồn đấy.<br>Khi nào em muốn có người nghe thì cứ gọi anh nhé.<br> ',
 91:'...T'+C+' thôi mà'+C+' như thế không công bằng đâu.<br>Anh nói vậy thì em lại muốn làm nũng mất—<br> ',
 92:'GỪOOOOOOÀ!!<br> ',
 93:'Oẹ!?<br>C'+C+' cái gì vừa rồi vậy!?<br> ',
 94:'Từ phía đơn vị đang đóng quân đó!<br>Mau quay về thôi!<br> ',
}

raw=open(EN_PATH,'rb').read().decode('utf-8-sig')
has_crlf=b'\r\n' in open(EN_PATH,'rb').read()
lines=raw.split('\r\n')
TEXT_CMDS=('title,','message,','messageTextUnder,','messageTextCenter,')
seq=0
errs=[]
out=[]
for ln in lines:
    if ln.startswith('title,'):
        seq+=1
        vi=VI[seq]
        out.append('title,'+vi)
        # title has no <br> normally
    elif ln.startswith('message,') or ln.startswith('messageTextUnder,') or ln.startswith('messageTextCenter,'):
        seq+=1
        parts=ln.split(',')
        old_tf=parts[2]
        vi=VI[seq]
        if vi.count('<br>')!=old_tf.count('<br>'):
            errs.append(f'#{seq} BR mismatch en={old_tf.count("<br>")} vi={vi.count("<br>")} :: {vi[:40]}')
        # ASCII comma guard on the pure text (excluding delimiters): vi is the field
        if ',' in vi:
            errs.append(f'#{seq} ASCII comma in vi')
        parts[2]=vi
        out.append(','.join(parts))
    else:
        out.append(ln)

assert seq==94, seq
if errs:
    print('ERRORS:')
    print('\n'.join(errs))
    raise SystemExit(1)

text='\r\n'.join(out)
open(VI_PATH,'wb').write(b'\xef\xbb\xbf'+text.encode('utf-8'))
print('WROTE',VI_PATH,'records',seq)
