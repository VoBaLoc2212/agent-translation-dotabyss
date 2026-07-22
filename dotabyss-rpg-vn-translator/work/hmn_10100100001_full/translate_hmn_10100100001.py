# -*- coding: utf-8 -*-
"""Generate Vietnamese Dot Abyss asset translation for hmn_10100100001."""
from __future__ import annotations
import json, hashlib, re, difflib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10100100001'
SRC = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
OUT = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work/hmn_10100100001_full'
JP_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
TEXT_CMDS = {'title','message','messageTextUnder','messageTextCenter'}

TRANSLATIONS = {
"タイトル": "Tiêu Đề",
"人類の最前線であり、災厄を塞き止める最後の砦。<br>前線基地の街は今――祭りの真っ最中だった。": "Là tuyến đầu của nhân loại và pháo đài cuối cùng ngăn chặn tai ương.<br>Thành phố căn cứ tiền tuyến lúc này――đang giữa mùa lễ hội.",
"それでは皆さん！<br>待ちに待った狩猟コンテストを開催いたしまーす！": "Vậy thì thưa mọi người!<br>Cuộc thi săn bắt mà chúng ta hằng mong đợi xin được bắt đầu!",
"集った多くの住人の前で、アリシアは高らかに宣言した。": "Trước đông đảo cư dân tụ họp‚ Alicia cất cao giọng tuyên bố.",
"ついに始まったね、狩猟コンテスト！<br>みんなでたっくさん楽しめたらいいな～♪": "Cuối cùng cũng bắt đầu rồi nhỉ‚ cuộc thi săn bắt!<br>Ước gì mọi người cùng vui thật là vui～♪",
"兵たちの士気を高めるために開催したイベントだ。<br>バチバチに競い合って盛り上がってくれればいいんだが……": "Đây là sự kiện được tổ chức để nâng cao sĩ khí binh lính.<br>Hy vọng mọi người cạnh tranh thật bùng nổ rồi khuấy động không khí lên……",
"ええ～？　みんなで楽しめればそれが一番でしょ！<br>勝ち負けなんてついでついでっ♪": "Ể～? Mọi người cùng vui mới là nhất chứ!<br>Thắng thua chỉ là chuyện phụ thôi‚ phụ thôi♪",
"そう言ってるディアーナが優勝候補だからなぁ……": "Người nói vậy lại chính là ứng viên vô địch như Diana mà……",
"狩猟コンテストとは、ハンターの皆さんに最高の食材を狩ってもらい<br>それを使った料理を提供していただきまして……": "Cuộc thi săn bắt là nơi các thợ săn sẽ săn về những nguyên liệu thượng hạng nhất<br>rồi dùng chúng để chiêu đãi các món ăn……",
"この厳格な審査員であるアリシアがっ！<br>公平に味の採点をおこない、優勝者を決めるというコンテストですっ！": "Và vị giám khảo nghiêm khắc Alicia này!<br>Sẽ chấm điểm hương vị thật công bằng rồi quyết định người chiến thắng!",
"う～ん、楽しみ！<br>狩りだけじゃなくて、料理の味まで楽しめちゃう！": "Ư～m‚ háo hức quá!<br>Không chỉ được xem đi săn mà còn được thưởng thức cả mùi vị món ăn nữa!",
"狩って終わりじゃ見てる人はあんまり参加できないけど、<br>料理を振る舞えるならみんなが楽しいもんねっ！": "Nếu chỉ săn xong là hết thì người xem khó tham gia cùng‚<br>nhưng nếu có thể đãi món ăn thì ai cũng vui mà!",
"素敵なルールだね、司令官くん。<br>キミが考えたんだよね～？": "Luật hay thật đấy‚ Chỉ Huy.<br>Là cậu nghĩ ra đúng không～?",
"あ、ああ。せっかくなら美味い飯が食いたいってだけの理由なんだが、<br>妙に好評みたいで嬉しいぞ、うん。": "À‚ ừ. Lý do chỉ là hiếm có dịp thì anh muốn ăn món ngon thôi‚<br>nhưng có vẻ lại được hưởng ứng lạ thường nên anh cũng vui‚ ừm.",
"そして参加者の皆さんには、相性とバランスを考えて選んだ<br>２人１組のチームで戦っていただきます～！": "Và các thí sinh sẽ thi đấu theo đội hai người<br>được chọn dựa trên độ ăn ý và cân bằng～!",
"では、まず１組目！<br>前線基地からエントリーしてくださった――": "Vậy thì đội đầu tiên!<br>Đăng ký từ căn cứ tiền tuyến――",
"アリシアは参加者の名前を読み上げ、どんどんチームが組まれていく。<br>参加者の多くは強者の風格を見せるベテランのハンターたちだ。": "Alicia đọc tên từng thí sinh và các đội lần lượt được ghép lại.<br>Phần lớn người tham gia là các thợ săn kỳ cựu toát lên khí chất của kẻ mạnh.",
"あ……知ってる人が呼ばれた。腕利きのハンターだよ。<br>すごい人がたくさんで盛り上がるな～！": "A…… có người quen được gọi kìa. Đó là một thợ săn rất cừ đấy.<br>Nhiều người lợi hại thế này chắc sẽ náo nhiệt lắm～!",
"その中でも一番なのがディアーナなんだろう？": "Và trong số đó Diana mới là người đứng đầu đúng không?",
"えぇ？　ボクなんて普通だよ、普通。<br>すごいハンターなんてたくさんいるんだから。": "Ể? Tôi chỉ bình thường thôi‚ bình thường mà.<br>Có rất nhiều thợ săn đáng gờm cơ đấy.",
"自覚は持ってほしいんだけどな……。<br>しかし、なかなかディアーナの名前が呼ばれないな。": "Anh muốn em tự giác nhận ra điều đó hơn cơ……<br>Nhưng mãi vẫn chưa thấy gọi tên Diana nhỉ.",
"そんな話題を出したところで、<br>ふとアリシアがこちらに視線を向ける。": "Đúng lúc câu chuyện vừa nhắc đến chuyện ấy‚<br>Alicia chợt hướng mắt về phía này.",
"そして最後のチーム。１人目は、ディアーナさん！": "Và đội cuối cùng. Người thứ nhất là Diana!",
"あ、呼ばれた！　ボクのパートナーは誰かなっ？": "A‚ được gọi rồi! Bạn đồng đội của tôi sẽ là ai đây?",
"腕利きだといいな。<br>ま、誰が相手でもディアーナならやれるだろうが。": "Hy vọng là người có bản lĩnh.<br>Mà dù ghép với ai thì Diana cũng xoay xở được thôi.",
"ディアーナさんは狩猟の腕前が素晴らしいと評判で、<br>普通のハンターと組んだ場合、バランスが悪くなると判断しました。": "Diana nổi tiếng vì tài săn bắn xuất sắc‚<br>nên chúng tôi nhận định nếu cô ấy ghép với thợ săn bình thường thì sẽ mất cân bằng.",
"そこで――ハンデとして！<br>前線基地の司令官とチームを組んでいただきますっ！": "Vì vậy――để làm điểm chấp!<br>Cô ấy sẽ lập đội với Chỉ Huy của căn cứ tiền tuyến!",
"はああぁぁっ！？　俺はエントリーなんてしてないぞ！？　<br>どうして出なきゃいけないんだっ！？": "Hảảảảả!? Anh có đăng ký đâu chứ!? <br>Tại sao anh lại phải tham gia!?",
"狩りに関しては完全な素人！　獲物はさばけないし料理も無理！<br>そんな足手まといをつけてやっと公平だという判断です！": "Hoàn toàn là tay mơ về săn bắn! Không biết xử lý con mồi‚ nấu ăn cũng chịu!<br>Gắn thêm một cục vướng víu như vậy mới công bằng!",
"お、俺が足手まとい！？<br>言いたい放題だな、おいっ！": "A‚ anh là cục vướng víu á!?<br>Nói quá đáng lắm rồi đấy!",
"この狩猟コンテストは、厳格かつ公平な審査員、アリシアがルールです！<br>異論は一切認めませんっ！": "Trong cuộc thi săn bắt này‚ giám khảo nghiêm khắc và công bằng Alicia chính là luật!<br>Tuyệt đối không chấp nhận phản đối!",
"どこが公平だーっ！？<br>絶対に優勝して見返してやるからなーっ！！！": "Công bằng chỗ nào hảー!?<br>Nhất định anh sẽ vô địch rồi cho cô sáng mắt raー!!!",
"というわけで、まもなくコンテストを開始します！<br>チームを組んだパートナーと交流を深めたり、作戦を考えてくださいね！": "Vậy nên cuộc thi sẽ sớm bắt đầu!<br>Hãy làm thân với đồng đội của mình hoặc cùng bàn chiến thuật nhé!",
"嘘だろ……のんびり飯だけ食うつもりだったのに、<br>俺も出場するのか……": "Không đùa chứ…… anh chỉ định thong thả ăn uống thôi mà‚<br>vậy mà anh cũng phải thi sao……",
"司令官くんがパートナーなんだね。<br>今日はよろしく～♪": "Chỉ Huy là bạn đồng đội của tôi nhỉ.<br>Hôm nay nhờ cậu nhé～♪",
"よろしく、じゃない！<br>何を気楽に言ってるんだ！": "Nhờ cậu cái gì chứ!<br>Sao em có thể nói nhẹ tênh như vậy!",
"えぇ～？　ボクは司令官くんと一緒で嬉しいけどな？": "Ể～? Tôi thì vui vì được đi cùng Chỉ Huy mà?",
"そりゃディアーナならどんなハンデがあっても関係ないだろうけど……": "Với Diana thì dù có điểm chấp nào cũng chẳng sao thật nhưng……",
"というか、誰がハンデだよ！<br>アリシアのやつ俺をお荷物扱いしやがって！": "Mà nói chứ‚ ai là điểm chấp hả!<br>Cái cô Alicia đó dám xem anh như gánh nặng!",
"絶対に負けられん。<br>なんとしてでも優勝してやる……！": "Tuyệt đối không thể thua.<br>Dù thế nào anh cũng phải giành chức vô địch……!",
"わ、やる気だね、司令官くん！<br>うんうん、今日は一緒に楽しも～♪": "Oa‚ Chỉ Huy hăng hái ghê!<br>Ừm ừm‚ hôm nay mình cùng vui nhé～♪",
"……もう少し怒れよ、ディアーナ。<br>自分で言うのも不本意だが、足手まといを押しつけられてるんだぞ。": "……Em nên giận thêm chút nữa đi‚ Diana.<br>Tự nói ra thì anh cũng không muốn đâu‚ nhưng em đang bị nhét cho một cục vướng víu đấy.",
"足手まといなんかじゃないよ。<br>狩りってね、とっても大変なんだから。": "Cậu không phải cục vướng víu đâu.<br>Săn bắn ấy mà‚ vất vả lắm đấy.",
"野外の１人歩きは危険だし、警戒にも苦労する。<br>獲物を狩ったら頑張って運ばなきゃいけないんだよ？": "Đi một mình ngoài hoang dã rất nguy hiểm‚ việc cảnh giới cũng không dễ.<br>Săn được con mồi rồi còn phải cố sức khuân về nữa cơ mà?",
"信頼できるパートナーが来てくれるのはすごく助かる。<br>キミと一緒で嬉しいよ、司令官くん♪": "Có một đồng đội đáng tin đi cùng sẽ giúp tôi rất nhiều.<br>Tôi vui vì được đi với cậu đấy‚ Chỉ Huy♪",
"ディアーナ……": "Diana……",
"それにね、狩りは大変なだけじゃない。<br>とっても楽しいんだ。": "Hơn nữa nhé‚ săn bắn không chỉ toàn vất vả đâu.<br>Nó vui lắm.",
"獲物の痕跡を探し、追い詰め、貫いたその瞬間の達成感！<br>その楽しさをキミと共有できるなんて、幸せだよ♪": "Cảm giác thành tựu khi lần theo dấu vết con mồi‚ dồn nó vào đường cùng rồi xuyên thủng nó!<br>Được chia sẻ niềm vui ấy với cậu thật hạnh phúc♪",
"ディアーナは勝利よりも楽しむことが大事か……": "Với Diana thì tận hưởng quan trọng hơn chiến thắng sao……",
"まあいい、それでこそ俺の腕の見せどころだ。<br>勝ってやるぞ……どんな手を使ってもな……！": "Thôi được‚ như vậy mới là lúc anh thể hiện bản lĩnh.<br>Anh sẽ thắng…… dù phải dùng bất cứ cách nào……!",
"さてっと。最初は狩りやすいのを狙おうか。<br>丁度いいのがいるみたいだし、ね。": "Nào. Đầu tiên ta nhắm con nào dễ săn nhé.<br>Hình như có một con vừa khéo ở kia đấy.",
"と、いうと？<br>俺には獲物らしき姿は見当たらないが……": "Ý em là sao?<br>Anh chẳng thấy bóng dáng con mồi nào cả……",
"んー、キミには見えないかな？<br>あっちのほうを飛んでるんだけど……": "Ưm‚ cậu không thấy à?<br>Nó đang bay ở đằng kia kìa……",
"飛んでる……？<br>まさかあの、ビーストヴァルチャーか！？": "Đang bay……?<br>Đừng nói là con Beast Vulture kia nhé!?",
"はるか上空で円を描いて飛ぶ、毛むくじゃらの鳥ビーストヴァルチャー。<br>その姿を指すと、ディアーナはぴょんと跳ねるように頷いた。": "Trên bầu trời xa tít‚ con chim xù lông Beast Vulture đang bay vòng tròn.<br>Khi anh chỉ vào nó‚ Diana gật đầu như nhảy cẫng lên.",
"そうそう！　食べる人は少ないけど、<br>意外と癖になる味をしてるんだ～。": "Đúng rồi đúng rồi! Ít người ăn nó lắm‚<br>nhưng mùi vị gây nghiện bất ngờ đấy～.",
"味の話ではなくて！<br>あんな遠くを飛んでる鳥をどうやって狩る気だよ！": "Anh đâu có nói chuyện mùi vị!<br>Em định săn con chim bay xa tít như thế bằng cách nào!",
"まさかディアーナなら<br>この距離でも簡単に当たるのか？": "Chẳng lẽ với Diana thì<br>khoảng cách này vẫn bắn trúng dễ dàng sao?",
"それは少し難しいかも？　風に乗る鳥はふわっと矢を避けたりするし。<br>でも、ちょっと工夫してあげれば……！": "Chuyện đó có lẽ hơi khó? Chim cưỡi gió đôi khi sẽ lướt tránh mũi tên.<br>Nhưng nếu khéo léo một chút thì……!",
"ディアーナは愛用の弓へ矢をつがえると、<br>上空に向けてギリリと引き絞った。": "Diana đặt mũi tên lên cây cung yêu thích‚<br>rồi kéo căng dây cung kèn kẹt hướng lên bầu trời.",
"ボクが放つのは飛雷の一矢……！<br>そーれぇっ！": "Thứ tôi phóng ra là một mũi tên phi lôi……!<br>Nàoー!",
"放たれた矢は大気を貫き、<br>まばゆい雷光をまとって天へと駆け昇る。": "Mũi tên được bắn ra xuyên qua không khí‚<br>khoác lấy ánh sét chói lòa rồi lao vút lên trời.",
"これは……すごい速度だなっ！　<br>しかし、本当に当たるのか……？": "Cái này…… tốc độ kinh thật! <br>Nhưng liệu có thật sự trúng không……?",
"当たらなくてもいいんだよ。<br>ほら、見てて。": "Không trúng cũng được mà.<br>Này‚ nhìn nhé.",
"ディアーナの放った雷の矢<br>大慌てで避けたビーストヴァルチャーの真横を通過した。": "Mũi tên sét do Diana bắn ra<br>vút ngang sát bên Beast Vulture đang hốt hoảng né tránh.",
"その瞬間、矢から放たれた電撃が獲物の体を痺れさせる。": "Ngay khoảnh khắc ấy‚ tia điện phóng ra từ mũi tên làm cơ thể con mồi tê liệt.",
"大成功～！　痺れて落ちてくるよ！": "Đại thành công～! Nó sẽ tê liệt rồi rơi xuống đấy!",
"ディアーナは落下地点に走り、<br>捕獲用の網を広げてビーストヴァルチャーを受け止めた。": "Diana chạy đến điểm rơi‚<br>giăng lưới bắt giữ ra và đỡ lấy Beast Vulture.",
"これで１匹目、だね♪": "Vậy là con thứ nhất rồi nhỉ♪",
"なるほどな……たとえ当たらなくとも、<br>雷の矢で叩き落とせるわけか……": "Ra là vậy…… dù không bắn trúng‚<br>em vẫn có thể dùng mũi tên sét đánh rơi nó……",
"相手が鳥だからこそ、だけどね。<br>空中ならちょっと痺れただけでも落ちちゃうから。": "Vì đối thủ là chim thôi nhé.<br>Ở trên không‚ chỉ cần hơi tê liệt là rơi xuống ngay mà.",
"見事に使いこなしてるな……さすがは凄腕ハンターだ。": "Em sử dụng thuần thục thật…… đúng là thợ săn cự phách.",
"もー、褒めすぎだよ、司令官くん。<br>じゃあ次を狙いにいこ～♪": "Thôi mà‚ Chỉ Huy khen quá lời rồi.<br>Vậy mình đi nhắm con tiếp theo nhé～♪",
"この辺りは獲物が多いんだ。小さいところならクレストラビット、<br>メインはグラスディアで、大物はアッシュボア！": "Khu này có nhiều con mồi lắm. Loại nhỏ thì có Crest Rabbit‚<br>chủ lực là Grass Deer‚ còn con lớn là Ash Boar!",
"となるとアッシュボアを狙いたいところだが……。<br>……ん？　あそこで水を飲んでるのは……？": "Vậy thì anh muốn nhắm Ash Boar……<br>……Hửm? Con đang uống nước ở kia là……?",
"ふと視線を向けた先。<br>水辺で一心不乱に水を飲む、燃えるように赤い狐の姿があった。": "Nơi anh chợt nhìn sang.<br>Bên mép nước có bóng một con cáo đỏ rực như lửa đang mải miết uống nước.",
"フレアフォックスだっ！<br>よく見つけたね、司令官くん！": "Là Flare Fox!<br>Chỉ Huy tìm giỏi thật đấy!",
"獲物、だな。しかし狙うには小さすぎたか。<br>狩ったところで意味がなさそうだ。": "Là con mồi nhỉ. Nhưng có vẻ quá nhỏ để nhắm đến.<br>Săn được cũng chẳng có ý nghĩa gì mấy.",
"ううん、小さいけど、あれはしっかり大人なんだよ。<br>首元のお肉が美味しいんだから♪": "Không đâu‚ nó nhỏ nhưng hoàn toàn trưởng thành rồi đấy.<br>Thịt ở phần cổ ngon lắm đó♪",
"本当に味に詳しいな、ディアーナ……": "Em thật sự rành mùi vị quá nhỉ‚ Diana……",
"それじゃあ、あの子は油断してるみたいだし……狩るよ。": "Vậy thì con đó có vẻ đang mất cảnh giác…… tôi săn đây.",
"ディアーナは滑らかに弓を構え、ピタリと狙いを定める。<br>音を抑えて獲物に気づかせないためか、雷はまとっていない。": "Diana nâng cung lên thật mượt mà và nhắm chuẩn xác.<br>Có lẽ để giảm âm thanh và không để con mồi phát hiện‚ mũi tên không hề mang sét.",
"いくよ――っ！": "Tôi bắn đây――!",
"まったく揺れることなく指先を離すディアーナ。<br>ゆるやかな弧を描いて飛んだ矢は、水を飲む狐を見事に貫いた。": "Diana buông ngón tay mà không hề dao động.<br>Mũi tên bay theo một đường cong mềm mại và xuyên trúng con cáo đang uống nước.",
"２匹目～！　やったねっ！": "Con thứ hai～! Tuyệt quá!",
"お見事。<br>しかし想定した獲物よりずっと小物だなー。": "Đẹp mắt lắm.<br>Nhưng nó nhỏ hơn con mồi anh dự tính nhiều quá nhỉ.",
"いーのいーの。<br>司令官くんの見つけた獲物を狩った、っていうのが大事だから。": "Không sao không sao.<br>Quan trọng là tôi đã săn được con mồi do Chỉ Huy tìm thấy mà.",
"キミのお手柄だよ。<br>やったね、司令官くん！": "Đó là công của cậu đấy.<br>Làm tốt lắm‚ Chỉ Huy!",
"……くそう、ディアーナはこんなにいい奴なのに、<br>俺が足を引っ張ってるのが悔しい……！": "……Chết tiệt‚ Diana tốt bụng đến thế này‚<br>vậy mà anh lại đang kéo chân em làm anh thấy tức quá……!",
"引っ張ってないってば！<br>すっごく楽しいよ♪": "Đã bảo là cậu không kéo chân tôi mà!<br>Tôi đang vui lắm đấy♪",
"しかし……ほら、みろよ。<br>あっちにもハンターがいるだろ。": "Nhưng mà…… này‚ nhìn đi.<br>Đằng kia cũng có thợ săn phải không.",
"巨大なアッシュボアを抱えたハンターチームが拳を突き上げている。<br>ビーストヴァルチャーやフレアフォックスとは格の違う大物だ。": "Một đội thợ săn đang ôm con Ash Boar khổng lồ và giơ nắm đấm lên.<br>Đó là con mồi lớn khác hẳn Beast Vulture hay Flare Fox.",
"さすが兄貴っ！<br>このアッシュボアのデカさときたら……優勝間違いなしっすね！": "Đúng là đại ca!<br>Con Ash Boar này to cỡ đó…… chắc chắn vô địch rồi!",
"当然ってもんよ！<br>俺と同じチームで良かったな！": "Đương nhiên rồi!<br>Được cùng đội với tao là may cho mày đấy!",
"また違う方向へ視線を向けると男女コンビのハンターが<br>コケだらけの巨大な角を持つシカ、グラスディアを運んでいる。": "Khi nhìn sang hướng khác‚ một cặp thợ săn nam nữ<br>đang khiêng con hươu Grass Deer với cặp sừng khổng lồ phủ đầy rêu.",
"どうだい、ハニー！<br>ぼくの腕前もなかなかだろう？": "Thế nào hả‚ em yêu!<br>Tay nghề của anh cũng khá lắm đúng không?",
"さすがねダーリン！<br>料理はわたしに任せておいて！": "Đúng là anh yêu của em!<br>Cứ để chuyện nấu nướng cho em!",
"おぉ……すまないがハニー、きみに作らせたら最下位確定だよ……": "Ôi…… xin lỗi em yêu‚ nhưng để em nấu thì chắc chắn đội mình đội sổ mất……",
"どういう意味か詳しく聞きたいわ、ダーリン？": "Em muốn nghe anh giải thích thật kỹ câu đó đấy‚ anh yêu?",
"相棒が俺じゃなきゃ、ああいう獲物を狩れていただろうに……": "Nếu bạn đồng đội của em không phải là anh‚ chắc em cũng săn được con mồi như thế rồi……",
"すごいね、あの人たち。<br>あんな大物、しかも傷も少ない。いい腕だっ！": "Họ giỏi thật đấy.<br>Con mồi lớn thế mà vết thương lại ít. Tay nghề tốt quá!",
"褒めてる場合じゃないだろ！<br>どうして嬉しそうなんだ、ディアーナ！": "Giờ đâu phải lúc khen họ!<br>Sao em lại có vẻ vui thế hả‚ Diana!",
"みんながそれぞれの獲物を狙って狩りをしてる。<br>でも時にすれ違い、通じ合う……！": "Mọi người đang nhắm vào con mồi riêng rồi đi săn.<br>Nhưng đôi khi họ lướt qua nhau‚ rồi thấu hiểu nhau……!",
"本当に楽しいよ～！<br>いいコンテストだね～♪": "Vui thật đấy～!<br>Đúng là một cuộc thi hay～♪",
"……楽しそうではあるんだがなあ。<br>勝つ気はあるんだろうか、ディアーナ……": "……Đúng là em ấy trông vui thật.<br>Nhưng Diana có định thắng không vậy……",
"相棒が楽しそうならそれでいいんだが、と肩をすくめたその時。<br>水辺から少し離れた森の中から、大きな鳴き声が聞こえた。": "Nếu bạn đồng đội vui thì cũng được thôi‚ anh vừa nhún vai nghĩ vậy.<br>Đúng lúc đó‚ từ khu rừng hơi xa bờ nước vang lên một tiếng kêu lớn.",
"――モーケッコブヒー！！！": "――Bò Cục Tác Ụt Ịt!!!",
"お、おお？<br>なんだ、今の妙な鳴き声！？": "Ơ‚ ồ?<br>Tiếng kêu kỳ quặc vừa rồi là gì thế!?",
"これは……ウシトリブタの鳴き声！": "Đây là…… tiếng kêu của Bò Gà Heo!",
"ウ……ウシトリブタ！？": "B…… Bò Gà Heo!?",
"ウシ、トリ、そしてブタの美味しさを併せ持ち、それを超える！　<br>伝説の高級食材だよ！？": "Nó có cả vị ngon của bò‚ gà và heo‚ rồi còn vượt trên tất cả! <br>Đó là nguyên liệu cao cấp trong truyền thuyết đấy!?",
"マジか！？　狩れば逆転だって夢じゃないぞ！<br>逃すわけにはいかないな！": "Thật sao!? Nếu săn được nó thì lội ngược dòng cũng không phải mơ!<br>Không thể để nó thoát được!",
"うん、すごく美味しいからみんなに料理を食べてほしいね！": "Ừ‚ nó ngon lắm nên tôi muốn mọi người được ăn món nấu từ nó!",
"……目的がズレているが、まあ良し！<br>いくぞおおおおおっ！": "……Mục tiêu hơi lệch rồi‚ nhưng thôi được!<br>Đi thôiôôôôô!",
"お～♪": "Ô～♪",
}

TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%(?:user|s|d)|\{\d+\}|\$\{[^}]+\}|%%')

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def detect_newline(raw: bytes) -> str:
    if b'\r\n' in raw: return 'CRLF'
    if b'\n' in raw: return 'LF'
    if b'\r' in raw: return 'CR'
    return 'NONE'

def split_line(line: str):
    return line.split(',')

def get_text_field(parts):
    if not parts: return None
    cmd = parts[0]
    if cmd == 'title' and len(parts) >= 2:
        return 1
    if cmd in {'message','messageTextUnder','messageTextCenter'} and len(parts) >= 3:
        return 2
    return None

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = SRC.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in text else '\n'
    lines = text.splitlines(True)
    src_noends = [l[:-2] if l.endswith('\r\n') else l[:-1] if l.endswith('\n') else l for l in lines]
    out_noends = []
    records = []
    issues = []
    counts = {k:0 for k in TEXT_CMDS}
    changed = 0
    unchanged_text = []
    for idx, line in enumerate(src_noends, start=1):
        parts = split_line(line)
        cmd = parts[0] if parts else ''
        if cmd in TEXT_CMDS: counts[cmd] += 1
        tf = get_text_field(parts)
        if tf is not None:
            src_text = parts[tf]
            vi = TRANSLATIONS.get(src_text)
            status = 'TRANSLATED' if vi is not None else 'UNMATCHED'
            if vi is None:
                vi = src_text
                issues.append({'line': idx, 'severity':'BLOCKER', 'type':'UNMATCHED_TEXT', 'source': src_text})
            else:
                if ',' in vi:
                    issues.append({'line': idx, 'severity':'BLOCKER', 'type':'ASCII_COMMA_IN_TRANSLATION', 'translation': vi})
                if TAG_RE.findall(src_text) != TAG_RE.findall(vi):
                    issues.append({'line': idx, 'severity':'BLOCKER', 'type':'TAG_MISMATCH', 'source': src_text, 'translation': vi})
                if PH_RE.findall(src_text) != PH_RE.findall(vi):
                    issues.append({'line': idx, 'severity':'BLOCKER', 'type':'PLACEHOLDER_MISMATCH', 'source': src_text, 'translation': vi})
                if vi == src_text:
                    unchanged_text.append(idx)
                parts[tf] = vi
                changed += 1
            out_line = ','.join(parts)
            records.append({'line': idx, 'command': cmd, 'speaker': parts[1] if cmd.startswith('message') and len(parts)>1 else None, 'source_text': src_text, 'vi_text': vi, 'status': status, 'delimiter_count_source': line.count(','), 'delimiter_count_vi': out_line.count(',')})
            out_noends.append(out_line)
        else:
            out_noends.append(line)
    out_text = newline.join(out_noends)
    if text.endswith('\n'):
        out_text += newline
    out_raw = (b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8')
    OUT.write_bytes(out_raw)

    out_lines = out_text.splitlines()
    # structural QA
    if len(out_lines) != len(src_noends):
        issues.append({'severity':'BLOCKER','type':'LINE_COUNT_MISMATCH','source':len(src_noends),'vi':len(out_lines)})
    for i,(s,o) in enumerate(zip(src_noends,out_lines), start=1):
        if s.count(',') != o.count(','):
            issues.append({'line':i,'severity':'BLOCKER','type':'DELIMITER_COUNT_MISMATCH','source':s.count(','),'vi':o.count(',')})
        sp, op = s.split(','), o.split(',')
        tf = get_text_field(sp)
        if tf is not None:
            # technical fields except text field unchanged
            sp2, op2 = sp[:], op[:]
            if len(sp2)==len(op2):
                sp2[tf] = op2[tf] = '<TEXT>'
                if sp2 != op2:
                    issues.append({'line':i,'severity':'BLOCKER','type':'TECH_FIELD_CHANGED','source':sp2,'vi':op2})
    focused_diff = ''.join(difflib.unified_diff(src_noends, out_lines, fromfile=str(SRC), tofile=str(OUT), lineterm='\n'))
    (WORK/'focused_diff.md').write_text('```diff\n'+focused_diff+'\n```\n', encoding='utf-8')
    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        'scene': SCENE,
        'created_at': now,
        'paths': {'source_asset': str(SRC), 'output_asset': str(OUT), 'jp_json': str(JP_JSON), 'en_json': str(EN_JSON), 'work_dir': str(WORK)},
        'source_hash_sha256': sha256(raw),
        'output_hash_sha256': sha256(out_raw),
        'encoding': 'utf-8-sig' if bom else 'utf-8',
        'bom': bom,
        'newline': detect_newline(raw),
        'line_count_source': len(src_noends),
        'line_count_output': len(out_lines),
        'text_command_counts': counts,
        'candidate_text_records': sum(counts.values()),
        'translated_records': changed,
        'unmatched_records': len([r for r in records if r['status']=='UNMATCHED']),
        'status': 'PASS' if not issues else 'FAIL',
        'independent_verify': {'status': 'NOT_RUN'},
        'records': records,
    }
    qa = {
        'scene': SCENE,
        'created_at': now,
        'structural_qa': {
            'line_count_match': len(out_lines)==len(src_noends),
            'delimiter_counts_match': all(s.count(',')==o.count(',') for s,o in zip(src_noends,out_lines)),
            'technical_fields_preserved': not any(i.get('type')=='TECH_FIELD_CHANGED' for i in issues),
            'tag_placeholder_preserved': not any(i.get('type') in {'TAG_MISMATCH','PLACEHOLDER_MISMATCH'} for i in issues),
            'bom_preserved': bom == out_raw.startswith(b'\xef\xbb\xbf'),
            'newline_preserved': detect_newline(raw) == detect_newline(out_raw),
            'text_command_counts': counts,
        },
        'linguistic_qa': {
            'jp_primary_en_alignment_only': True,
            'commander_translation': '司令官/Commander -> Chỉ Huy trong text fields',
            'speaker_and_charaload_names_preserved': True,
            'ascii_comma_rule': 'No ASCII comma inside translated text fields; U+201A used where needed.',
            'h18': 'No H18/adult content in this scene.',
        },
        'issues': issues,
        'unchanged_text_lines': unchanged_text,
        'independent_verify': {'status': 'NOT_RUN'},
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': manifest['status'], 'translated': changed, 'candidates': manifest['candidate_text_records'], 'issues': len(issues), 'out': str(OUT)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
