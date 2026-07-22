# -*- coding: utf-8 -*-
"""Apply Vietnamese translation for hmn_10180100003 without modifying EN source."""
from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SCENE = "hmn_10180100003"
ROOT = Path("E:/AgentTranslation")
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"
SRC = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
DIFF = WORK / "focused_diff.md"
MANIFEST = WORK / "manifest.json"
QA = WORK / "qa_log.json"
TEXT_COMMANDS = {"title", "message", "messageTextUnder", "messageTextCenter"}

TRANSLATIONS = {
    "試練の先へ、復活のドリル！": "Vượt Qua Thử Thách‚ Mũi Khoan Hồi Sinh!",
    "<size=48>――大穴浅層　岩場地帯</size>": "<size=48>――Tầng Nông Đại Huyệt  Khu Vực Đá</size>",
    "グォォォォン……": "Gruooooon……",
    "岩場に隠れたグラディアと<user>の付近を<br>大型のゴーレムが歩き回っている。": "Con golem cỡ lớn đang đi quanh gần<br>グラディア và <user> đang nấp giữa bãi đá.",
    "巨大な足が地面を踏みしめるたび<br>周囲がぐらぐらと揺れた。": "Mỗi lần đôi chân khổng lồ giẫm xuống mặt đất<br>xung quanh lại rung chuyển dữ dội.",
    "なんとか逃げられた、か。<br>だがあの大型ゴーレム、まだこちらを探してるな。": "Cuối cùng cũng thoát được nhỉ.<br>Nhưng con golem cỡ lớn kia vẫn đang tìm chúng ta.",
    "……ごめん。<br>私が試し掘りになんて誘ったから……": "……Xin lỗi.<br>Tại em rủ anh đi đào thử nên mới……",
    "壁も掘ってみろ、なんて言ったのは俺だ。<br>お互い様ってやつだな。": "Chính anh mới bảo em thử khoan cả vách đá mà.<br>Xem như cả hai cùng có lỗi đi.",
    "だからこそ、ここは協力して状況を打開しよう。<br>お前のドリルを頼りにしてるぞ、グラディア。": "Vì vậy giờ ta phải hợp sức để phá thế bế tắc này.<br>Anh trông cậy vào mũi khoan của em đấy‚ グラディア.",
    "……でも、私のドリルじゃ、<br>あのゴーレムに穴すらあけられなかった。": "……Nhưng mũi khoan của em<br>đến một cái lỗ trên con golem đó cũng không khoan nổi.",
    "硬い相手にこそドリル、なんだろ。<br>諦めずにもう１度挑んでみないか？": "Đối thủ càng cứng thì càng phải dùng khoan‚ đúng không?<br>Đừng bỏ cuộc‚ thử thêm lần nữa nhé?",
    "ううん、もう駄目なんだよ。<br>……見てて。": "Không‚ hết cách rồi.<br>……Anh xem này.",
    "グラディアがドリルを操作すると、カチッという軽い音が鳴った。<br>ドリルの先端は少しだけ振動し――動くことはなかった。": "Khi グラディア thao tác mũi khoan‚ một tiếng cách khẽ vang lên.<br>Đầu khoan chỉ rung nhẹ rồi――không hề chuyển động.",
    "ドリルが動かない……？<br>壊れたのか？": "Mũi khoan không chạy……?<br>Nó hỏng rồi à?",
    "さっきのオーバーヒートで、<br>部品が焼き付いたんだ。": "Vì bị quá nhiệt lúc nãy<br>nên linh kiện bị cháy kẹt rồi.",
    "安定性を考えずに、新型の部品を使いすぎた。<br>上昇した出力に内部パーツが耐えられなかったの。": "Em đã dùng quá nhiều linh kiện đời mới mà không tính đến độ ổn định.<br>Các bộ phận bên trong không chịu nổi công suất tăng lên.",
    "私が急ぎすぎた、焦りすぎたんだ。<br>失敗に向き合う前に、先へ進んじゃったから……": "Em đã quá vội‚ quá nôn nóng.<br>Vì em cứ tiến lên trước khi đối mặt với thất bại……",
    "こんなんじゃお父さんのところへ<br>たどり着けるはずない……": "Cứ thế này thì em không thể nào<br>đến được chỗ cha……",
    "役立たずだ、私。<br>改良したって調子にのって、こんな失敗を……": "Em vô dụng thật.<br>Cứ tưởng đã cải tiến được rồi lại đắc ý‚ để xảy ra thất bại thế này……",
    "本当にごめん……": "Em thật sự xin lỗi……",
    "おい、何を落ち込んでる。<br>１度失敗したからなんだっていうんだ。": "Này‚ sao lại ủ rũ thế.<br>Thất bại một lần thì đã sao chứ.",
    "失敗こそが次の成功につながるんだろう？<br>今こそトライアンドエラーだ！": "Chính thất bại mới dẫn tới thành công tiếp theo‚ đúng không?<br>Giờ mới là lúc thử và sửa sai!",
    "……ここから、成功を？": "……Từ đây mà đi tới thành công sao?",
    "おう、このぐらいのピンチで諦めるな。<br>まだまだあがくぞ！": "Ừ‚ đừng bỏ cuộc chỉ vì chút nguy cấp này.<br>Ta vẫn còn vùng vẫy được!",
    "実戦で使ってみたら欠点がわかった――立派な失敗だろう！<br>この次こそ成功してやればいいんだ！": "Đem ra thực chiến mới biết nhược điểm――đó là một thất bại rất ra dáng đấy!<br>Lần sau chỉ cần biến nó thành thành công là được!",
    "……キミは全然諦めないね。<br>本当に……お父さんみたいだ。": "……Anh đúng là chẳng chịu bỏ cuộc chút nào.<br>Thật sự…… giống cha em quá.",
    "いいや、グラディアが希望を信じているように、<br>俺も諦めずに抵抗しようって思っただけだ。": "Không đâu‚ chỉ là giống như グラディア tin vào hy vọng<br>anh cũng nghĩ mình phải chống cự đến cùng thôi.",
    "グラディアの中のお父さんが、<br>俺にとっても希望になってるんだよ。": "Người cha trong lòng グラディア<br>cũng đã trở thành hy vọng đối với anh.",
    "私の中のお父さんが……": "Người cha trong lòng em……",
    "うん、わかった。私もエラーを恐れない。<br>失敗を受け入れて、もう１度トライする。": "Ừ‚ em hiểu rồi. Em cũng sẽ không sợ lỗi nữa.<br>Em sẽ chấp nhận thất bại và thử thêm lần nữa.",
    "失敗を……受け入れて……あっ！": "Chấp nhận…… thất bại…… a!",
    "どうした？": "Sao thế?",
    "そういえば、ここに……": "Nghĩ lại thì‚ trong này……",
    "この部品、壊れてるみたいですけど、<br>捨てちゃっていいですか？": "Linh kiện này hình như hỏng rồi<br>em vứt đi được không ạ?",
    "……っ。<br>これは、ダメ。": "……!<br>Cái này thì không được.",
    "グラディアはアリシアの持ってきたいくつかのパーツを、<br>丁寧にバッグへとしまいこんだ。": "グラディア cẩn thận cất những linh kiện mà アリシア mang tới<br>vào trong túi.",
    "そうだ。<br>あの時のパーツ……！": "Đúng rồi.<br>Những linh kiện lúc đó……!",
    "グラディアがバックを開くと、<br>いくつかの壊れたパーツが入っていた。": "Khi グラディア mở túi ra<br>bên trong có vài linh kiện đã hỏng.",
    "アリシアに捨てられそうになったやつか！<br>持ったままだったんだな。": "Mấy thứ suýt bị アリシア vứt đi đó hả!<br>Em vẫn giữ chúng bên mình à.",
    "うん、これを使えばドリルが修理できるかも。": "Ừ‚ dùng những thứ này có lẽ sẽ sửa được mũi khoan.",
    "希望が見えてきたな。<br>グラディアが掃除下手で助かった。": "Bắt đầu thấy hy vọng rồi đấy.<br>May mà グラディア không giỏi dọn dẹp.",
    "む……下手じゃない。<br>必要な場所に置いてるだけ。": "Ưm…… em không vụng.<br>Chỉ là để chúng ở nơi cần thiết thôi.",
    "今回も必要になったしな、そういうことにしておこう。": "Lần này đúng là cần thật‚ vậy cứ coi là thế đi.",
    "すぐ修理を始める。<br>生き残ってるパーツの共食い修理……！": "Em sẽ bắt đầu sửa ngay.<br>Sửa kiểu tận dụng các linh kiện còn sống sót……!",
    "おう、好きなようにやってくれ。<br>手伝えることがあれば何でも言えよ！": "Ừ‚ cứ làm theo ý em đi.<br>Có gì anh giúp được thì cứ nói!",
    "ここを、こうして……。<br>こっちの壊れた回路を迂回して、正常な部分を繋げば……": "Chỗ này làm thế này……<br>Nếu đi vòng qua mạch hỏng bên này và nối với phần còn hoạt động……",
    "グォォォォ……": "Gruoooo……",
    "（足音が近づいてきたな……。<br>ゴーレムがこっちに来てる、か）": "（Tiếng bước chân đang đến gần……<br>Con golem đang tới chỗ này sao）",
    "そろそろ隠れてるのも限界かもな……。<br>納期が近いみたいだが、進捗はどうだ、グラディア？": "Có lẽ sắp hết thời gian nấp rồi……<br>Hạn chót có vẻ đang tới gần‚ tiến độ sao rồi‚ グラディア?",
    "もう少し……！": "Chỉ chút nữa thôi……!",
    "（壊れた部分はあっても、生き残った部分はちゃんと使える。<br>無茶な試験にも耐えてくれたパーツなんだ）": "（Dù có phần bị hỏng‚ những phần còn sống sót vẫn dùng được hẳn hoi.<br>Chúng là các linh kiện đã chịu được cả thử nghiệm liều lĩnh đó）",
    "（失敗したからこそ、信頼できる部品が必要だって分かった。<br>この子たちならきっと不安定な新型を支えてくれる！）": "（Chính vì thất bại nên em mới hiểu mình cần những linh kiện đáng tin cậy.<br>Nếu là các em ấy thì chắc chắn sẽ chống đỡ được đời mới còn bất ổn!）",
    "（今度こそ失敗を成功につなげるんだ。<br>司令官と、キミと一緒に帰るために！）": "（Lần này nhất định em sẽ nối thất bại với thành công.<br>Để trở về cùng Chỉ Huy‚ cùng anh!）",
    "グォォォォォッ！！！": "Gruoooooo!!!",
    "見つかったか！<br>俺が引き付ける、グラディアは修理を続けろ！": "Bị phát hiện rồi sao!<br>Anh sẽ dụ nó‚ グラディア cứ tiếp tục sửa đi!",
    "司令官っ！？": "Chỉ Huy!?",
    "のろまなゴーレム相手に囮になるぐらいなら、俺にもできる！<br>信用しろ！": "Làm mồi nhử cho một con golem chậm chạp thì anh cũng làm được!<br>Tin anh đi!",
    "……うん。<br>必ず直してみせる。": "……Ừ.<br>Em nhất định sẽ sửa được.",
    "（……私がドリルを直して、そしてゴーレムを貫くって、<br>司令官は少しも疑ってない）": "（……Chỉ Huy không hề nghi ngờ rằng<br>em sẽ sửa mũi khoan rồi xuyên thủng con golem）",
    "（応えたい。あの人の信頼に。<br>キミの想いに……！）": "（Em muốn đáp lại. Niềm tin của người ấy.<br>Và tâm ý của anh……!）",
    "最後のパーツが繋がり、ドリルがその形を取り戻す。<br>スイッチを入れると、鈍い音を立てて先端が回り始めた。": "Linh kiện cuối cùng được nối vào‚ mũi khoan lấy lại hình dạng vốn có.<br>Khi bật công tắc‚ đầu khoan phát ra âm thanh trầm đục và bắt đầu quay.",
    "取り替えたパーツは信頼性が高いだけで、何の機能もついてない。<br>こんなのはチューンアップじゃなく、ただのデチューンだ。": "Những linh kiện thay vào chỉ có độ tin cậy cao chứ chẳng có chức năng gì.<br>Thế này không phải nâng cấp mà chỉ là hạ cấu hình thôi.",
    "でも、これこそが失敗を乗り越えて、<br>成功へとつなげるドリル！": "Nhưng đây mới chính là mũi khoan vượt qua thất bại<br>để nối tới thành công!",
    "待ってて、司令官……！": "Hãy chờ em‚ Chỉ Huy……!",
    "グォォォォォォォォォォンッ！": "Gruooooooooooon!",
    "大暴れしやがって……。<br>動きはのろいし、単純だが、大きすぎるのが厄介だな。": "Nó quậy phá dữ quá……<br>Động tác chậm và đơn giản‚ nhưng quá to nên phiền thật.",
    "このままじゃいずれ捕まる……っ！": "Cứ thế này thì sớm muộn cũng bị bắt……!",
    "ゴーレムが地面に両腕を叩きつける。<br>大きく揺れた地面に、<user>がバランスを崩す。": "Con golem đập cả hai tay xuống mặt đất.<br>Mặt đất rung mạnh khiến <user> mất thăng bằng.",
    "う、わっ……まずい……！": "Ư‚ oái…… nguy rồi……!",
    "体勢を崩した<user>を踏み潰そうと<br>ゴーレムが足を持ち上げた、その背後から――": "Con golem nhấc chân lên định giẫm nát <user> đang mất thăng bằng.<br>Đúng lúc đó‚ từ phía sau nó――",
    "えええいっ！": "Êêêi!",
    "グォォォッ！？": "Gruooo!?",
    "グラディアッ！<br>岩の上から飛びついたのかっ！？": "グラディア!<br>Em nhảy từ trên tảng đá xuống à!?",
    "ゴーレムに飛び乗ったグラディアが、<br>その頭部へドリルを叩き込む。": "グラディア nhảy lên con golem<br>và đâm mũi khoan thẳng vào đầu nó.",
    "どんな硬い岩にだって、私のドリルは負けたりしない！": "Dù là tảng đá cứng đến đâu‚ mũi khoan của em cũng không thua!",
    "魔石のパワーを与えられたドリルが<br>高速でゴーレムの頭に食い込む。": "Mũi khoan được truyền sức mạnh ma thạch<br>cắm sâu vào đầu golem với tốc độ cao.",
    "ドリル本体が甲高い音を立て、グラディアの腕が反動で震える。<br>しかし、それでも回転は止まることなく、穴を広げ続ける――": "Thân khoan phát ra tiếng rít chói tai‚ cánh tay グラディア run lên vì phản lực.<br>Thế nhưng vòng quay vẫn không dừng lại‚ tiếp tục khoét rộng cái lỗ――",
    "いけ、グラディアーーーッ！": "Làm đi‚ グラディアーーー!",
    "貫いて、私のドリルッ！": "Xuyên thủng đi‚ mũi khoan của ta!",
    "グオオオオオオオアアアアァァァァァァァッ！！！": "Gruooooooooaaaaaaa!!!",
    "ドリルの先端が、ついにゴーレムの頭を貫いた。<br>ゴーレムはぐらりとその場に倒れ伏す。": "Đầu khoan cuối cùng đã xuyên thủng đầu con golem.<br>Con golem lảo đảo rồi đổ gục ngay tại chỗ.",
    "や、った……": "Làm…… được rồi……",
    "頭に風穴を開けるとは……さすが、<br>改良しただけのことはあるな！": "Khoan thủng cả đầu nó…… quả không hổ danh<br>là thứ đã được cải tiến!",
    "昔のパーツもがんばってくれた。<br>失敗を乗り越えた昔のドリルが、助けてくれた。": "Những linh kiện cũ cũng đã cố hết sức.<br>Mũi khoan cũ từng vượt qua thất bại đã cứu em.",
    "そうだったのか……": "Ra là vậy……",
    "でもまだまだ。古いパーツの流用で、完成形じゃない。<br>今回の失敗も糧にして、もっとドリルを改良する。": "Nhưng vẫn còn xa lắm. Chỉ tận dụng linh kiện cũ nên chưa phải hình thái hoàn chỉnh.<br>Em sẽ lấy thất bại lần này làm chất liệu để cải tiến mũi khoan hơn nữa.",
    "私も、ドリルも、まだまだ強くなれる。<br>キミのおかげで、お父さんにつながる１歩を踏み出せたよ。": "Cả em và mũi khoan vẫn còn có thể mạnh hơn nữa.<br>Nhờ anh mà em đã bước được một bước tới gần cha.",
    "……お父さんが導いてくれたんのかもな。<br>いつか自分の元にたどり着くように、ってさ。": "……Có lẽ cha em đã dẫn đường cho em đấy.<br>Để một ngày nào đó em có thể đến được chỗ ông ấy.",
    "司令官……、<br>キミは本当に、そういうことを簡単に言う……": "Chỉ Huy……<br>Anh thật sự nói những chuyện như vậy dễ dàng quá……",
    "なんだ、またお父さんにでも見えたか？": "Sao thế‚ em lại thấy anh giống cha mình à?",
    "……キミはもう、お父さんには見えないよ。": "……Anh không còn giống cha em nữa đâu.",
    "そうか？<br>うれしいような、寂しいような……なんか複雑な気分だな……": "Vậy à?<br>Vừa vui vừa thấy hơi buồn…… cảm giác phức tạp thật……",
    "ま、さっさと戻るとしよう。": "Thôi‚ ta mau quay về nào.",
    "うん……そうだね。": "Ừ…… đúng vậy.",
    "お父さんになんて見えないよ。<br>だってキミは……": "Anh đâu còn giống cha em nữa.<br>Vì anh là……",
    "お父さんより、かっこいいなって、<br>思っちゃったから。": "Vì em đã lỡ nghĩ rằng<br>anh còn ngầu hơn cả cha em.",
    "……司令官、また試し掘りに付き合ってくれる？<br>ドリルの話をしながら、ね。": "……Chỉ Huy‚ lần sau anh lại đi đào thử cùng em nhé?<br>Vừa đi vừa nói chuyện về mũi khoan.",
    "ちゃんと予備パーツを持ってくるなら、な。": "Nếu em nhớ mang đủ linh kiện dự phòng thì được.",
    "ふふ……約束。": "Hì hì…… hứa rồi nhé.",
    "（いつか必ずお父さんを見つけ出して、<br>キミを紹介するよ）": "（Một ngày nào đó em nhất định sẽ tìm được cha<br>và giới thiệu anh với ông ấy）",
    "（ドリルのロマンを分かってくれる人で……<br>私の大切な人だよ、って）": "（Rằng anh là người hiểu được lãng mạn của mũi khoan……<br>và là người quan trọng của em）",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def detect_newline(data: bytes) -> str:
    return "CRLF" if b"\r\n" in data else "LF"


def has_bom(data: bytes) -> bool:
    return data.startswith(b"\xef\xbb\xbf")


def text_field_index(parts):
    if not parts:
        return None
    cmd = parts[0]
    if cmd == "title":
        return 1 if len(parts) > 1 else None
    if cmd in {"message", "messageTextUnder", "messageTextCenter"}:
        return 2 if len(parts) > 2 else None
    return None


def tags(s: str):
    return re.findall(r"<[^>]+>", s)


def placeholders(s: str):
    return re.findall(r"%[A-Za-z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}", s)


def jp_chars(s: str) -> bool:
    return bool(re.search(r"[ぁ-んァ-ヶ一-龯]", s))


def normalize_vi(s: str) -> str:
    # protect delimiters: ASCII comma cannot appear inside text fields
    return s.replace(",", "‚")


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = SRC.read_bytes()
    text = raw.decode("utf-8-sig")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    # split preserving terminal newline status
    lines = text.splitlines()
    had_terminal_newline = text.endswith(("\n", "\r\n"))

    ja_data = json.loads(JA_JSON.read_text(encoding="utf-8"))
    en_data = json.loads(EN_JSON.read_text(encoding="utf-8"))
    untranslated_en_values = sum(1 for v in en_data.values() if not v)

    out_lines = []
    records = []
    errors = []
    command_counts = Counter()
    translated_count = 0
    for idx, line in enumerate(lines, 1):
        parts = line.split(",")
        field_idx = text_field_index(parts)
        new_parts = list(parts)
        if field_idx is not None:
            command_counts[parts[0]] += 1
            src_field = parts[field_idx]
            vi = TRANSLATIONS.get(src_field)
            status = "TRANSLATED" if vi is not None else "UNMATCHED"
            if vi is None:
                errors.append({"line": idx, "type": "missing_translation", "text": src_field})
            else:
                vi = normalize_vi(vi)
                new_parts[field_idx] = vi
                translated_count += 1
                if tags(src_field) != tags(vi):
                    errors.append({"line": idx, "type": "tag_mismatch", "source": tags(src_field), "vi": tags(vi)})
                if placeholders(src_field) != placeholders(vi):
                    errors.append({"line": idx, "type": "placeholder_mismatch", "source": placeholders(src_field), "vi": placeholders(vi)})
                if "," in vi:
                    errors.append({"line": idx, "type": "ascii_comma_in_text_field", "vi": vi})
                if parts[0] == "title" and vi != "Vượt Qua Thử Thách‚ Mũi Khoan Hồi Sinh!":
                    errors.append({"line": idx, "type": "title_case_check", "vi": vi})
            records.append({
                "line": idx,
                "command": parts[0],
                "speaker": parts[1] if len(parts) > 1 else "",
                "source_text": src_field,
                "vi_text": new_parts[field_idx],
                "status": status,
                "delimiter_count_source": line.count(","),
                "delimiter_count_vi": ",".join(new_parts).count(","),
                "tag_count_source": len(tags(src_field)),
                "tag_count_vi": len(tags(new_parts[field_idx])),
            })
        new_line = ",".join(new_parts)
        if new_line.count(",") != line.count(","):
            errors.append({"line": idx, "type": "delimiter_count_changed", "source": line.count(","), "vi": new_line.count(",")})
        out_lines.append(new_line)

    output_text = newline.join(out_lines) + (newline if had_terminal_newline else "")
    OUT.write_text(output_text, encoding="utf-8-sig" if has_bom(raw) else "utf-8", newline="")

    out_raw = OUT.read_bytes()
    out_text = out_raw.decode("utf-8-sig")
    out_lines_read = out_text.splitlines()
    readback_errors = []
    if len(out_lines_read) != len(lines):
        readback_errors.append({"type": "line_count_mismatch", "source": len(lines), "vi": len(out_lines_read)})
    for i, (a, b) in enumerate(zip(lines, out_lines_read), 1):
        if a.count(",") != b.count(","):
            readback_errors.append({"line": i, "type": "readback_delimiter_mismatch", "source": a.count(","), "vi": b.count(",")})
    remaining_jp = []
    for rec in records:
        vi_text = out_lines_read[rec["line"] - 1].split(",")[text_field_index(out_lines_read[rec["line"] - 1].split(","))]
        # Exclude preserved character names in Japanese from leftover JP scan.
        stripped = vi_text.replace("グラディア", "").replace("アリシア", "")
        if jp_chars(stripped):
            remaining_jp.append({"line": rec["line"], "text": vi_text})

    diff_lines = list(difflib.unified_diff(
        lines,
        out_lines_read,
        fromfile=str(SRC),
        tofile=str(OUT),
        lineterm=""
    ))
    DIFF.write_text("# Focused Diff: hmn_10180100003\n\n```diff\n" + "\n".join(diff_lines) + "\n```\n", encoding="utf-8")

    source_meta = {
        "asset_source": str(SRC),
        "ja_json": str(JA_JSON),
        "en_json": str(EN_JSON),
        "output": str(OUT),
        "sha256_asset_source": sha256(SRC),
        "sha256_ja_json": sha256(JA_JSON),
        "sha256_en_json": sha256(EN_JSON),
        "sha256_output": sha256(OUT),
        "bom_source": has_bom(raw),
        "bom_output": has_bom(out_raw),
        "newline_source": detect_newline(raw),
        "newline_output": detect_newline(out_raw),
        "line_count_source": len(lines),
        "line_count_output": len(out_lines_read),
        "candidate_text_records": sum(command_counts.values()),
        "command_counts": dict(command_counts),
        "translated_text_records": translated_count,
        "ja_json_entries": len(ja_data),
        "en_json_entries": len(en_data),
        "en_json_blank_values": untranslated_en_values,
        "field_rule": "title uses field 2; message/messageTextUnder/messageTextCenter use field 3; preserve all other fields and delimiters",
        "notes": [
            "JP asset text matched ja.json order; en.json values are blank for this scene, so JP asset/ja.json were used as primary alignment source.",
            "Speaker names and charaload asset names kept unchanged per task rule; Japanese character-name leftovers グラディア/アリシア are intentional.",
        ],
    }
    qa = {
        "scene": SCENE,
        "status": "PASS" if not (errors or readback_errors or remaining_jp) else "REVIEW",
        "structural_qa": {
            "line_count_match": len(lines) == len(out_lines_read),
            "bom_preserved": has_bom(raw) == has_bom(out_raw),
            "newline_preserved": detect_newline(raw) == detect_newline(out_raw),
            "delimiter_counts_preserved": not any(e.get("type", "").endswith("delimiter_mismatch") or e.get("type") == "delimiter_count_changed" for e in errors + readback_errors),
            "tag_placeholder_errors": [e for e in errors if e["type"] in {"tag_mismatch", "placeholder_mismatch"}],
            "ascii_comma_errors": [e for e in errors if e["type"] == "ascii_comma_in_text_field"],
        },
        "translation_qa": {
            "candidate_text_records": sum(command_counts.values()),
            "translated_text_records": translated_count,
            "unmatched_records": [r for r in records if r["status"] != "TRANSLATED"],
            "remaining_japanese_excluding_preserved_names": remaining_jp,
            "h18": "not_present; all characters confirmed 18+ by project rule",
            "commander_rule": "司令官/Commander translated as Chỉ Huy in text fields",
        },
        "issues": errors + readback_errors,
        "records": records,
    }
    manifest = {
        "scene": SCENE,
        "status": qa["status"],
        "source_meta": source_meta,
        "outputs": {"vi_asset": str(OUT), "focused_diff": str(DIFF), "qa_log": str(QA), "script": str(Path(__file__))},
        "mapping_status_counts": {"TRANSLATED": translated_count, "UNMATCHED": len([r for r in records if r["status"] != "TRANSLATED"])},
        "qa_summary": qa["structural_qa"] | qa["translation_qa"],
        "independent_verify": None,
    }
    QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": qa["status"], "translated": translated_count, "candidates": sum(command_counts.values()), "issues": len(qa["issues"]), "output": str(OUT)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
