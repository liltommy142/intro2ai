# Bản đồ ôn thi Final theo slide

> Mục tiêu: khi quên một chủ đề, mở đúng file PDF và nhảy tới đúng **trang PDF** được ghi dưới đây.
>
> Cơ sở ưu tiên: đối chiếu syllabus, slide môn học và ba đề cuối kỳ 2021-2022, 2022-2023, 2023-2024 trong thư mục `finalexam`.

## Thứ tự học chắc cú nhất

1. **ID3 Decision Tree**
2. **Logic mệnh đề và logic vị từ**
3. **Minimax và Alpha-Beta pruning**
4. **Naïve Bayes**
5. **CSP và Backtracking**
6. **Perceptron, MLP và Backpropagation**
7. **BFS, UCS, DFS, Greedy và A\***
8. **PEAS, loại agent, local search và lịch sử AI**

Ba đề cũ cho thấy:

| Nội dung | Tần suất thấy trong 3 đề |
|---|---:|
| ID3/Decision Tree | 3/3 |
| PL/FOL và suy diễn logic | 3/3 |
| CSP/Backtracking | 1/3 |
| Minimax/Alpha-Beta | 1/3, nằm trong đề gần nhất |
| Naïve Bayes | 1/3, nằm trong đề gần nhất |
| Neural Network | 0/3, nhưng có trong syllabus và slide hiện tại |

---

## 1. ID3 Decision Tree - ưu tiên cao nhất

**Slide:** [Lecture 10 - Basic Machine Learning](../slides/2023-Lecture10-BasicML.pdf)

Đọc theo thứ tự:

- Trang 33-38: ý tưởng chia để trị, thuật toán dựng cây và các trường hợp dừng.
- Trang 40-42: entropy.
- Trang 43-54: average entropy và information gain; cách chọn thuộc tính.
- Trang 50 và 54: ví dụ tính hoàn chỉnh trên bộ dữ liệu nhà hàng.
- Trang 57: quiz dựng cây nhận diện virus - nên tự giải từ đầu đến cuối.

Công thức phải nhớ:

```text
H(S) = -Σ pᵢ log₂(pᵢ)

AE(A) = Σᵥ (|Sᵥ| / |S|) H(Sᵥ)

IG(A, S) = H(S) - AE(A)
```

Sau khi học phải làm được:

- Tính entropy của nhãn.
- Tính AE và IG của từng thuộc tính.
- Chọn root và tiếp tục chia từng nhánh.
- Xử lý nhánh toàn cùng class, hết thuộc tính hoặc không còn mẫu.
- Vẽ cây hoàn chỉnh, rút các luật `IF ... THEN ...` và phân loại mẫu mới.

Đề để luyện:

- [Final 2021-2022, trang 1](20212022/1.png): dùng Gain Ratio.
- [Final 2022-2023, trang 1](20222023/1.png): dùng Information Gain.
- [Final 2023-2024, trang 1](20232024/1.png): ID3 và phân loại mẫu mới.

> Với slide hiện tại, học **Information Gain** trước. Gain Ratio chỉ xem thêm để làm được đề 2021-2022.

---

## 2. Logic mệnh đề - PL

**Slide:** [Lecture 7 - Logical Agents](../slides/2023-Lecture07-LogicalAgents.pdf)

Đọc theo thứ tự:

- Trang 19-22 và 27-32: model, entailment `KB ⊨ α` và model checking.
- Trang 44-54: resolution và quy trình chứng minh bằng phản chứng.
- Trang 48-50: chuyển công thức sang CNF.
- Trang 83: quiz Forward Chaining và Backward Chaining.
- Trang 84: quiz DPLL/Davis-Putnam.

Quy trình resolution phải thuộc:

1. Viết KB và query bằng logic.
2. Thêm **phủ định query** vào KB.
3. Khử `↔` và `→`.
4. Đẩy phủ định vào trong.
5. Chuyển tất cả mệnh đề sang CNF/clause.
6. Resolve các literal đối ngẫu.
7. Suy ra clause rỗng `□` thì kết luận `KB ⊨ query`.

Sau khi học phải làm được:

- Phân biệt `KB ⊨ α` với việc `α` đúng trong một model riêng lẻ.
- Chuyển `P → Q` thành `¬P ∨ Q`.
- Chuyển công thức có `↔`, `→`, `¬`, `∧`, `∨` về CNF.
- Ghi rõ hai clause cha ở mỗi bước resolution.
- Chạy forward/backward chaining trên definite/Horn clauses.

