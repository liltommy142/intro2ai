# Lời giải Final Exam 2023-2024

Nguồn đề: [trang 1](1.png), [trang 2](2.png), [trang 3](3.png), [trang 4](4.png).

## Câu 1. ID3 và Naïve Bayes

Dùng 10 mẫu đã có nhãn. Phân bố lớp là:

- `cinema`: 6;
- `tennis`: 2;
- `stay-in`: 1;
- `shopping`: 1.

Entropy ban đầu:

$$
H(S)=-0.6\log_2 0.6-0.2\log_2 0.2-2(0.1\log_2 0.1)=1.5710.
$$

### a. Xây dựng cây ID3 và bộ luật

Information Gain tại gốc:

| Thuộc tính | Information Gain |
|---|---:|
| Weather | 0.6955 |
| Parents | **0.6100** |
| Cash | 0.2813 |
| Exam | 0.3710 |

Lưu ý: bảng trên cho thấy `Weather` có IG lớn hơn `Parents`. Vì vậy theo đúng ID3 dùng Information Gain, **gốc phải là `Weather`**. Ta tiếp tục tính trên từng nhánh:

- `Weather = sunny`: các mẫu 1, 2, 10 gồm `cinema, tennis, tennis`. `Parents` phân chia hoàn hảo: `visit -> cinema`, `no-visit -> tennis`.
- `Weather = rainy`: các mẫu 4, 5, 6 gồm `cinema, stay-in, cinema`. `Parents` phân chia hoàn hảo: `visit -> cinema`, `no-visit -> stay-in`.
- `Weather = windy`: các mẫu 3, 7, 8, 9 gồm ba `cinema`, một `shopping`. `Parents` phân chia tốt nhất: `visit -> cinema`; với `no-visit`, dùng `Cash`: `poor -> cinema`, `rich -> shopping`.

Cây ID3:

```text
Weather?
├── sunny -> Parents?
│   ├── visit    -> cinema
│   └── no-visit -> tennis
├── rainy -> Parents?
│   ├── visit    -> cinema
│   └── no-visit -> stay-in
└── windy -> Parents?
    ├── visit    -> cinema
    └── no-visit -> Cash?
        ├── poor -> cinema
        └── rich -> shopping
```

Bộ luật là sáu đường đi từ gốc đến sáu lá của cây trên.

### b. Phân lớp mẫu 11

Mẫu 11 có `Weather = sunny`, `Parents = no-visit`, nên đi đến lá `tennis`. Hai thuộc tính còn lại không cần xét.

$$
\boxed{\text{ID3 dự đoán mẫu 11 là tennis}.}
$$

### c. So sánh với Naïve Bayes

Với mẫu:

$$
X=(sunny,no\text{-}visit,poor,yes),
$$

Naïve Bayes không làm trơn cho các score chưa chuẩn hóa:

$$
\begin{aligned}
score(cinema)
&=\frac6{10}\cdot\frac16\cdot\frac16\cdot\frac36\cdot\frac36
=\frac1{240}\approx0.00417,\\
score(tennis)
&=\frac2{10}\cdot\frac22\cdot\frac22\cdot\frac02\cdot\frac02=0,\\
score(stay\text{-}in)&=0,\\
score(shopping)&=0.
\end{aligned}
$$

Vì vậy Naïve Bayes **không làm trơn** dự đoán `cinema`, khác kết quả `tennis` của ID3.

Nếu môn học yêu cầu Laplace add-one để xử lý xác suất 0, với số giá trị lần lượt của `Weather, Parents, Cash, Exam` là `3,2,2,2`:

$$
\begin{aligned}
score_L(cinema)&=0.6\cdot\frac29\cdot\frac28\cdot\frac48\cdot\frac48
\approx0.00833,\\
score_L(tennis)&=0.2\cdot\frac35\cdot\frac34\cdot\frac14\cdot\frac14
=0.005625.
\end{aligned}
$$

Hai lớp một-mẫu có score nhỏ hơn. Khi dùng Laplace, Naïve Bayes vẫn dự đoán `cinema`. Vì vậy trong cả hai cách xử lý, kết quả Naïve Bayes khác với kết quả `tennis` của ID3; khi làm bài vẫn nên ghi rõ có dùng làm trơn hay không.

---

## Câu 2. Minimax và Alpha-Beta

### 1. Sao lưu giá trị bằng Minimax

Các nút MIN ngay trên lá:

| Nút | Phép tính | Giá trị |
|---|---|---:|
| H | min(99, 8) | 8 |
| I | min(5, 16) | 5 |
| J | min(83, 6) | 6 |
| K | min(6, 15) | 6 |
| L | min(18, 18) | 18 |
| M | min(22, 28) | 22 |
| N | min(99, 8) | 8 |
| O | min(90, 17) | 17 |

Các nút MAX kế tiếp:

$$
D=\max(8,5)=8,\quad E=\max(6,6)=6,
$$

$$
F=\max(18,22)=22,\quad G=\max(8,17)=17.
$$

Các nút MIN ở độ sâu 1 và nút gốc:

