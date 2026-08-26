from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"D:\Study\intro2ai")
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path(r"C:\Users\pqt01\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\matplotlib\mpl-data\fonts\ttf")
FONT_REGULAR = str(FONT_DIR / "DejaVuSans.ttf")
FONT_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
FONT_ITALIC = str(FONT_DIR / "DejaVuSans-Oblique.ttf")
FONT_BOLD_ITALIC = str(FONT_DIR / "DejaVuSans-BoldOblique.ttf")

pdfmetrics.registerFont(TTFont("ArialVN", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("ArialVN-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("ArialVN-Italic", FONT_ITALIC))
pdfmetrics.registerFont(TTFont("ArialVN-BoldItalic", FONT_BOLD_ITALIC))
pdfmetrics.registerFontFamily(
    "ArialVN",
    normal="ArialVN",
    bold="ArialVN-Bold",
    italic="ArialVN-Italic",
    boldItalic="ArialVN-BoldItalic",
)

INK = colors.HexColor("#111111")
MID = colors.HexColor("#555555")
LIGHT = colors.HexColor("#E8E8E8")
PALE = colors.HexColor("#F6F6F6")
WHITE = colors.white


def P(text, style):
    return Paragraph(text, style)


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleVN", parent=base["Title"], fontName="ArialVN-Bold",
            fontSize=23, leading=27, alignment=TA_CENTER, textColor=INK,
            spaceAfter=5 * mm,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleVN", parent=base["Normal"], fontName="ArialVN",
            fontSize=11, leading=15, alignment=TA_CENTER, textColor=MID,
            spaceAfter=4 * mm,
        ),
        "h1": ParagraphStyle(
            "H1VN", parent=base["Heading1"], fontName="ArialVN-Bold",
            fontSize=15, leading=18, textColor=INK, spaceBefore=2 * mm,
            spaceAfter=2.5 * mm, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2VN", parent=base["Heading2"], fontName="ArialVN-Bold",
            fontSize=11.2, leading=14, textColor=INK, spaceBefore=2.5 * mm,
            spaceAfter=1.2 * mm, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "BodyVN", parent=base["BodyText"], fontName="ArialVN",
            fontSize=9.2, leading=12.4, textColor=INK, spaceAfter=1.5 * mm,
        ),
        "small": ParagraphStyle(
            "SmallVN", parent=base["BodyText"], fontName="ArialVN",
            fontSize=8.1, leading=10.5, textColor=INK, spaceAfter=1 * mm,
        ),
        "tiny": ParagraphStyle(
            "TinyVN", parent=base["BodyText"], fontName="ArialVN",
            fontSize=7.0, leading=8.8, textColor=INK, spaceAfter=0.6 * mm,
        ),
        "bullet": ParagraphStyle(
            "BulletVN", parent=base["BodyText"], fontName="ArialVN",
            fontSize=9.0, leading=12.0, leftIndent=4 * mm, firstLineIndent=-3 * mm,
            bulletIndent=0, textColor=INK, spaceAfter=1.1 * mm,
        ),
        "smallbullet": ParagraphStyle(
            "SmallBulletVN", parent=base["BodyText"], fontName="ArialVN",
            fontSize=7.6, leading=9.7, leftIndent=3 * mm, firstLineIndent=-2.3 * mm,
            textColor=INK, spaceAfter=0.5 * mm,
        ),
        "formula": ParagraphStyle(
            "FormulaVN", parent=base["BodyText"], fontName="ArialVN-Bold",
            fontSize=9.2, leading=12.2, leftIndent=4 * mm, rightIndent=3 * mm,
            borderWidth=0.5, borderColor=colors.HexColor("#999999"),
            borderPadding=5, backColor=PALE, spaceBefore=1.2 * mm,
            spaceAfter=2 * mm,
        ),
        "callout": ParagraphStyle(
            "CalloutVN", parent=base["BodyText"], fontName="ArialVN",
            fontSize=8.8, leading=11.6, leftIndent=3 * mm, rightIndent=3 * mm,
            borderWidth=0.6, borderColor=INK, borderPadding=6,
            backColor=PALE, spaceBefore=1.2 * mm, spaceAfter=2 * mm,
        ),
        "cheat_h1": ParagraphStyle(
            "CheatH1", parent=base["Heading1"], fontName="ArialVN-Bold",
            fontSize=12.8, leading=14.5, textColor=INK,
            spaceBefore=0.8 * mm, spaceAfter=1.0 * mm, keepWithNext=True,
        ),
        "cheat_h2": ParagraphStyle(
            "CheatH2", parent=base["Heading2"], fontName="ArialVN-Bold",
            fontSize=9.2, leading=10.8, textColor=INK,
            spaceBefore=1.1 * mm, spaceAfter=0.4 * mm, keepWithNext=True,
        ),
        "cheat": ParagraphStyle(
            "CheatBody", parent=base["BodyText"], fontName="ArialVN",
            fontSize=8.25, leading=10.3, textColor=INK, spaceAfter=0.8 * mm,
        ),
        "cheat_formula": ParagraphStyle(
            "CheatFormula", parent=base["BodyText"], fontName="ArialVN-Bold",
            fontSize=8.25, leading=10.35, textColor=INK, leftIndent=1.6 * mm,
            borderWidth=0.35, borderColor=colors.HexColor("#9A9A9A"),
            borderPadding=2.5, backColor=PALE, spaceBefore=0.5 * mm,
            spaceAfter=0.8 * mm,
        ),
        "cheat_bullet": ParagraphStyle(
            "CheatBullet", parent=base["BodyText"], fontName="ArialVN",
            fontSize=8.05, leading=10.0, leftIndent=2.7 * mm,
            firstLineIndent=-2.1 * mm, textColor=INK, spaceAfter=0.35 * mm,
        ),
    }


S = make_styles()


def header_footer(canvas, doc, short_title):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(colors.HexColor("#777777"))
    canvas.setLineWidth(0.35)
    canvas.line(doc.leftMargin, h - 10 * mm, w - doc.rightMargin, h - 10 * mm)
    canvas.setFont("ArialVN", 7.2)
    canvas.setFillColor(MID)
    canvas.drawString(doc.leftMargin, h - 8.1 * mm, short_title)
    canvas.drawRightString(w - doc.rightMargin, 7.2 * mm, f"Trang {doc.page}")
    canvas.drawString(doc.leftMargin, 7.2 * mm, "CSC14003 - Nhập môn Trí tuệ nhân tạo")
    canvas.restoreState()


def outline_page(canvas, doc):
    header_footer(canvas, doc, "ĐỀ CƯƠNG ÔN FINAL - CSC14003")


def cheat_page(canvas, doc):
    header_footer(canvas, doc, "CHEATSHEET FINAL - CSC14003")


def bullet(text, small=False):
    return P("• " + text, S["smallbullet" if small else "bullet"])


def section_title(number, title, tag=None):
    tag_text = f"  |  {tag}" if tag else ""
    rule = HRFlowable(width="100%", thickness=1.2, color=INK, spaceAfter=2 * mm)
    rule.keepWithNext = True
    return [P(f"{number}. {title}{tag_text}", S["h1"]), rule]


def two_col_table(left, right, widths=(0.5, 0.5), gap=3 * mm):
    usable = A4[0] - 28 * mm
    t = Table([[left, right]], colWidths=[usable * widths[0] - gap / 2, usable * widths[1] - gap / 2], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), gap),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def standard_table(rows, widths, header=True, font_size=8.0):
    data = []
    for row_i, row in enumerate(rows):
        style = ParagraphStyle(
            f"Tbl{row_i}", parent=S["small"], fontName="ArialVN-Bold" if header and row_i == 0 else "ArialVN",
            fontSize=font_size, leading=font_size + 2.1, spaceAfter=0,
        )
        data.append([P(str(cell), style) for cell in row])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#777777")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), LIGHT))
    t.setStyle(TableStyle(cmds))
    return t