Đề để luyện:

- [Final 2021-2022, trang 2](20212022/2.png): kiểm tra hai kết luận từ KB mệnh đề.

---

## 3. Logic vị từ - FOL

**Slide:** [Lecture 8 - First-Order Logic](../slides/2023-Lecture08-FirstOrderLogic.pdf)

Đọc theo thứ tự:

- Trang 40: bài tập dịch câu tiếng Anh sang FOL.
- Trang 42-45: Universal Instantiation và Existential Instantiation.
- Trang 48-51: Generalized Modus Ponens.
- Trang 50-57: unification, substitution và MGU; trang 57 là quiz.
- Trang 69: quiz Forward Chaining đến fixed point.
- Trang 80-81: quiz Backward Chaining và tìm substitution trả lời.
- Trang 83-86: sáu bước chuyển FOL sang CNF và Skolemization.
- Trang 87-92: FOL resolution; trang 92 là quiz tổng hợp.

Sáu bước FOL sang CNF:

1. Khử `↔`.
2. Khử `→` bằng `¬P ∨ Q`.
3. Đẩy `¬` vào trong.
4. Standardize variables apart.
5. Skolemize các biến tồn tại `∃`.
6. Bỏ lượng từ `∀`, phân phối `∨` qua `∧` và tách clause.

Bẫy thường gặp:

- Dùng sai `∀` và `∃` khi dịch câu.
- Dùng lại cùng một Skolem constant cho hai biến tồn tại khác nhau.
- Quên rằng Skolem function phải phụ thuộc các biến `∀` đang nằm ngoài nó.
- Unify hai mệnh đề mà chưa standardize apart.
- Không ghi phép thế `θ` trong bước resolution.

Đề để luyện:

- [Final 2022-2023, trang 1](20222023/1.png) và [trang 2](20222023/2.png): dịch sáu câu sang FOL rồi chứng minh bằng resolution.
- [Final 2023-2024, trang 4](20232024/4.png): chứng minh `∃z r(z)` từ KB.

---

## 4. Minimax và Alpha-Beta pruning

**Slide:** [Lecture 5 - Adversarial Search](../slides/2023-Lecture05-AdversarialSearch.pdf)

Đọc theo thứ tự:

- Trang 18-21: Minimax và cách backup giá trị từ lá lên gốc.
- Trang 22: độ phức tạp `O(b^m)` và không gian `O(bm)`.
- Trang 26-32: Alpha-Beta pruning và move ordering.
- Trang 33-38: depth cutoff và evaluation function.
- Trang 39-45: stochastic game/expectiminimax - đọc sau cùng.

Quy tắc phải thuộc:

```text
Node MAX:
  v = max(v, child)
  nếu v >= beta thì prune
  alpha = max(alpha, v)

Node MIN:
  v = min(v, child)
  nếu v <= alpha thì prune
  beta = min(beta, v)
```

Sau khi học phải làm được:

- Ghi đúng tầng MAX/MIN.
- Tính Minimax từ dưới lên.
- Chạy DFS trái sang phải và ghi `(α, β)` khi vào mỗi node.
- Đánh dấu tất cả node/nhánh không được kiểm tra.
- Sắp xếp nhánh để Alpha-Beta cắt được nhiều nhất.
- Giải thích Alpha-Beta không thay đổi giá trị root so với Minimax.

Đề để luyện:

- [Final 2023-2024, trang 2](20232024/2.png): Minimax và bắt đầu Alpha-Beta.
- [Final 2023-2024, trang 3](20232024/3.png): Alpha-Beta và thông tin ordering.
- [Final 2023-2024, trang 4](20232024/4.png): sắp xếp lại cây và đếm node bị cắt.

---

## 5. Naïve Bayes

**Slide:** [Lecture 10 - Basic Machine Learning](../slides/2023-Lecture10-BasicML.pdf)

Đọc theo thứ tự:

- Trang 62-64: định lý Bayes.
- Trang 64-68: Naïve Bayes và ví dụ phân loại hoàn chỉnh.
- Trang 69-72: xác suất bằng 0 và Laplace correction.
- Trang 73: missing values.
- Trang 74: ưu, nhược điểm và giả định conditional independence.
- Trang 75: quiz phân loại virus - nên tự giải cả hai trường hợp có/không Laplace.