$$
B=\min(8,6)=6,\quad C=\min(22,17)=17,
$$

$$
A=\max(6,17)=17.
$$

**MAX chọn nhánh phải qua `C`.**

### 2a. Alpha-Beta theo thứ tự trái sang phải

Ghi cặp `(alpha, beta)` lúc đi vào nút và kết quả trả về:

```text
A MAX (-inf,+inf)
├── B MIN (-inf,+inf)
│   ├── D MAX (-inf,+inf)
│   │   ├── H MIN (-inf,+inf): min(99,8)=8
│   │   └── I MIN (8,+inf): đọc 5, beta=5 <= alpha=8
│   │       └── cắt lá 16
│   │   D=8
│   └── E MAX (-inf,8)
│       ├── J MIN (-inf,8): min(83,6)=6
│       └── K MIN (6,8): đọc 6, beta=6 <= alpha=6
│           └── cắt lá 15
│       E=6
│   B=6
└── C MIN (6,+inf)
    ├── F MAX (6,+inf)
    │   ├── L MIN (6,+inf): 18
    │   └── M MIN (18,+inf): 22
    │   F=22
    └── G MAX (6,22)
        ├── N MIN (6,22): 8
        └── O MIN (8,22): 17
        G=17
    C=17
A=17
```

Hai lá không được kiểm tra là:

$$
\boxed{16\text{ (con phải của I), }15\text{ (con phải của K)}}.
$$

### 2b. Nước đi và quan hệ với Minimax

Alpha-Beta trả `A = 17`, nên MAX vẫn đi **phải**, qua `C`.

Nói chung, với cùng cây, cùng độ sâu và cùng hàm đánh giá, Alpha-Beta luôn trả cùng giá trị và nước đi tối ưu như Minimax. Thứ tự duyệt chỉ thay đổi số nút được cắt, không thay đổi kết quả.

### 3a. Sắp xếp để cắt được nhiều nút

Nguyên tắc ordering:

- tại node MAX, xét nút có giá trị ước lượng lớn trước;
- tại node MIN, xét nút có giá trị ước lượng nhỏ trước.

Từ các giá trị sao lưu `B=6`, `C=17` và Eval `D=9`, `E=7`, `F=24`, `G=16`, thứ tự nên là:

```text
A: C trước, B sau
C: G trước, F sau
B: E trước, D sau
```

Ở tầng kế tiếp dùng giá trị Minimax đã tính để ordering:

```text
G: O trước, N sau       F: M trước, L sau
E: J/K theo thứ tự nào cũng được (đều bằng 6)
D: H trước, I sau
```

Trong mỗi node MIN ngay trên lá, xét lá nhỏ trước:

```text
H: 8,99    I: 5,16    J: 6,83    K: 6,15
L: 18,18   M: 22,28   N: 8,99    O: 17,90
```

Một cây đã sắp xếp hợp lệ theo thứ tự DFS trái sang phải:

```text
A
├── C
│   ├── G
│   │   ├── O: 17, 90
│   │   └── N: 8, 99
│   └── F
│       ├── M: 22, 28
│       └── L: 18, 18
└── B
    ├── E
    │   ├── J: 6, 83
    │   └── K: 6, 15
    └── D
        ├── H: 8, 99
        └── I: 5, 16
```

### 3b. Số nút không được kiểm tra

Với ordering trên, các phần bị cắt là:

- lá `99` thứ hai dưới `N`: 1 nút;
- toàn bộ cây con `L`: `L` và 2 lá, tổng 3 nút;
- lá `83` dưới `J`: 1 nút;
- lá `15` dưới `K`: 1 nút;
- toàn bộ cây con `D`: `D`, `H`, `I` và 4 lá, tổng 7 nút.

Tổng cộng:

$$
\boxed{1+3+1+1+7=13\text{ nút không được kiểm tra}.}
$$

---

## Câu 3. Chứng minh bằng logic vị từ

KB:

$$
\begin{aligned}
1.\;&\forall x\,[p(x)\leftrightarrow(q(x)\lor r(x))],\\
2.\;&\forall y\,[\neg q(y)\Rightarrow p(y)],\\
3.\;&p(1),\\
4.\;&p(2),\\
5.\;&q(1),\\
6.\;&\neg q(2).
\end{aligned}
$$

Cần chứng minh `exists z r(z)`.

Từ chiều `p(x) => q(x) or r(x)` của mệnh đề tương đương, ta có clause:

$$
\neg p(x)\lor q(x)\lor r(x).
$$

Resolution:

1. Thế `x/2`: `¬p(2) or q(2) or r(2)`.
2. Resolve với `p(2)`, suy ra `q(2) or r(2)`.
3. Resolve với `¬q(2)`, suy ra `r(2)`.
4. Existential Generalization: từ `r(2)` suy ra `exists z r(z)`.

Vậy:

$$
\boxed{KB\models\exists z\,r(z)}.
$$

Nhận xét: các mệnh đề 2, 3 và 5 không cần dùng trong chứng minh này.