def build_outline():
    path = OUT / "DE-CUONG-ON-FINAL-CSC14003.pdf"
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm,
        topMargin=15 * mm, bottomMargin=13 * mm,
        title="Đề cương ôn final CSC14003", author="Codex",
        subject="Đề cương tổng hợp từ slide môn học và đề cuối kỳ 2021-2024",
    )
    story = []

    # Cover and exam map
    story += [Spacer(1, 16 * mm), P("ĐỀ CƯƠNG ÔN FINAL", S["title"]),
              P("CSC14003 - Nhập môn Trí tuệ nhân tạo", S["subtitle"]),
              P("Bám slide giảng viên + đối chiếu 3 bộ đề cuối kỳ 2021-2024", S["subtitle"]),
              Spacer(1, 5 * mm)]
    priority_rows = [
        ["Ưu tiên", "Chủ đề", "Tần suất trong 3 bộ đề", "Cách học chắc điểm"],
        ["1", "ID3 / Decision Tree", "3/3", "Thuộc công thức; tự tính trọn một cây"],
        ["1", "PL/FOL: CNF, unification, resolution", "3/3", "Luyện biến đổi và ghi từng clause"],
        ["2", "Minimax + Alpha-Beta", "Có ở các đề gần đây", "Duyệt đúng thứ tự, ghi α/β"],
        ["2", "Naive Bayes", "Có ở các đề gần đây", "Prior, likelihood, Laplace"],
        ["3", "CSP + AC-3", "1/3", "MRV/LCV, domain sau mỗi bước"],
        ["4", "Perceptron / MLP", "Chưa thấy trong 3 đề", "Nắm forward, delta, update"],
        ["5", "Search + PEAS + local search", "Nền tảng môn", "So sánh thuật toán và điều kiện tối ưu"],
    ]
    story += [standard_table(priority_rows, [14*mm, 49*mm, 44*mm, 72*mm], font_size=7.7), Spacer(1, 4 * mm)]
    story += [P("Cách dùng tài liệu", S["h2"]),
              bullet("Học theo thứ tự ưu tiên ở bảng trên. Mỗi chủ đề: đọc slide chỉ định, làm lại ví dụ, rồi giải đề cũ không nhìn lời giải."),
              bullet("Đề cương này để hiểu quy trình. File cheatsheet đi kèm để ôn công thức và bẫy ngay trước giờ thi."),
              P("Quy ước: phần 'Bẫy' là lỗi dễ mất điểm; phần 'Khi làm bài' là thứ tự trình bày nên ghi ra giấy.", S["callout"]),
              P("Nguồn nội bộ", S["h2"]),
              P("Lecture 1-11 trong thư mục slide; syllabus CSC14003; đề cuối kỳ 2021-2022, 2022-2023, 2023-2024 trong thư mục finalexam.", S["small"]),
              PageBreak()]

    # ID3
    story += section_title("1", "ID3 / Decision Tree", "ƯU TIÊN CAO NHẤT - xuất hiện 3/3 đề")
    story += [P("Đọc ở slide: Lecture 10 - Basic Machine Learning, trang 33-57; entropy/Information Gain trang 40-54; quiz trang 57.", S["callout"]),
              P("Công thức lõi", S["h2"]),
              P("Entropy(S) = -Σ<sub>c</sub> p(c) log<sub>2</sub> p(c)<br/>AverageEntropy(S,A) = Σ<sub>v</sub> |S<sub>v</sub>|/|S| · Entropy(S<sub>v</sub>)<br/>IG(S,A) = Entropy(S) - AverageEntropy(S,A)", S["formula"]),
              P("Gain Ratio (từng xuất hiện trong đề 2021-2022)", S["h2"]),
              P("SplitInfo(S,A) = -Σ<sub>v</sub> |S<sub>v</sub>|/|S| · log<sub>2</sub>(|S<sub>v</sub>|/|S|)<br/>GainRatio(S,A) = IG(S,A) / SplitInfo(S,A)", S["formula"])]
    left = [P("Quy trình dựng cây", S["h2"]),
            bullet("1) Tính entropy của tập hiện tại."),
            bullet("2) Với từng thuộc tính, chia tập theo từng giá trị; tính entropy của từng nhánh."),
            bullet("3) Lấy trung bình có trọng số để ra AverageEntropy; suy ra IG hoặc Gain Ratio."),
            bullet("4) Chọn thuộc tính có chỉ số lớn nhất làm node; lặp trên từng nhánh."),
            bullet("5) Mỗi đường root -> leaf cho một luật IF-THEN.")]
    right = [P("Điều kiện dừng", S["h2"]),
             bullet("Tất cả mẫu cùng nhãn: trả leaf có nhãn đó."),
             bullet("Hết thuộc tính: trả nhãn plurality/majority của tập hiện tại."),
             bullet("Subset rỗng: dùng plurality/majority của tập cha."),
             P("Bẫy", S["h2"]),
             bullet("Trọng số nhánh là |S_v|/|S|, không phải chia đều."),
             bullet("0 log(0) được quy ước bằng 0."),
             bullet("IG thiên vị thuộc tính có nhiều giá trị; Gain Ratio hiệu chỉnh thiên vị này.")]
    story += [two_col_table(left, right), Spacer(1, 2 * mm)]
    example_rows = [
        ["Bước", "Phải ghi trên bài thi"],
        ["Entropy gốc", "Đếm số mẫu từng class -> p(c) -> thay vào công thức"],
        ["Mỗi thuộc tính", "Liệt kê các subset S_v, entropy từng subset, trọng số |S_v|/|S|"],
        ["So sánh", "Lập bảng IG hoặc Gain Ratio của tất cả thuộc tính còn lại"],
        ["Cây và luật", "Vẽ node/edge rõ giá trị; mỗi root-to-leaf là một rule"],
        ["Mẫu mới", "Đi từ root theo giá trị thuộc tính; tới leaf để lấy class"],
    ]
    story += [P("Khung trình bày ăn điểm", S["h2"]), standard_table(example_rows, [32*mm, 147*mm], font_size=8.1),
              P("Tự kiểm: nếu node con thuần nhất thì entropy = 0. Nếu một thuộc tính tách hoàn hảo toàn bộ class thì AverageEntropy = 0 và IG = Entropy(S).", S["callout"]),
              Spacer(1, 3 * mm)]

    # Naive Bayes
    story += section_title("2", "Naive Bayes", "ƯU TIÊN CAO")
    story += [P("Đọc ở slide: Lecture 10, trang 62-75; Laplace trang 69-72; quiz trang 75.", S["callout"]),
              P("Bayes: P(C|X) = P(X|C)P(C)/P(X). Giả định naive: các đặc trưng độc lập có điều kiện khi biết class.", S["body"]),
              P("score(C) = P(C) · Π<sub>i</sub> P(x<sub>i</sub>|C)<br/>Chọn class có score lớn nhất. Khi chỉ so sánh class, không cần tính mẫu số P(X).", S["formula"]),
              P("Laplace correction cho đặc trưng rời rạc:<br/>P(x<sub>i</sub>=v|C) = (count(v,C)+1) / (count(C)+k), với k là số giá trị có thể của thuộc tính.", S["formula"])]
    left = [P("Quy trình", S["h2"]),
            bullet("1) Lập bảng đếm class và từng giá trị thuộc tính theo class."),
            bullet("2) Prior: P(C)=count(C)/N."),
            bullet("3) Likelihood: tính P(x_i|C) cho đúng class; dùng Laplace nếu đề yêu cầu hoặc có xác suất 0."),
            bullet("4) Nhân prior với toàn bộ likelihood; so sánh score."),
            bullet("5) Có thể dùng log-score để biến tích thành tổng khi số đặc trưng lớn.")]
    right = [P("Bẫy", S["h2"]),
             bullet("Không đảo P(x|C) thành P(C|x)."),
             bullet("Một conditional bằng 0 làm cả tích bằng 0; Laplace xử lý việc này."),
             bullet("Mẫu số Laplace dùng count(C)+k, không dùng N+k."),
             bullet("Không bỏ prior trừ khi đề nói prior các class bằng nhau."),
             bullet("Nếu đề cho số liệu đã làm trơn, không cộng 1 lần nữa.")]
    story += [two_col_table(left, right),
              P("Mẫu trình bày: score(C1)=P(C1)×P(x1|C1)×...; score(C2)=...; vì score(C1) > score(C2) nên dự đoán C1. Ghi đủ phân số trước khi làm tròn.", S["callout"]),
              P("ID3 hay Naive Bayes?", S["h2"]),
              standard_table([
                  ["Tiêu chí", "ID3", "Naive Bayes"],
                  ["Sản phẩm", "Cây và luật dễ giải thích", "Xác suất/score theo class"],
                  ["Tính toán lõi", "Entropy, IG/Gain Ratio", "Prior, likelihood, Laplace"],
                  ["Lỗi hay gặp", "Sai trọng số subset", "Sai chiều điều kiện, bỏ prior"],
              ], [36*mm, 71*mm, 72*mm], font_size=8.0), Spacer(1, 3 * mm)]

    # PL
    story += section_title("3", "Propositional Logic: CNF, Resolution, Chaining", "ƯU TIÊN CAO NHẤT")
    story += [P("Đọc ở slide: Lecture 7 - Logical Agents. Entailment trang 19-22 và 27-32; CNF/resolution trang 44-54; FC/BC quiz trang 83; DPLL trang 84.", S["callout"]),
              P("Khái niệm", S["h2"]),
              P("KB ⊨ α nghĩa là trong mọi model mà KB đúng thì α cũng đúng. Resolution thường chứng minh bằng phản chứng: kiểm tra KB ∧ ¬α có dẫn đến mâu thuẫn hay không.", S["body"]),
              P("Các tương đương phải thuộc", S["h2"]),
              P("P -> Q ≡ ¬P ∨ Q<br/>P <-> Q ≡ (¬P ∨ Q) ∧ (¬Q ∨ P)<br/>¬(P ∧ Q) ≡ ¬P ∨ ¬Q;  ¬(P ∨ Q) ≡ ¬P ∧ ¬Q<br/>P ∨ (Q ∧ R) ≡ (P ∨ Q) ∧ (P ∨ R)", S["formula"])]
    left = [P("Refutation resolution", S["h2"]),
            bullet("1) Lập KB ∧ ¬query."),
            bullet("2) Khử <-> và ->."),
            bullet("3) Đẩy ¬ vào trong; khử phủ định kép."),
            bullet("4) Phân phối ∨ qua ∧ để ra CNF."),
            bullet("5) Tách thành các clause."),
            bullet("6) Resolve hai clause có literal đối ngẫu."),
            bullet("7) Ra clause rỗng □ -> KB ⊨ query.")]
    right = [P("Resolution rule", S["h2"]),
             P("(A ∨ P), (B ∨ ¬P) => (A ∨ B)", S["formula"]),
             P("Bẫy", S["h2"]),
             bullet("Phải thêm ¬query, không thêm query."),
             bullet("Clause rỗng mới là chứng cứ mâu thuẫn."),
             bullet("Đánh số clause; ghi hai clause cha mỗi bước."),
             bullet("Không resolve hai literal cùng dấu."),
             bullet("CNF là AND của các clause; mỗi clause là OR của literal.")]
    story += [two_col_table(left, right), Spacer(1, 2 * mm),
              P("Forward chaining và backward chaining", S["h2"]),
              standard_table([
                  ["Phương pháp", "Bắt đầu", "Dừng", "Ghi nhớ"],
                  ["Forward chaining", "Facts trong KB", "Query xuất hiện hoặc fixed point", "Data-driven; rule Horn"],
                  ["Backward chaining", "Query", "Về facts hoặc thất bại", "Goal-driven; tránh lặp mục tiêu"],
              ], [35*mm, 46*mm, 56*mm, 42*mm], font_size=7.8),
              P("Nếu forward chaining dừng ở fixed point mà chưa có query, chỉ kết luận 'không suy ra được bằng thủ tục này'; đừng tự ý kết luận query sai nếu ngữ nghĩa bài không cho phép.", S["callout"]),
              Spacer(1, 3 * mm)]

    # FOL
    story += section_title("4", "First-Order Logic", "CNF + UNIFICATION + RESOLUTION")
    story += [P("Đọc ở slide: Lecture 8. Dịch FOL trang 40; UI/EI trang 42-45; GMP/unification trang 48-57; FC trang 69; BC trang 80-81; CNF/Skolem trang 83-86; resolution trang 87-92.", S["callout"]),
              P("Dịch ngôn ngữ", S["h2"]),
              standard_table([
                  ["Cụm từ", "Ký hiệu / mẫu"],
                  ["mọi A đều là B", "∀x (A(x) -> B(x))"],
                  ["có ít nhất một A là B", "∃x (A(x) ∧ B(x))"],
                  ["không có A nào là B", "∀x (A(x) -> ¬B(x)) hoặc ¬∃x(A(x)∧B(x))"],
                  ["chỉ A mới là B", "∀x (B(x) -> A(x)); chú ý chiều kéo theo"],
              ], [52*mm, 127*mm], font_size=8.1),
              P("Quy trình FOL -> CNF", S["h2"])]
    left = [bullet("1) Khử <->, rồi khử ->."),
            bullet("2) Đẩy ¬ vào trong qua lượng từ: ¬∀xP ≡ ∃x¬P; ¬∃xP ≡ ∀x¬P."),
            bullet("3) Standardize apart: đổi tên biến ở các mệnh đề khác nhau."),
            bullet("4) Skolemize ∃."),
            bullet("5) Bỏ ∀ ngầm định."),
            bullet("6) Phân phối ∨ qua ∧; tách clause.")]
    right = [P("Skolem", S["h2"]),
             bullet("∃x P(x) -> P(c): dùng Skolem constant mới."),
             bullet("∀y ∃x P(x,y) -> P(f(y),y): Skolem function nhận các biến ∀ đang bao ngoài."),
             bullet("Hai lượng ∃ độc lập không được dùng chung một Skolem constant."),
             P("Mất tương đương nhưng giữ equisatisfiability, đủ cho refutation.", S["small"])]
    story += [two_col_table(left, right),
              P("Unification", S["h2"]),
              P("Tìm substitution θ sao cho E₁θ = E₂θ. MGU là substitution tổng quát nhất. Constant khác nhau hoặc function khác tên/arity -> fail. Occurs check: x không thể unify với f(x).", S["formula"]),
              P("Ví dụ: Knows(John,x) và Knows(y,Mother(y)) có thể cần giải ràng buộc đồng thời; luôn áp dụng substitution mới lên toàn bộ substitution đang có, không giải từng vị trí độc lập.", S["body"]),
              P("FOL resolution", S["h2"]),
              bullet("Standardize variables apart giữa hai clause; tìm literal đối ngẫu có thể unify; ghi MGU θ; bỏ cặp literal và áp dụng θ lên resolvent."),
              bullet("Lặp đến □. Trên bài thi, ghi dạng: C1, C2, θ={...} => C3."),
              P("Bẫy lớn: thiếu standardize-apart, bỏ quên θ, dùng sai Skolem function, hoặc dịch sai 'only'.", S["callout"]),
              Spacer(1, 3 * mm)]

    # Adversarial search
    story += section_title("5", "Minimax và Alpha-Beta Pruning", "ƯU TIÊN CAO")
    story += [P("Đọc ở slide: Lecture 5 - Adversarial Search. Minimax trang 18-21; complexity trang 22; alpha-beta trang 26-32; cutoff/evaluation trang 33-38; stochastic games trang 39-45.", S["callout"]),
              P("Minimax", S["h2"]),
              P("MAX node lấy max giá trị child; MIN node lấy min. Time O(b<super>m</super>), space O(bm) khi duyệt sâu. Kết quả giả định đối thủ chơi tối ưu.", S["formula"])]
    left = [P("MAX-VALUE", S["h2"]),
            P("v = -∞<br/>for child:<br/>  v = max(v, MIN-VALUE(child))<br/>return v", S["formula"]),
            P("MAX lưu α: cận dưới tốt nhất MAX đã đảm bảo được.", S["small"])]
    right = [P("MIN-VALUE", S["h2"]),
             P("v = +∞<br/>for child:<br/>  v = min(v, MAX-VALUE(child))<br/>return v", S["formula"]),
             P("MIN lưu β: cận trên tốt nhất MIN đã đảm bảo được.", S["small"])]
    story += [two_col_table(left, right),
              P("Alpha-Beta - điều kiện cắt", S["h2"]),
              P("Tại MAX: sau khi cập nhật v, nếu v ≥ β thì prune; ngược lại α=max(α,v).<br/>Tại MIN: sau khi cập nhật v, nếu v ≤ α thì prune; ngược lại β=min(β,v).", S["formula"]),
              P("Trình tự làm bài", S["h2"]),
              bullet("Duyệt DFS đúng thứ tự child đề cho. Truyền (α,β) từ cha xuống. Sau mỗi child: cập nhật v, kiểm tra prune ngay, rồi mới sang child kế."),
              bullet("Ghi α,β cạnh node; khoanh giá trị node; gạch toàn bộ nhánh chưa duyệt khi cắt. Root chọn action có minimax value tốt nhất."),
              P("Bẫy", S["h2"]),
              bullet("Alpha-beta không đổi minimax value, chỉ giảm số node duyệt. Chỉ child chưa duyệt mới bị prune."),
              bullet("Best move ordering có thể đạt khoảng O(b^(m/2)); hiệu quả phụ thuộc thứ tự duyệt."),
              P("Cutoff minimax: dừng ở depth limit/cutoff test và dùng EVAL thay UTILITY. Hàm EVAL tốt phải tương quan với kết quả thực và giữ đúng thứ tự win > draw > loss.", S["callout"]),
              Spacer(1, 3 * mm)]

    # CSP
    story += section_title("6", "Constraint Satisfaction Problems", "CSP + BACKTRACKING + AC-3")
    story += [P("Đọc ở slide: Lecture 6. Mô hình trang 7-14; AC-3 trang 24-29; backtracking/MRV/LCV trang 30-38; FC vs AC trang 38-40; quiz trang 43-47; min-conflicts trang 48-53.", S["callout"]),
              P("Mô hình CSP = Variables X, Domains D, Constraints C. Trong constraint graph: node là biến; edge nối hai biến có constraint chung.", S["body"]),
              P("Backtracking", S["h2"]),
              P("Nếu assignment đầy đủ -> solution. Chọn biến chưa gán -> chọn giá trị -> nếu consistent thì gán và recurse -> thất bại thì undo/backtrack.", S["formula"])]
    rows = [
        ["Heuristic", "Chọn gì?", "Mục đích"],
        ["MRV", "Biến có domain còn ít giá trị nhất", "Fail sớm"],
        ["Degree", "Tie-break: biến ràng buộc nhiều biến chưa gán nhất", "Tác động lớn nhất"],
        ["LCV", "Giá trị loại ít lựa chọn của hàng xóm nhất", "Giữ đường sống cho bước sau"],
    ]
    story += [standard_table(rows, [29*mm, 86*mm, 64*mm], font_size=8.0), Spacer(1, 2 * mm)]
    left = [P("Forward Checking", S["h2"]),
            bullet("Sau khi gán X=v, xóa khỏi domain hàng xóm các giá trị conflict."),
            bullet("Nếu domain nào rỗng -> backtrack."),
            bullet("Chỉ lan từ biến vừa được gán; nhẹ hơn AC-3.")]
    right = [P("AC-3", S["h2"]),
             bullet("Queue ban đầu chứa các arc."),
             bullet("REVISE(X_i,X_j): xóa x∈D_i nếu không tồn tại y∈D_j thỏa constraint."),
             bullet("Nếu D_i rỗng -> failure. Nếu thay đổi, thêm lại (X_k,X_i), k≠j.")]
    story += [two_col_table(left, right),
              P("AC-3 pseudocode rút gọn", S["h2"]),
              P("queue <- all arcs<br/>while queue not empty: pop (Xi,Xj); if REVISE(Xi,Xj): if Di empty return failure; add (Xk,Xi) for neighbors Xk≠Xj<br/>return success", S["formula"]),
              P("Khi làm bài: sau mỗi assignment/revise, ghi domain mới. Đừng chỉ ghi 'consistent'. Với Sudoku: biến = ô trống; domain = các số hợp lệ; constraint AllDiff theo hàng, cột, box.", S["callout"]),
              Spacer(1, 3 * mm)]

    # Neural networks
    story += section_title("7", "Perceptron, MLP và Backpropagation", "DỰ PHÒNG THEO SLIDE")
    story += [P("Đọc ở slide: Lecture 11. Perceptron trang 14-22; MLP/backprop trang 24-29; gradient descent trang 34-37; momentum và biến thể trang 38-44; quiz trang 45-47.", S["callout"]),
              P("Perceptron", S["h2"]),
              P("net = Σ<sub>i</sub> w<sub>i</sub>x<sub>i</sub> - θ;  y = step(net)<br/>e = y<sub>d</sub> - y;  Δw<sub>i</sub> = ηx<sub>i</sub>e;  w<sub>i</sub> <- w<sub>i</sub> + Δw<sub>i</sub>", S["formula"]),
              bullet("Bias có thể viết bằng x₀=1 với weight w₀. Giữ đúng convention dấu bias/threshold mà đề cho."),
              bullet("Perceptron một lớp không biểu diễn được XOR; MLP có hidden layer thì được."),
              P("Sigmoid và forward pass", S["h2"]),
              P("σ(z)=1/(1+e<super>-z</super>);  σ'(z)=σ(z)(1-σ(z))<br/>net<sub>j</sub>=Σ<sub>i</sub>w<sub>ij</sub>x<sub>i</sub>;  y<sub>j</sub>=σ(net<sub>j</sub>)<br/>SSE: E=1/2 Σ<sub>k</sub>(y<sub>d,k</sub>-y<sub>k</sub>)²", S["formula"]),
              P("Backprop với sigmoid", S["h2"]),
              P("Output: δ<sub>k</sub>=y<sub>k</sub>(1-y<sub>k</sub>)(y<sub>d,k</sub>-y<sub>k</sub>)<br/>Hidden: δ<sub>j</sub>=y<sub>j</sub>(1-y<sub>j</sub>)Σ<sub>k</sub>w<sub>jk</sub>δ<sub>k</sub><br/>Δw<sub>ij</sub>=ηδ<sub>j</sub>x<sub>i</sub>;  w<sub>ij</sub><-w<sub>ij</sub>+Δw<sub>ij</sub>", S["formula"]),
              P("Thứ tự tính", S["h2"]),
              standard_table([
                  ["Bước", "Việc cần làm"],
                  ["1. Forward", "Tính net và output từng layer, giữ đủ số lẻ"],
                  ["2. Output delta", "Tính error rồi nhân đạo hàm activation"],
                  ["3. Hidden delta", "Dùng weight cũ và delta layer sau"],
                  ["4. Update", "Cập nhật mọi weight và bias sau khi đã có delta"],
              ], [34*mm, 145*mm], font_size=8.1),
              P("Bẫy: cập nhật weight quá sớm rồi dùng weight mới để tính hidden delta; quên bias; đảo dấu (target-output); sai chiều index weight.", S["callout"]),
              Spacer(1, 3 * mm)]

    # Search
    story += section_title("8", "Uninformed và Informed Search", "NỀN TẢNG")
    story += [P("Đọc ở slide: Lecture 3 Part 1 - formulation trang 12-14, search structures trang 34-41; Part 2 - BFS 8-21, UCS 24-41, DFS 43-48, DLS 50-52, IDS 54-57, bidirectional 59-60; Part 3 - Greedy 12-18, A* 20-36, heuristics/dominance 57-60.", S["callout"])]
    search_rows = [
        ["Thuật toán", "Frontier / ưu tiên", "Complete", "Optimal", "Bẫy chính"],
        ["BFS", "FIFO", "Có, b hữu hạn", "Có nếu cost đều", "Tốn bộ nhớ"],
        ["DFS", "LIFO", "Không với depth vô hạn", "Không", "Dễ đi sai nhánh sâu"],
        ["UCS", "min g(n)", "Có nếu cost ≥ ε", "Có", "Goal test khi pop"],
        ["Greedy", "min h(n)", "Tùy graph/implementation", "Không", "Không nhìn cost đã đi"],
        ["A*", "min f=g+h", "Có trong điều kiện chuẩn", "Có với h phù hợp", "Phải cập nhật path rẻ hơn"],
    ]
    story += [standard_table(search_rows, [28*mm, 35*mm, 36*mm, 28*mm, 52*mm], font_size=7.4), Spacer(1, 2 * mm),
              P("Heuristic", S["h2"]),
              P("Admissible: 0 ≤ h(n) ≤ h*(n), không overestimate chi phí thật đến goal.<br/>Consistent: h(n) ≤ c(n,n') + h(n') cho mọi cạnh. Consistent => admissible (với h(goal)=0). A* graph search optimal khi h consistent.", S["formula"]),
              P("Khi mô phỏng search", S["h2"]),
              bullet("Ghi rõ node gồm state, parent, action, g, depth. Tách thứ tự expanded khỏi returned path."),
              bullet("Mỗi vòng: lấy node đúng cấu trúc frontier; kiểm tra goal theo convention của thuật toán; expand; xử lý duplicate; cập nhật frontier."),
              bullet("UCS/A*: dừng khi goal được lấy khỏi priority queue, không dừng ngay lúc goal vừa được sinh."),
              bullet("Nếu tìm được đường rẻ hơn đến node đang ở frontier, cập nhật/reinsert node đó. Tie-break đúng như đề quy định."),
              P("Công thức nhớ nhanh: Greedy chỉ h; UCS chỉ g; A* dùng g+h.", S["callout"]),
              Spacer(1, 3 * mm)]

    # Supporting theory
    story += section_title("9", "PEAS, Agent Types và Local Search", "ĐỌC NHANH")
    story += [P("Đọc ở slide: Lecture 2 - PEAS trang 26-42, agent types trang 49-64. Lecture 4 - hill climbing 10-19, simulated annealing 21-22, local beam 24-25, genetic algorithm 27-38.", S["callout"]),
              P("PEAS", S["h2"]),
              P("P = Performance measure; E = Environment; A = Actuators; S = Sensors. Khi lập PEAS, mô tả đúng task environment cụ thể, không ghi tên thuật toán thay cho actuator/sensor.", S["formula"]),
              standard_table([
                  ["Agent", "Chọn hành động dựa trên", "Điểm phân biệt"],
                  ["Simple reflex", "Percept hiện tại + condition-action rules", "Không lưu trạng thái"],
                  ["Model-based reflex", "Internal state + model", "Xử lý partially observable"],
                  ["Goal-based", "Trạng thái mục tiêu", "Cần search/planning"],
                  ["Utility-based", "Expected utility", "So sánh trade-off/rủi ro"],
                  ["Learning agent", "Experience/feedback", "Performance, learning, critic, problem generator"],
              ], [41*mm, 75*mm, 63*mm], font_size=7.8), Spacer(1, 2 * mm),
              P("Local search", S["h2"]),
              standard_table([
                  ["Thuật toán", "Ý tưởng", "Bẫy / điểm nhớ"],
                  ["Hill climbing", "Chuyển sang neighbor tốt hơn", "Local maximum, ridge, plateau"],
                  ["Simulated annealing", "Đôi lúc nhận bước xấu theo xác suất", "Temperature giảm dần; thoát local optimum"],
                  ["Local beam", "Giữ k trạng thái tốt nhất", "Các beam có thể hội tụ giống nhau"],
                  ["Genetic algorithm", "Selection, crossover, mutation", "Representation và fitness quyết định chất lượng"],
              ], [36*mm, 76*mm, 67*mm], font_size=7.8),
              P("Các chủ đề này ít xuất hiện trong 3 bộ đề đã nhặt, nhưng là nguồn câu lý thuyết ngắn/trắc nghiệm. Ưu tiên sau khi làm chắc ID3, logic, minimax, NB và CSP.", S["callout"]),
              Spacer(1, 3 * mm)]

    # Final checklist
    story += section_title("10", "Checklist trước khi thi", "CHỐT ĐIỂM")
    checklist = [
        ["Chủ đề", "Tự kiểm trong 2 phút"],
        ["ID3", "Viết được H, AE, IG, GR; nhớ 3 điều kiện dừng; tự dựng 1 cây"],
        ["Naive Bayes", "Viết score; Laplace đúng mẫu số; giải thích vì sao bỏ P(X)"],
        ["PL", "Đổi ->, <->; đưa CNF; refutation bắt đầu bằng ¬query"],
        ["FOL", "Dịch lượng từ; standardize; Skolem; MGU; resolution có θ"],
        ["Alpha-Beta", "MAX: v≥β; MIN: v≤α; cập nhật sau từng child"],
        ["CSP", "MRV, Degree, LCV; FC vs AC-3; REVISE đúng chiều"],
        ["Neural net", "Forward -> output delta -> hidden delta -> update; giữ weight cũ"],
        ["Search", "BFS/DFS/UCS/Greedy/A*; goal test UCS/A* khi pop; h consistent"],
    ]
    story += [standard_table(checklist, [38*mm, 141*mm], font_size=8.1), Spacer(1, 4 * mm),
              P("Cách trình bày để lấy điểm", S["h2"]),
              bullet("Viết công thức trước rồi mới thay số; giữ phân số hoặc ít nhất 4 chữ số thập phân ở bước giữa."),
              bullet("Logic: đánh số clause; ghi clause cha và substitution. Alpha-beta: ghi α,β tại node. CSP: ghi domain sau từng revise."),
              bullet("Neural net: tách net -> activation -> error -> update. Search: ghi frontier/expanded order nếu đề yêu cầu."),
              bullet("Nếu kẹt, vẫn ghi quy trình đúng và các đại lượng trung gian; đây thường là phần điểm lớn."),
              P("Lộ trình chắc cú", S["h2"]),
              standard_table([
                  ["Vòng", "Mục tiêu"],
                  ["1", "ID3 + PL/FOL: làm lại toàn bộ câu đề cũ"],
                  ["2", "Minimax + Naive Bayes + CSP: giải không nhìn tài liệu"],
                  ["3", "Neural net + search + PEAS/local search: ôn công thức và câu lý thuyết"],
                  ["4", "Làm một đề đủ thời gian; chấm lỗi trình bày; dùng cheatsheet rà lần cuối"],
              ], [25*mm, 154*mm], font_size=8.2),
              Spacer(1, 4 * mm),
              P("Ưu tiên độ chính xác hơn tốc độ: mỗi lần làm sai, ghi lỗi vào cheatsheet cá nhân bằng một dòng ngắn.", S["callout"])]

    doc.build(story, onFirstPage=outline_page, onLaterPages=outline_page)
    return path


