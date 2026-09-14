# Lời giải Final Exam 2021-2022

Nguồn đề: [trang 1](1.png), [trang 2](2.png).

## Câu 1. Xây dựng cây quyết định bằng Gain Ratio

Tập huấn luyện có 7 mẫu, gồm 4 mẫu lớp `O` và 3 mẫu lớp `M`.

$$
H(S)=-\frac47\log_2\frac47-\frac37\log_2\frac37=0.9852
$$

### a. Chọn thuộc tính và dựng cây

Các giá trị tại nút gốc:

| Thuộc tính | Information Gain | Split Information | Gain Ratio |
|---|---:|---:|---:|
| Age | 0.0202 | 0.9852 | 0.0205 |
| Income | 0.1281 | 0.9852 | 0.1300 |
| Education | 0.3060 | 1.5567 | **0.1965** |

Vì `Education` có Gain Ratio lớn nhất nên nó là nút gốc.

- `Education = University`: cả hai mẫu đều là `O`, nên đây là lá `O`.
- `Education = Highschool`: có 1 mẫu `O`, 2 mẫu `M`. So sánh hai thuộc tính còn lại:
  - `GR(Age) = 0.2740`;
  - `GR(Income) = 1.0000`.
  Chọn `Income`: `High -> O`, `Low -> M`.
- `Education = College`: có 1 mẫu `O`, 1 mẫu `M`. `Income` không phân chia được vì cả hai đều `High`; `Age` phân chia hoàn hảo nên `GR(Age)=1`: `<35 -> O`, `>=35 -> M`.

Cây quyết định:

```text
Education?
├── University  -> O
├── Highschool  -> Income?
│   ├── High    -> O
│   └── Low     -> M
└── College     -> Age?
    ├── < 35    -> O
    └── >= 35   -> M
```

Bộ luật phân lớp:

1. `Education = University -> Candidate = O`.
2. `Education = Highschool AND Income = High -> Candidate = O`.
3. `Education = Highschool AND Income = Low -> Candidate = M`.
4. `Education = College AND Age < 35 -> Candidate = O`.
5. `Education = College AND Age >= 35 -> Candidate = M`.

### b. Phân lớp cử tri `(<35, High, University)`

Tại gốc, `Education = University` đi thẳng tới lá `O`.

**Kết luận: cử tri này ủng hộ ứng viên `O`.**

---

## Câu 2. Sudoku 4 x 4 và Backtracking

Ký hiệu miền của mọi biến là:

$$
D(X_{ij})=\{1,2,3,4\}.
$$

### 1. Các ràng buộc

Các ô đã cho:

$$
X_{11}=3,\quad X_{12}=4,\quad X_{23}=3,\quad X_{33}=4,\quad X_{34}=2.
$$

Ràng buộc hàng:

$$
\operatorname{AllDiff}(X_{i1},X_{i2},X_{i3},X_{i4}),\quad i=1,2,3,4.
$$

Ràng buộc cột:

$$
\operatorname{AllDiff}(X_{1j},X_{2j},X_{3j},X_{4j}),\quad j=1,2,3,4.
$$

Ràng buộc bốn khối 2 x 2:

$$
\begin{aligned}
&\operatorname{AllDiff}(X_{11},X_{12},X_{21},X_{22}),\\
&\operatorname{AllDiff}(X_{13},X_{14},X_{23},X_{24}),\\
&\operatorname{AllDiff}(X_{31},X_{32},X_{41},X_{42}),\\
&\operatorname{AllDiff}(X_{33},X_{34},X_{43},X_{44}).
\end{aligned}
$$

### 2. Cây Backtracking cho `X13`, `X14`, `X21`

Duyệt biến theo đúng thứ tự đề bài và thử giá trị tăng dần:

```text
X13
├── 1
│   └── X14: không có giá trị
│       (hàng 1 buộc X14=2 nhưng cột 4 đã có X34=2) -> thất bại
├── 2
│   └── X14
│       ├── 1 -> X21
│       │       ├── 1 -> nhất quán cục bộ
│       │       └── 2 -> nhất quán cục bộ
│       ├── 2 -> sai hàng 1
│       ├── 3 -> sai hàng 1 (X11=3)
│       └── 4 -> sai hàng 1 (X12=4)
├── 3 -> sai hàng 1
└── 4 -> sai hàng 1
```

Nếu Backtracking tiếp tục cho đến khi hoàn thành toàn bộ bảng, nhánh `X21=1` sẽ thất bại ở các biến sau; nghiệm duy nhất là:

```text
3 4 2 1
2 1 3 4
1 3 4 2
4 2 1 3
```

Do đó trong nghiệm hoàn chỉnh:

$$
\boxed{X_{13}=2,\quad X_{14}=1,\quad X_{21}=2}.
$$

---

## Câu 3. Suy diễn logic mệnh đề

$$
KB=\{A\lor C,\ A\Rightarrow(B\land E),\ C\Rightarrow(E\lor D),\ E\Rightarrow F\}.
$$

Đưa về các clause cần dùng:

$$
\begin{aligned}
&A\lor C,\\
&\neg A\lor B,\\
&\neg A\lor E,\\
&\neg C\lor E\lor D,\\
&\neg E\lor F.
\end{aligned}
$$

### a. Có suy ra `F` không?

Không. Một phản mô hình là:

$$
A=0,\ C=1,\ B=0,\ E=0,\ D=1,\ F=0.
$$

Mọi mệnh đề trong `KB` đều đúng nhưng `F` sai. Vì vậy:

$$
\boxed{KB\not\models F}.
$$

### b. Có suy ra `¬D => F` không?

`¬D => F` tương đương `D or F`. Chứng minh bằng resolution phản chứng, thêm phủ định của kết luận:

$$
\neg(D\lor F)\equiv \neg D\land\neg F.
$$

Các bước resolution:

1. Từ `¬E or F` và `¬F`, suy ra `¬E`.
2. Từ `¬A or E` và `¬E`, suy ra `¬A`.
3. Từ `A or C` và `¬A`, suy ra `C`.
4. Từ `¬C or E or D` và `C`, suy ra `E or D`.
5. Từ `E or D` và `¬E`, suy ra `D`.
6. Từ `D` và `¬D`, suy ra clause rỗng `□`.

Vậy phủ định kết luận gây mâu thuẫn:

$$
\boxed{KB\models(\neg D\Rightarrow F)}.
$$
