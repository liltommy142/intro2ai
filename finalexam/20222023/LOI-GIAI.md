# Lời giải Final Exam 2022-2023

Nguồn đề: [trang 1](1.png), [trang 2](2.png).

## Câu 1. ID3 trên bảng thời tiết

Chỉ dùng 14 mẫu đã có nhãn để huấn luyện. Trong đó có 9 mẫu `Yes` và 5 mẫu `No`:

$$
H(S)=-\frac9{14}\log_2\frac9{14}-\frac5{14}\log_2\frac5{14}=0.9403.
$$

### a. Xây dựng cây và bộ luật phân lớp

Information Gain tại nút gốc:

| Thuộc tính | Information Gain |
|---|---:|
| Outlook | **0.2467** |
| Humidity | 0.1518 |
| Windy | 0.0481 |
| Temperature | 0.0292 |

Chọn `Outlook` làm gốc.

- `Outlook = Overcast`: cả 4 mẫu đều `Yes`.
- `Outlook = Sunny`: có 2 `Yes`, 3 `No`. `Humidity` phân chia hoàn hảo: `High -> No`, `Normal -> Yes`.
- `Outlook = Rain`: có 3 `Yes`, 2 `No`. `Windy` phân chia hoàn hảo: `False -> Yes`, `True -> No`.

Cây ID3:

```text
Outlook?
├── Overcast -> Yes
├── Sunny    -> Humidity?
│   ├── High   -> No
│   └── Normal -> Yes
└── Rain     -> Windy?
    ├── False -> Yes
    └── True  -> No
```

Bộ luật:

1. `Outlook = Overcast -> Class = Yes`.
2. `Outlook = Sunny AND Humidity = High -> Class = No`.
3. `Outlook = Sunny AND Humidity = Normal -> Class = Yes`.
4. `Outlook = Rain AND Windy = False -> Class = Yes`.
5. `Outlook = Rain AND Windy = True -> Class = No`.

### b. Phân lớp mẫu 15 và 16

- Mẫu 15: `Outlook = Overcast`, nên `Class = Yes`.
- Mẫu 16: `Outlook = Rain`, `Windy = True`, nên `Class = No`.

$$
\boxed{\text{Mẫu 15 = Yes, mẫu 16 = No}.}
$$

---

## Câu 2. Logic vị từ và resolution

Quy ước hằng:

- `Jack`, `Curiosity`, `Tuna` là các cá thể tương ứng;
- với câu 1, dùng một biến tồn tại để biểu diễn "một con chó".

### a. Biểu diễn sáu câu bằng logic bậc nhất

1. Jack sở hữu một con chó:

$$
\exists x\,[D(x)\land O(Jack,x)].
$$

2. Ai sở hữu một con chó là người yêu động vật:

$$
\forall x\forall y\,[(D(y)\land O(x,y))\Rightarrow L(x)].
$$

3. Người yêu động vật không giết động vật:

$$
\forall x\forall y\,[(L(x)\land A(y))\Rightarrow\neg K(x,y)].
$$

4. Jack giết Tuna hoặc Curiosity giết Tuna:

$$
K(Jack,Tuna)\lor K(Curiosity,Tuna).
$$

5. Tuna là một con mèo:

$$
C(Tuna).
$$

6. Mọi con mèo đều là động vật:

$$
\forall x\,[C(x)\Rightarrow A(x)].
$$

### b. Curiosity có giết Tuna không?

Skolem hóa câu 1 bằng hằng `d`:

$$
D(d),\qquad O(Jack,d).
$$

Các clause cần dùng:

$$
\begin{aligned}
&D(d),\\
&O(Jack,d),\\
&\neg D(y)\lor\neg O(x,y)\lor L(x),\\
&\neg L(x)\lor\neg A(y)\lor\neg K(x,y),\\
&K(Jack,Tuna)\lor K(Curiosity,Tuna),\\
&C(Tuna),\\
&\neg C(x)\lor A(x).
\end{aligned}
$$

Suy diễn bằng resolution:

1. Từ clause 3 với `D(d)` và `O(Jack,d)`, suy ra `L(Jack)`.
2. Từ `C(Tuna)` và `¬C(x) or A(x)` với phép thế `x/Tuna`, suy ra `A(Tuna)`.
3. Từ clause 4, `L(Jack)` và `A(Tuna)`, suy ra `¬K(Jack,Tuna)`.
4. Từ `K(Jack,Tuna) or K(Curiosity,Tuna)` và `¬K(Jack,Tuna)`, suy ra `K(Curiosity,Tuna)`.

Do đó:

$$
\boxed{KB\models K(Curiosity,Tuna).}
$$

**Kết luận: Curiosity có giết Tuna.**