def ch(text, style="cheat"):
    return P(text, S[style])


def cb(text):
    return P("• " + text, S["cheat_bullet"])


def cheat_section(title, items):
    flows = [P(title, S["cheat_h1"]), HRFlowable(width="100%", thickness=0.75, color=INK, spaceAfter=0.8 * mm)]
    flows.extend(items)
    return flows


def build_cheatsheet():
    path = OUT / "CHEATSHEET-FINAL-CSC14003.pdf"
    left_margin = right_margin = 8 * mm
    top_margin = 13 * mm
    bottom_margin = 11 * mm
    gap = 5 * mm
    usable_w = A4[0] - left_margin - right_margin
    col_w = (usable_w - gap) / 2
    frame_h = A4[1] - top_margin - bottom_margin
    frames = [
        Frame(left_margin, bottom_margin, col_w, frame_h, leftPadding=1.2*mm, rightPadding=1.2*mm, topPadding=1.2*mm, bottomPadding=1.2*mm, id="left"),
        Frame(left_margin + col_w + gap, bottom_margin, col_w, frame_h, leftPadding=1.2*mm, rightPadding=1.2*mm, topPadding=1.2*mm, bottomPadding=1.2*mm, id="right"),
    ]
    doc = BaseDocTemplate(
        str(path), pagesize=A4, leftMargin=left_margin, rightMargin=right_margin,
        topMargin=top_margin, bottomMargin=bottom_margin,
        title="Cheatsheet final CSC14003", author="Codex",
        subject="Cheatsheet công thức và quy trình ôn final",
    )
    doc.addPageTemplates([PageTemplate(id="two-column", frames=frames, onPage=cheat_page)])
    st = []

    # Page 1, left - ID3
    st += cheat_section("1. ID3 / DECISION TREE", [
        ch("<b>H(S)=-Σ<sub>c</sub>p(c)log<sub>2</sub>p(c)</b><br/><b>AE(S,A)=Σ<sub>v</sub>|S<sub>v</sub>|/|S|·H(S<sub>v</sub>)</b><br/><b>IG(S,A)=H(S)-AE(S,A)</b>", "cheat_formula"),
        ch("<b>SplitInfo=-Σ<sub>v</sub>|S<sub>v</sub>|/|S|·log<sub>2</sub>(|S<sub>v</sub>|/|S|)</b><br/><b>GainRatio=IG/SplitInfo</b>", "cheat_formula"),
        ch("<b>Dựng cây</b>", "cheat_h2"),
        cb("H tập hiện tại -> AE/IG (hoặc GR) từng thuộc tính -> chọn lớn nhất -> chia subset -> lặp."),
        cb("Dừng: subset rỗng -> majority parent; cùng class -> leaf; hết attribute -> majority hiện tại."),
        cb("Mỗi root-to-leaf = một IF-THEN rule; phân loại mẫu bằng cách đi đúng nhánh."),
        ch("<b>Bẫy:</b> trọng số |S_v|/|S|; 0log0=0; IG bias thuộc tính nhiều giá trị; đừng làm tròn sớm.", "cheat"),
        ch("<b>Ghi bài:</b> bảng [attribute | entropy từng nhánh | AE | IG/GR], rồi vẽ cây.", "cheat"),
    ])
    st += cheat_section("2. NAIVE BAYES", [
        ch("<b>P(C|X)=P(X|C)P(C)/P(X)</b><br/><b>score(C)=P(C)Π<sub>i</sub>P(x<sub>i</sub>|C)</b> -> chọn score max.", "cheat_formula"),
        ch("<b>Laplace:</b> P(x_i=v|C)=(count(v,C)+1)/(count(C)+k), k=#giá trị có thể của thuộc tính.", "cheat_formula"),
        cb("Prior P(C)=count(C)/N -> conditional -> nhân score. So class thì bỏ P(X)."),
        cb("Bẫy: không đảo P(x|C); không bỏ prior; xác suất 0 -> Laplace; mẫu số là count(C)+k."),
    ])
    st += [Spacer(1, 1*mm), ch("<b>Ưu tiên đề cũ:</b> ID3 3/3; Logic 3/3; sau đó Minimax, NB, CSP.", "cheat_formula")]

    # Page 1, right - PL
    st += cheat_section("3. PROPOSITIONAL LOGIC", [
        ch("P->Q ≡ ¬P∨Q<br/>P<->Q ≡ (¬P∨Q)∧(¬Q∨P)<br/>¬(P∧Q) ≡ ¬P∨¬Q<br/>¬(P∨Q) ≡ ¬P∧¬Q<br/>P∨(Q∧R) ≡ (P∨Q)∧(P∨R)", "cheat_formula"),
        ch("<b>Chứng minh KB ⊨ α bằng resolution</b>", "cheat_h2"),
        cb("Lập KB ∧ ¬α -> khử <->, -> -> đẩy ¬ -> phân phối ∨ qua ∧ -> clauses."),
        cb("Resolve: (A∨P), (B∨¬P) => (A∨B). Ra □ thì entailment đúng."),
        cb("Ghi số clause và hai clause cha. Không resolve literal cùng dấu."),
        ch("<b>Forward chaining</b>", "cheat_h2"),
        cb("Facts -> rule có mọi premise đã biết -> thêm conclusion -> lặp đến query/fixed point."),
        ch("<b>Backward chaining</b>", "cheat_h2"),
        cb("Query -> tìm rule kết luận ra query -> biến premises thành subgoals -> facts; tránh vòng lặp."),
        ch("<b>Bẫy:</b> refutation thêm ¬query; □ là mâu thuẫn; CNF = AND của clauses, clause = OR của literals.", "cheat_formula"),
    ])
    st += cheat_section("4. FOL - DỊCH NHANH", [
        cb("mọi A là B: ∀x(A(x)->B(x))"),
        cb("có A là B: ∃x(A(x)∧B(x))"),
        cb("không A nào là B: ∀x(A(x)->¬B(x))"),
        cb("chỉ A mới B: ∀x(B(x)->A(x)) - coi chừng chiều."),
    ])

    # Page 2, left - FOL
    st += cheat_section("5. FOL - CNF / UNIFICATION", [
        ch("<b>FOL -> CNF</b>", "cheat_h2"),
        cb("Khử <->; khử ->; đẩy ¬ qua lượng từ; standardize apart; Skolemize ∃; bỏ ∀; phân phối ∨ qua ∧; tách clause."),
        ch("¬∀xP ≡ ∃x¬P;  ¬∃xP ≡ ∀x¬P", "cheat_formula"),
        ch("<b>Skolem:</b> ∃xP(x)->P(c).<br/>∀y∃xP(x,y)->P(f(y),y).<br/>Mỗi ∃ độc lập dùng symbol mới; function nhận các ∀ bao ngoài.", "cheat_formula"),
        ch("<b>Unification / MGU</b>", "cheat_h2"),
        cb("Tìm θ để E1θ=E2θ. Constant khác nhau -> fail. Function khác name/arity -> fail. Occurs check: x không unify f(x)."),
        cb("Áp dụng substitution mới vào toàn bộ biểu thức/substitution đang có."),
        ch("<b>GMP:</b> p1',...,pn', (p1∧...∧pn->q), với p_i'=p_iθ => qθ.", "cheat_formula"),
        ch("<b>FOL resolution</b>", "cheat_h2"),
        cb("Standardize apart -> chọn literal đối ngẫu -> unify bằng MGU θ -> bỏ cặp -> áp θ lên resolvent -> lặp đến □."),
        cb("Trình bày: C1, C2, θ={...} => C3."),
        ch("<b>Bẫy:</b> thiếu θ; dùng chung Skolem constant; quên biến ∀ trong Skolem function; resolve trước khi standardize.", "cheat_formula"),
    ])

    # Page 2, right - Minimax
    st += cheat_section("6. MINIMAX / ALPHA-BETA", [
        ch("MAX lấy max child; MIN lấy min child.<br/>Time O(b<super>m</super>), space O(bm).", "cheat_formula"),
        ch("<b>MAX</b>: v=-∞; v=max(v,child); nếu <b>v≥β</b> prune; α=max(α,v).<br/><b>MIN</b>: v=+∞; v=min(v,child); nếu <b>v≤α</b> prune; β=min(β,v).", "cheat_formula"),
        cb("Duyệt DFS đúng thứ tự đề. Truyền (α,β) xuống. Cập nhật v sau mỗi child, kiểm tra cắt ngay."),
        cb("Ghi α,β cạnh node; chỉ gạch các child chưa duyệt. Root chọn action có minimax value tốt nhất."),
        cb("Alpha-beta không đổi kết quả. Move ordering càng tốt càng cắt nhiều; best case ~O(b^(m/2))."),
        ch("<b>Cutoff:</b> đến depth limit thì dùng EVAL thay UTILITY; EVAL phải tương quan kết quả thật.", "cheat_formula"),
    ])
    st += cheat_section("7. CSP", [
        ch("CSP = variables X + domains D + constraints C.", "cheat_formula"),
        cb("Backtrack: complete? -> choose variable -> order values -> consistent? assign+recurse -> undo."),
        cb("MRV: domain nhỏ nhất. Degree: tie-break, nhiều neighbor chưa gán nhất. LCV: loại ít lựa chọn neighbor nhất."),
        ch("<b>Forward checking:</b> sau X=v, xóa giá trị conflict khỏi domain neighbors; domain rỗng -> backtrack.", "cheat"),
        ch("<b>AC-3:</b> queue all arcs. REVISE(Xi,Xj): xóa x∈Di nếu không có y∈Dj thỏa constraint. Di rỗng -> fail; nếu đổi thì thêm (Xk,Xi), k≠j.", "cheat_formula"),
        cb("Bẫy: REVISE có hướng; sau mỗi revise phải ghi domain mới; FC yếu hơn AC-3."),
    ])

    # Page 3, left - NN
    st += cheat_section("8. PERCEPTRON / BACKPROP", [
        ch("<b>Perceptron</b><br/>net=Σw_i x_i-θ; y=step(net)<br/>e=y_d-y; Δw_i=ηx_i e; w_i<-w_i+Δw_i", "cheat_formula"),
        cb("Bias có thể là x0=1. Một perceptron không giải XOR."),
        ch("<b>Sigmoid</b><br/>σ(z)=1/(1+e<super>-z</super>)<br/>σ'(z)=σ(z)(1-σ(z))", "cheat_formula"),
        ch("<b>Forward</b><br/>net_j=Σ_i w_ij x_i; y_j=σ(net_j)<br/>E=1/2 Σ_k(y_d,k-y_k)²", "cheat_formula"),
        ch("<b>Backprop</b><br/>δ_k=y_k(1-y_k)(y_d,k-y_k)<br/>δ_j=y_j(1-y_j)Σ_k w_jkδ_k<br/>Δw_ij=ηδ_jx_i; w_ij<-w_ij+Δw_ij", "cheat_formula"),
        cb("Thứ tự: forward -> output delta -> hidden delta bằng weight cũ -> update toàn bộ."),
        cb("Bẫy: quên bias; đảo dấu target-output; update sớm; sai chiều index weight; làm tròn sớm."),
    ])
    st += cheat_section("9. SEARCH - CÔNG THỨC", [
        ch("UCS: f=g. Greedy: f=h. A*: f=g+h.", "cheat_formula"),
        cb("Admissible: 0≤h(n)≤h*(n). Consistent: h(n)≤c(n,n')+h(n')."),
        cb("Consistent => admissible (h(goal)=0). A* graph search optimal nếu h consistent."),
    ])

    # Page 3, right - Search and basics
    st += cheat_section("10. SEARCH - SO SÁNH", [
        ch("<b>BFS:</b> FIFO; complete; optimal nếu step cost đều; space lớn.<br/><b>DFS:</b> LIFO; không optimal; có thể không complete.<br/><b>UCS:</b> min g; optimal với cost≥ε; goal test khi POP.<br/><b>Greedy:</b> min h; nhanh nhưng không đảm bảo optimal.<br/><b>A*:</b> min g+h; graph search optimal với h consistent.", "cheat_formula"),
        cb("UCS/A*: dừng khi goal được lấy khỏi priority queue, không phải lúc sinh."),
        cb("Có path rẻ hơn tới node: update/reinsert frontier. Tie-break theo đề."),
        cb("Ghi expanded order riêng returned path; ghi frontier nếu đề yêu cầu."),
    ])
    st += cheat_section("11. PEAS / AGENT", [
        ch("<b>PEAS</b> = Performance, Environment, Actuators, Sensors.", "cheat_formula"),
        cb("Simple reflex: current percept. Model-based: internal state. Goal-based: goal/search. Utility-based: expected utility. Learning: experience/feedback."),
    ])
    st += cheat_section("12. LOCAL SEARCH", [
        cb("Hill climbing: best neighbor; kẹt local max/ridge/plateau."),
        cb("Simulated annealing: đôi lúc nhận bước xấu; temperature giảm dần."),
        cb("Local beam: giữ k states. GA: selection -> crossover -> mutation; cần representation/fitness tốt."),
    ])
    st += cheat_section("TRÌNH BÀY ĂN ĐIỂM", [
        cb("Công thức trước, thay số sau; giữ ≥4 số lẻ trung gian."),
        cb("ID3: bảng H/AE/IG. Logic: clause cha + θ. Alpha-beta: α/β. CSP: domains. NN: net->y->δ->update."),
        cb("Nếu kẹt, vẫn ghi quy trình và đại lượng trung gian."),
        ch("<b>Slide:</b> L10 ID3/NB; L7 PL; L8 FOL; L5 game; L6 CSP; L11 NN; L3 search; L2 agents; L4 local search.", "cheat_formula"),
    ])
    st += [FrameBreak()]
    st += cheat_section("GHI CHÚ SAU KHI LÀM ĐỀ", [
        ch("Dùng cột này để ghi đúng lỗi mình vừa mắc; càng cụ thể càng dễ tránh lặp lại.", "cheat"),
        cb("□ Công thức/quy tắc mình quên"),
        cb("□ Bước tính hoặc phép biến đổi mình sai"),
        cb("□ Quy ước duyệt/tie-break của đề"),
        cb("□ Lỗi trình bày làm mất điểm"),
    ])
    for _ in range(14):
        st += [HRFlowable(width="100%", thickness=0.35, color=colors.HexColor("#AAAAAA"), spaceBefore=3.4*mm, spaceAfter=3.4*mm)]

    doc.build(st)
    return path


if __name__ == "__main__":
    outputs = [build_outline(), build_cheatsheet()]
    for p in outputs:
        print(p)