Công thức:

```text
P(C | X) ∝ P(C) × Π P(xₖ | C)
```

Khi so sánh các class, thường không cần tính mẫu số `P(X)` vì giống nhau cho mọi class.

Sau khi học phải làm được:

- Tính prior `P(C)`.
- Tính từng conditional probability `P(xₖ | C)`.
- Nhân likelihood và prior cho từng class.
- Chọn class có giá trị lớn nhất.
- Áp dụng Laplace khi một xác suất bằng 0.
- So sánh kết quả Naïve Bayes với ID3 trên cùng một mẫu.

Đề để luyện:

- [Final 2023-2024, trang 1](20232024/1.png) và phần đầu [trang 2](20232024/2.png).

---

## 6. CSP và Backtracking

**Slide:** [Lecture 6 - Constraint Satisfaction Problem](../slides/2023-Lecture06-CSP.pdf)

Đọc theo thứ tự:

- Trang 7-11: `Variables`, `Domains`, `Constraints`; ví dụ map coloring.
- Trang 12-14: scheduling và cách viết ràng buộc trước-sau/không chồng lấn.
- Trang 24-29: Arc Consistency và AC-3.
- Trang 30-38: Backtracking, MRV, degree heuristic và LCV.
- Trang 38-40: Forward Checking so với Arc Consistency.
- Trang 43-47: ba quiz map coloring, AC vs Forward Checking và timetable.
- Trang 48-53: min-conflicts - ưu tiên thấp hơn.
- Trang 56-60: tree-structured CSP - ưu tiên thấp hơn.

Sau khi học phải làm được:

- Mô hình bài toán thành `X`, `D`, `C`.
- Vẽ constraint graph.
- Vẽ cây backtracking theo đúng thứ tự biến/giá trị đề cho.
- Dùng MRV, degree và LCV để chọn bước kế tiếp.
- Chạy Forward Checking và AC-3, ghi rõ giá trị bị xóa khỏi domain.

Đề để luyện:

- [Final 2021-2022, trang 2](20212022/2.png): Sudoku 4×4, viết constraints và vẽ cây backtracking.

---

## 7. Perceptron, MLP và Backpropagation

**Slide:** [Lecture 11 - Neural Networks](../slides/2023-Lecture11-NeuralNetworks.pdf)

Đọc theo thứ tự:

- Trang 14-16: perceptron, activation và learning rule.
- Trang 17-19: AND/OR và lý do perceptron không học được XOR.
- Trang 20-22: ví dụ và quiz tính output perceptron.
- Trang 24-29: MLP, sigmoid, forward pass, backpropagation và SSE.
- Trang 34-37: gradient descent, local minimum, plateau và saddle point.
- Trang 38-44: tanh, momentum và adaptive learning rate - học sau cùng.
- Trang 45-47: quiz forward pass và backpropagation.

Công thức cốt lõi:

```text
Perceptron:
Y = step(Σ xᵢwᵢ - θ)
e = Yd - Y
Δwᵢ = αxᵢe

Sigmoid:
σ(x) = 1 / (1 + e^(-x))

Output gradient:
δₖ = yₖ(1-yₖ)(ydₖ-yₖ)

Hidden gradient:
δⱼ = yⱼ(1-yⱼ)Σₖ(δₖwⱼₖ)
```

Sau khi học phải làm được:

- Tính output perceptron cho mọi tổ hợp input nhị phân.
- Thực hiện một bước cập nhật trọng số perceptron.
- Tính forward pass qua một hidden layer.
- Tính output error, hidden error và weight correction cho một bước backprop.

---

## 8. Search cơ bản và A* - phần dự phòng

### Problem formulation

**Slide:** [Lecture 3.1 - Problem Solving by Searching](../slides/2023-Lecture03-P1-ProblemSolvingBySearching.pdf)

- Trang 12-14: năm thành phần của bài toán tìm kiếm.
- Trang 34-40: tree search, graph search, frontier, explored set và cấu trúc node.
- Trang 41: completeness, optimality, time và space.

### Uninformed Search

**Slide:** [Lecture 3.2 - Uninformed Search](../slides/2023-Lecture03-P2-UninformedSearch.pdf)

- Trang 8-21: BFS; trang 21 là quiz.
- Trang 24-41: UCS; trang 41 là quiz.
- Trang 43-48: DFS; trang 48 là quiz.
- Trang 50-52: Depth-Limited Search.
- Trang 54-57: Iterative Deepening Search.
- Trang 59-60: Bidirectional Search.

### Informed Search

**Slide:** [Lecture 3.3 - Informed Search](../slides/2023-Lecture03-P3-InformedSearch.pdf)

- Trang 12-18: Greedy Best-First Search.
- Trang 20-28: A* với `f(n) = g(n) + h(n)`.
- Trang 30-36: admissible, consistent và optimality.
- Trang 31-32: misplaced tiles và Manhattan distance cho 8-puzzle.
- Trang 57-60: dominance, relaxed problem và kết hợp nhiều heuristic.

Sau khi học phải làm được:

- Ghi expanded order và returned path.
- Theo dõi frontier theo đúng FIFO/LIFO/priority.
- Với UCS/A*, cập nhật node nếu tìm được đường rẻ hơn.
- Nhớ UCS/A* chỉ kết thúc khi goal được lấy ra khỏi priority queue.
- Kiểm tra `h(n) ≤ h*(n)` và `h(n) ≤ c(n,n') + h(n')`.

---

## 9. Các phần chỉ ôn khi còn thời gian

### Intelligent Agents

**Slide:** [Lecture 2 - Intelligent Agents](../slides/2023-Lecture02-IntelligentAgents.pdf)

- Trang 5-23: agent, rationality, performance measure và autonomy.
- Trang 26-32: PEAS và quiz.
- Trang 33-42: phân loại task environment và quiz.
- Trang 49-59: simple reflex, model-based, goal-based và utility-based agents.
- Trang 60-64: bốn thành phần của learning agent.

### Local Search

**Slide:** [Lecture 4 - Local Search](../slides/2023-Lecture04-LocalSearch.pdf)

- Trang 10-19: Hill Climbing và quiz 4-Queens.
- Trang 21-22: Simulated Annealing, xác suất nhận `e^(ΔE/T)`.
- Trang 24-25: Local Beam Search.
- Trang 27-38: Genetic Algorithm; trang 33 là quiz fitness/selection.

### Introduction to AI

**Slide:** [Lecture 1 - Introduction to AI](../slides/2023-Lecture01-IntroductionToAI.pdf)

- Trang 11-18: các định nghĩa AI và Turing Test.
- Trang 21-22: các lĩnh vực nền tảng của AI.
- Trang 27-28: các mốc lịch sử chính.

---

## Kế hoạch nếu chỉ còn một ngày

### Buổi 1 - ID3 và Naïve Bayes

1. Đọc Lecture 10 trang 33-57.
2. Tự giải quiz trang 57.
3. Đọc trang 62-75.
4. Tự giải quiz trang 75.
5. Làm lại Câu 1 của đề 2023-2024.

### Buổi 2 - Logic

1. Ôn PL → CNF → resolution trong Lecture 7.
2. Ôn FOL translation, unification, Skolemization và resolution trong Lecture 8.
3. Làm lại Câu 2 đề 2022-2023 và Câu 3 đề 2023-2024.

### Buổi 3 - Minimax và Alpha-Beta

1. Đọc Lecture 5 trang 18-38.
2. Làm toàn bộ Câu 2 đề 2023-2024.
3. Kiểm tra lại mọi điều kiện prune và move ordering.

### Thời gian còn lại

1. CSP/Backtracking.
2. Perceptron và một bước backpropagation.
3. A* và bảng so sánh các thuật toán search.

---

## Checklist trước khi đi thi

- [ ] Tự dựng được một cây ID3 không nhìn lời giải.
- [ ] Tự tính được Naïve Bayes có Laplace correction.
- [ ] Chuyển được PL/FOL sang CNF.
- [ ] Chứng minh được một query bằng resolution và ghi rõ substitution.
- [ ] Chạy được Minimax và Alpha-Beta, đánh dấu đúng node bị prune.
- [ ] Viết được `Variables`, `Domains`, `Constraints` cho một CSP.
- [ ] Thực hiện được một bước perceptron/backprop.
- [ ] Chạy được BFS/UCS/A* trên một graph nhỏ.

> Quy định thi phải theo thông báo hiện tại. Một số đề cũ đánh dấu được dùng tài liệu, nhưng syllabus hiện tại ghi closed-book.
