# Vấn đáp Intro2AI - sổ tay trả lời từ repo

> Mục tiêu: nói được ý chính trong khoảng 30-60 giây, sau đó mở rộng khi bị hỏi sâu. Nội dung dưới đây bám vào slide, đề Final, hai lab và project DUSt3R đang có trong repository. Không biến kết quả benchmark cũ thành khẳng định về lần chấm cuối nếu chưa chạy lại.

## Cách trả lời

Mỗi câu nên theo thứ tự: **định nghĩa/ý tưởng -> cơ chế -> lý do chọn hoặc giới hạn -> ví dụ trong repo**. Nếu chưa chắc một số đo, nói rõ đó là kết quả của bộ test đã lưu, không phải kết quả chấm chính thức.

## 1. Bức tranh môn học

### 1. AI là gì? Agent là gì?

**Nói ngắn:** AI nghiên cứu cách xây hệ thống có thể nhận biết môi trường, suy luận và hành động để đạt mục tiêu. Một agent nhận percept từ môi trường rồi chọn action. Agent hợp lý không có nghĩa là luôn thắng, mà chọn hành động làm tối đa performance measure dựa trên percept sequence và kiến thức hiện có.

**Bị hỏi sâu:** Muốn mô tả đúng một agent, dùng PEAS: Performance measure, Environment, Actuators, Sensors. Với Hide-and-Seek: performance là Pacman bắt nhanh hoặc Ghost sống đủ lâu; môi trường là maze; actuator là Move; sensor là `map_state`, vị trí mình và, tùy Lab, vị trí đối thủ.

**Nguồn:** `slides/2023-Lecture01-IntroductionToAI.pdf`, `slides/2023-Lecture02-IntelligentAgents.pdf`, `labs/lab1/HideSeek/pacman/src/agent_interface.py`.

### 2. Phân biệt problem formulation và search?

**Nói ngắn:** Problem formulation quyết định ta tìm cái gì: initial state, actions, transition model, goal test, path cost. Search là thuật toán duyệt không gian trạng thái đã được mô hình hóa đó. Formulation sai thì dùng A* hay BFS cũng không cứu được.

**Ví dụ:** Lab 1 coi một ô maze là state; action là bốn hướng; tường là trạng thái không hợp lệ; goal Pacman là đến vị trí Ghost. `astar()` trong `labs/lab1/final/agent.py` chỉ hoạt động đúng vì `is_valid()` và `get_neighbors()` mô tả maze đúng.

### 3. Bốn tiêu chí đánh giá search là gì?

**Nói ngắn:** Completeness: có tìm được nghiệm nếu nghiệm tồn tại không. Optimality: nghiệm có chi phí thấp nhất không. Time complexity và space complexity đo tài nguyên. Khi chọn thuật toán phải nói rõ giả định về chi phí cạnh, branching factor và heuristic.

## 2. Search và tối ưu

### 4. BFS, UCS, DFS và IDS khác nhau thế nào?

| Thuật toán | Chọn node theo | Khi nào tối ưu | Điểm cần nhớ |
|---|---|---|---|
| BFS | độ sâu nhỏ nhất | mọi cost cạnh bằng nhau | đầy đủ nhưng tốn bộ nhớ |
| UCS | path cost `g(n)` nhỏ nhất | cost cạnh không âm | tối ưu với cost dương/không âm phù hợp |
| DFS | đi sâu trước | không đảm bảo | ít bộ nhớ, có thể lạc/vòng lặp |
| IDS | lặp depth limit | cost cạnh bằng nhau | tính đầy đủ của BFS, bộ nhớ gần DFS |

**Nối repo:** `bfs_distances()` ở Lab 1 dùng BFS để lấy khoảng cách thật có tính tường. Nó không phải A*, vì nó cần khoảng cách từ một điểm đến toàn bộ các ô để làm heuristic/fallback.

### 5. A* làm gì và tại sao dùng trong Pacman?

**Nói ngắn:** A* ưu tiên node có `f(n)=g(n)+h(n)`: chi phí đã đi cộng ước lượng đến đích. Nếu `h` admissible, tức không overestimate chi phí còn lại, graph search với điều kiện phù hợp trả đường đi tối ưu. Pacman cần bắt nhanh nên code dùng `g` là số bước và Manhattan distance làm `h`.

**Trong code:** `labs/lab1/final/agent.py` và `labs/lab2/init/agent.py` dùng heap chứa `(f, g, counter, position, path)`. `counter` giúp thứ tự heap xác định khi các điểm bằng nhau. `follow_path()` chỉ gộp các bước đầu cùng hướng, vì luật cho Pacman đi tối đa hai ô thẳng hàng, không được rẽ giữa lượt.

**Giới hạn:** Manhattan không nhìn thấy tường nên có thể underestimate, không nhất thiết sát chi phí thật. Đây là lý do nó vẫn an toàn cho A* trên lưới 4 hướng, còn BFS distance chính xác hơn nhưng tốn hơn nếu tính lặp ở nhiều node.

### 6. Heuristic admissible và consistent là gì?

**Nói ngắn:** Admissible là `h(n) <= h*(n)`, không bao giờ đánh giá cao quá chi phí thật đến goal. Consistent là `h(n) <= c(n,n') + h(n')` với mọi cạnh. Consistency giúp `f` không giảm dọc đường đi và graph-search A* không phải mở lại node trong điều kiện chuẩn.

### 7. Vì sao Lab 2 dùng `!= 1`, không dùng `== 0`?

**Nói ngắn:** Trong framework Blind, `1` là tường luôn thấy; `-1` là ô trống đang bị fog, chứ không phải tường. Vì vậy ô đi được phải là mọi ô khác `1`. Nếu viết `==0`, agent xem gần như toàn bộ mê cung là chướng ngại và không lập đường đi xa được.

**Bằng chứng:** `labs/lab2/README.md` đối chiếu PDF, framework `get_observation` và QA; `is_valid()` của `labs/lab2/init/agent.py` cài đúng điều kiện này. Đây là một điểm nên giải thích thẳng: code bám framework thật sự chấm, đồng thời không lấy vị trí đối phương ngoài quan sát.

### 8. Local search có gì khác search theo path?

**Nói ngắn:** Local search thường chỉ giữ một hay vài trạng thái hiện tại, tối ưu theo hàm objective hơn là giữ cả path. Nó hợp với không gian lớn như n-queens hoặc tối ưu hóa. Hill-climbing dễ kẹt local maximum, plateau, ridge; simulated annealing đôi khi nhận bước xấu để thoát kẹt; genetic algorithm tiến hóa quần thể theo selection, crossover, mutation.

**Bẫy:** Không nói hill-climbing là luôn tối ưu. Nó thường hiệu quả bộ nhớ nhưng không đảm bảo global optimum.

## 3. Adversarial search và Lab 1

### 9. Minimax hoạt động thế nào?

**Nói ngắn:** Minimax giả sử hai phía hợp lý và đối kháng. MAX chọn child có utility lớn nhất cho mình, MIN chọn child nhỏ nhất cho MAX. Backup giá trị từ lá lên gốc rồi chọn action tốt nhất ở gốc. Nó đảm bảo quyết định tốt nhất dưới giả định đối thủ cũng chơi tốt nhất, không phải dự báo đối thủ ngẫu nhiên.

**Trong Lab 1:** Ghost maximize điểm an toàn; Pacman minimize điểm đó. Khi Manhattan distance nhỏ hơn `CAPTURE_DIST=2`, code trả utility rất âm. Ở depth 0, code gọi `_evaluate()` với khoảng cách, degree của ô và phạt ngõ cụt/quay lại.

### 10. Alpha-beta có đổi đáp án minimax không?

**Nói ngắn:** Không. Alpha-beta chỉ bỏ những nhánh chắc chắn không thể ảnh hưởng kết quả tại root. `alpha` là giá trị tốt nhất MAX đã chắc có; `beta` là giá trị tốt nhất MIN đã chắc có. Khi `alpha >= beta`, phần còn lại của node không thể đổi lựa chọn của tổ tiên nên được cắt.

**Trong code:** `_minimax()` trong `labs/lab1/final/agent.py` cập nhật alpha ở lượt Ghost/MAX, beta ở lượt Pacman/MIN và `break` tại cutoff. Lợi ích là có thể xét sâu hơn trong 1 giây, không phải để làm Ghost "thông minh hơn" về mặt utility.

### 11. Tại sao iterative deepening + time budget quan trọng?

**Nói ngắn:** Bài lab giới hạn 1 giây mỗi bước. Iterative deepening chạy depth 1, 2, 3...; chỉ thay `best_move` sau khi hoàn thành trọn một depth. Nếu hết thời gian ở depth sâu hơn, agent vẫn có đáp án hợp lệ từ depth hoàn chỉnh gần nhất. `TIME_BUDGET=0.65` chừa biên cho máy chấm.

**Bị hỏi thêm:** `MAX_DEPTH=10` là chặn an toàn, không phải lời hứa lúc nào cũng tìm tới 10. `try/except` và `_greedy_fallback()` giúp lỗi search không biến thành crash cả trận.

### 12. Vì sao evaluation của Ghost dùng Manhattan trong minimax dù BFS chính xác hơn?

**Nói ngắn:** BFS khoảng cách thật tốt nếu tính từ đúng vị trí đang xét. Bản nháp dùng một bảng BFS tính ở vị trí Pacman thật đầu lượt rồi tái sử dụng ở các node mô phỏng, nên sai khi Pacman mô phỏng đã di chuyển. Manhattan tại node tuy bỏ qua tường nhưng luôn tính giữa đúng hai vị trí giả lập hiện tại. Đó là đánh đổi ưu tiên tính nhất quán của state mô phỏng.

**Bằng chứng cần nhắc đúng mức:** `labs/lab1/final/explain.md` và `plan.md` ghi lại bug này cùng benchmark nội bộ; đó là ghi nhận thử nghiệm của nhóm, không phải một định lý rằng Manhattan luôn tốt hơn BFS.

### 13. Agent Lab 1 khác bản initial ở đâu?

**Nói ngắn:** Pacman giữ A* vì đường đuổi đã hiệu quả; thay đổi lớn là Ghost từ greedy một bước sang minimax + alpha-beta + iterative deepening, có time budget và fallback. Greedy cũ vẫn giữ làm phương án an toàn: ưu tiên xa Pacman theo BFS distance và có mobility tốt.

**Bằng chứng:** xem bảng so sánh trong `labs/lab1/final/explain.md`; code nộp là `labs/lab1/final/agent.py`.

### 14. Luật Lab 1 nào dễ bị hỏi?

**Trả lời:** Pacman đi tối đa hai ô cùng hướng trong một lượt; Ghost đi một ô; hai bên di chuyển đồng thời; bắt khi Manhattan distance `< 2`; Ghost thắng khi sống 200 bước. Có giới hạn 1 giây/bước và 128 MB. Khi hòa win-rate, completion steps là tie-break theo QA. Vì mỗi cặp chấm một lần với start cố định, robustness quan trọng hơn tối ưu dựa trên một seed may mắn.

**Nguồn:** `labs/lab1/HideSeek-2526-3.pdf`, `labs/lab1/final/overview.md`, hai workbook QA.

## 4. Partial observability và Lab 2

### 15. Belief state là gì?

**Nói ngắn:** Khi không quan sát được state thật, agent duy trì phân phối xác suất trên các state có thể xảy ra. Belief state thay thế cho việc đoán một điểm duy nhất quá sớm. Mỗi vòng cập nhật gồm predict theo transition model rồi update theo observation.

### 16. `EnemyTracker` cập nhật belief ra sao?

**Nói ngắn:** Nếu thấy đối phương, phân phối collapse: xác suất 1 tại ô đó. Nếu mất dấu, predict khuếch tán xác suất qua những ô đi được mà đối phương có thể tới, rồi update loại các ô hiện đang thấy vì biết đối phương không ở đó. Sau đó chuẩn hóa để tổng bằng 1. Nếu mass về 0 do mâu thuẫn/biên, reset đều trên ô unseen hợp lệ.

**Trong code:** `labs/lab2/init/belief.py`. Các test kiểm tra distribution không NaN, không âm, tường có mass 0, tổng xấp xỉ 1 và các tình huống thấy/mất dấu/reset.

### 17. Khi Ghost mất dấu Pacman, vì sao `enemy_speed=2`?

**Nói ngắn:** Transition model phải phản ánh luật thật. Pacman có thể đi hai ô thẳng hàng mỗi lượt; nếu Ghost chỉ khuếch tán belief một ô, Ghost đánh giá vùng nguy hiểm nhỏ hơn thực tế. Vì vậy `GhostAgent` tạo tracker với `enemy_speed=ASSUMED_PACMAN_SPEED`.

### 18. Pacman chọn target thế nào khi không thấy Ghost?

**Nói ngắn:** Không chỉ lao đến argmax của belief. Code chấm từng ô theo lượng probability mass mà Pacman có thể quan sát từ đó, chia nhẹ theo chi phí đi tới. Ý nghĩa là chọn nơi giúp thu thông tin hiệu quả trên mỗi bước, rồi dùng A* tới đó. Nếu chưa có target, agent đi nước hợp lệ fallback.

**Nguồn code:** `best_scouting_target()`, `visible_mass()` trong `labs/lab2/init/agent.py`.

### 19. Các kiểm thử Lab 2 chứng minh gì và không chứng minh gì?

**Trả lời:** `test_belief.py` kiểm tra invariants và hành vi module `EnemyTracker`, gồm thấy địch chính xác, belief lan khi mất dấu, reset khi tổng xác suất bằng 0, input lỗi không văng exception và benchmark update dưới ngưỡng nội bộ. Nó không tự chứng minh agent thắng benchmark framework hay tối ưu chiến lược toàn cục; điều đó phải chạy Arena riêng.

## 5. CSP, logic và học máy

### 20. CSP gồm những thành phần nào? Backtracking dùng sao?

**Nói ngắn:** CSP có variables, domains và constraints. Backtracking gán biến từng bước; khi partial assignment vi phạm constraint thì quay lui. MRV chọn biến còn ít giá trị hợp lệ nhất, degree heuristic ưu tiên biến ràng buộc nhiều biến khác, LCV thử giá trị loại ít lựa chọn của hàng xóm nhất. Forward checking xóa sớm giá trị bất khả thi; AC-3 mạnh hơn vì duy trì arc consistency.

### 21. Entailment khác equivalence thế nào?

**Nói ngắn:** `KB ⊨ α` nghĩa là mọi model làm KB đúng cũng làm α đúng. Equivalence `α ≡ β` nghĩa hai công thức có cùng giá trị chân lý ở mọi model. Một công thức có thể được KB entail mà không tương đương với toàn bộ KB.

### 22. Quy trình resolution mệnh đề?

**Nói ngắn:** Muốn chứng minh `KB ⊨ q`, thêm `¬q` vào KB, khử `↔` và `→`, đẩy phủ định vào literal, chuyển CNF, tách clauses và resolve literal đối ngẫu. Sinh được empty clause thì mâu thuẫn, suy ra q được entail. Phải ghi hai clause cha, không chỉ nhảy tới kết quả.

### 23. Những bước FOL sang CNF?

**Nói ngắn:** Khử equivalence, implication; đưa phủ định vào trong; standardize variables apart; Skolemize existential quantifiers; bỏ universal quantifiers; phân phối `∨` qua `∧` rồi tách clauses. Skolem function phải phụ thuộc đúng các universal variables đang bao ngoài nó.

### 24. ID3 chọn thuộc tính như thế nào?

**Nói ngắn:** Tính entropy của nhãn ở tập hiện tại, tính average entropy sau khi split theo từng thuộc tính, rồi information gain `IG(A,S)=H(S)-AE(A)`. Chọn thuộc tính IG lớn nhất, lặp trên từng nhánh. Dừng khi nhánh thuần, không còn thuộc tính, hoặc không còn mẫu.

$$
H(S)=-\sum_i p_i\log_2 p_i
$$

**Đề cũ:** 2021-2022 dùng Gain Ratio, nên ngoài IG còn có `SplitInfo`; từ kết quả đã giải, `GainRatio(Education)=0.1965` nên root là `Education`. 2023-2024 dùng 10 mẫu training, `IG(Weather)=0.6955` nên root là `Weather`.

### 25. Gain Ratio khắc phục gì?

**Nói ngắn:** Information gain thiên vị thuộc tính có nhiều giá trị, vì chúng dễ tạo nhánh nhỏ/thuần. Gain Ratio chia IG cho SplitInfo để phạt split phân mảnh quá mạnh. Nó không có nghĩa luôn chọn thuộc tính có nhiều nhánh ít hơn; vẫn phải so giá trị hợp lệ và hiểu ngữ cảnh đề.

### 26. Naive Bayes tính class cho mẫu mới ra sao?

**Nói ngắn:** Với giả định các feature độc lập có điều kiện theo class:

$$
P(C\mid X)\propto P(C)\prod_k P(x_k\mid C)
$$

Tính prior từ toàn bộ training set, likelihood theo từng class rồi so score. Không cần tính `P(X)` khi chỉ chọn class vì mẫu số giống nhau. Laplace smoothing chỉ cần khi zero frequency làm một score bị triệt tiêu.

### 27. Perceptron, MLP và backpropagation?

**Nói ngắn:** Perceptron là bộ phân lớp tuyến tính, chỉ tách được dữ liệu linearly separable. MLP thêm hidden layers và activation phi tuyến để học ranh giới phức tạp. Backprop dùng chain rule tính gradient loss theo từng weight từ output lùi về input, sau đó optimizer cập nhật weight theo hướng giảm loss. Nó không "tự tìm công thức" mà dùng đạo hàm của computational graph.

## 6. DUSt3R - phần đồ án

### 28. DUSt3R giải bài toán gì?

**Nói ngắn:** DUSt3R nhận hai ảnh, không cần intrinsic hay camera pose làm input, và hồi quy geometry 3D dày đặc theo cặp. Ý chính không phải camera biến mất, mà đổi camera từ điều kiện phải biết trước thành đại lượng có thể suy ra sau từ biểu diễn 3D.

**Một câu kể chuyện:** Classical pipeline là `camera + matches -> triangulation -> 3D`; DUSt3R là `images -> pointmaps -> 3D -> depth/matches/camera`.

### 29. Pointmap khác depth map thế nào?

**Nói ngắn:** Depth map cho một scalar khoảng cách theo ray ở mỗi pixel. Pointmap cho vector tọa độ 3D tại mỗi pixel, dạng `W x H x 3`. Nếu biết intrinsic và depth thì back-project được pointmap; nhưng pointmap đã mang trực tiếp hình học 3D nên tiện so sánh, matching và alignment trong không gian 3D.

### 30. Vì sao hai output pointmap đặt trong cùng frame ảnh 1?

**Nói ngắn:** Với cặp ảnh, network xuất `X_1,1` và `X_2,1`; cả hai được biểu diễn trong coordinate frame của ảnh 1. Nhờ vậy điểm từ hai view có thể so trực tiếp, nearest-neighbor matching và pairwise alignment không phải đổi qua lại giữa hai hệ tọa độ riêng.

### 31. Architecture của DUSt3R?

**Nói ngắn:** Hai ảnh vào ViT encoder Siamese dùng chung weights. Sau đó hai decoder trao đổi token qua cross-attention lặp lại, rồi regression heads tạo pointmap và confidence map. Cross-attention giúp hai view ảnh hưởng lẫn nhau để output aligned. Global alignment N-view là hậu xử lý tối ưu riêng, không phải một layer decoder.

### 32. Confidence có phải xác suất calibrated không?

**Nói ngắn:** Không nên gọi là xác suất đúng. Confidence là trọng số dương được học trong loss: vùng khó hoặc mơ hồ có thể bị giảm trọng số. Nó không có nhãn confidence trực tiếp, nên ý nghĩa chính là weighting cho regression/later optimization, không phải một xác suất đã calibration.

### 33. Vì sao phải normalize scale trong loss?

**Nói ngắn:** Hình học từ ảnh có scale ambiguity. Loss chuẩn hóa predicted và ground-truth pointmap theo khoảng cách trung bình tới origin trước khi đo sai khác, để không phạt chỉ vì lệch một scale toàn cục. Điều này không làm scale metric tự xuất hiện.

### 34. Global alignment khác bundle adjustment (BA) thế nào?

**Nói ngắn:** BA cổ điển thường tối ưu reprojection error 2D của camera và landmarks. DUSt3R global alignment mặc định tối ưu residual giữa pointmaps trong 3D trên graph các pair, cùng rigid transforms và scale pairwise. Nó vẫn cần graph đủ liên thông theo nội dung thị giác, không phải phép ghép ảnh vô điều kiện.

### 35. Từ pointmap suy ra các task khác ra sao?

**Nói ngắn:** Monocular depth lấy `z` của pointmap khi chạy cùng một ảnh hai lần. Matching dùng mutual nearest neighbors trong không gian 3D. Relative pose có thể fit bằng weighted Procrustes hoặc qua matches với essential/PnP-RANSAC. Các route đó là bước downstream, không phải mạng xuất pose trực tiếp.

### 36. Trade-off phải nói trung thực của DUSt3R?

**Trả lời:** Điểm mạnh là plug-and-play: không cần calibration/pose đầu vào và một pointmap phục vụ nhiều task. Đổi lại pointmap không bị ép hoàn toàn theo camera model vật lý tại inference; scale/evaluation có thể cần alignment; global alignment là tối ưu số; và trên DTU, specialist dùng GT camera/train chuyên domain chính xác hơn. Không được gọi mọi kết quả là zero-shot tuyệt đối.

### 37. Video/Manim trong repo thực sự cài những gì?

**Trả lời:** `project/A-Star-DUSt3R/render.py` ghép bảy chapter theo thứ tự: intro, classical geometry, pointmap, pairwise common frame, network, global alignment, takeaways. `src/scenes/visuals.py` tạo geometry vector như pixel grid, point cloud, camera và token grid, tránh phụ thuộc screenshot paper. `tests/test_foundation_scenes.py` là contract cho import scene, visual metaphor, không dùng `MathTex`, dry-run Network scene và discovery entry point.

**Lưu ý khi bảo vệ:** Đừng nói video đã render/đạt chất lượng cuối chỉ vì source tồn tại. Nếu chưa chạy fresh render thì nói chính xác: source, test contract và checklist đã có; render cuối cần được xác nhận riêng.

## 7. Câu hỏi chéo và cách giữ câu trả lời đáng tin

### 38. “Mã này có phải em hiểu không? Hãy trace một lượt.”

**Lab 1:** `PacmanAgent.step()` nhận map và vị trí -> A* đến Ghost -> `follow_path()` trả một hướng và 1-2 bước. `GhostAgent.step()` chuẩn bị map degree -> search iterative deepening trước deadline -> `_minimax()` mô phỏng Ghost/Pacman -> fallback greedy nếu cần -> trả `Move`.

**Lab 2:** Trước khi chọn action gọi `tracker.update()`. Nếu thấy địch thì chase/evade trực tiếp; nếu không thì dùng belief: Pacman tới vị trí thu được nhiều information mass, Ghost dùng target belief cho nhánh an toàn rồi duy trì minimax.

### 39. “Nếu giả định của em sai thì sao?”

**Trả lời tốt:** Nêu giả định cụ thể, hậu quả và guard. Ví dụ minimax giả sử Pacman chọn nước hại Ghost nhất; nếu thực tế đối thủ không tối ưu, chiến lược vẫn an toàn theo worst case nhưng có thể bảo thủ. Với Blind Arena, giả định tường luôn thấy đã được đối chiếu source framework và QA; code vẫn không dùng vị trí địch khi `enemy_position is None`.

### 40. “Kết quả nào đã được kiểm tra?”

**Trả lời tốt:** Chỉ trích đúng artifact. Lab 1 có `labs/lab1/final/test_results/`, `results_final_vs_initial.csv`, log tournament và unit tests; Lab 2 có `test_belief.py`; DUSt3R có contract tests. Nếu không chạy lại trong buổi hiện tại, gọi chúng là **kết quả/lưu vết test đã lưu**, không nói "vừa chạy pass".

## 8. Checklist trước buổi vấn đáp

- [ ] Đọc `finalexam/ON-FINAL-THEO-SLIDE.md`, rồi tự làm lại một bài ID3, một PL/FOL resolution và một cây alpha-beta.
- [ ] Mở `labs/lab1/final/agent.py`, tự trace một lượt Pacman và một lượt Ghost không nhìn ghi chú.
- [ ] Mở `labs/lab2/init/belief.py`, giải thích predict/update/reset và vì sao `-1` vẫn walkable theo framework.
- [ ] Đọc `project/A-Star-DUSt3R/docs/research.md`, đặc biệt sections 2-6 và 9-10; không học thuộc benchmark thiếu dataset/metric/caveat.
- [ ] Khi bị hỏi số liệu, mở đúng file nguồn trước khi trả lời. Khi bị hỏi kết quả mới, chạy test/benchmark tương ứng thay vì dựa vào ghi chú cũ.

## Bản đồ nguồn nhanh

| Cần ôn | Mở trước |
|---|---|
| Final theo slide | `finalexam/ON-FINAL-THEO-SLIDE.md` |
| Lời giải đề ba năm | `finalexam/20212022/LOI-GIAI.md`, `20222023/LOI-GIAI.md`, `20232024/LOI-GIAI.md` |
| Lab 1 - chiến lược và bằng chứng | `labs/lab1/final/overview.md`, `explain.md`, `plan.md`, `agent.py` |
| Lab 2 - fog và belief | `labs/lab2/README.md`, `init/agent.py`, `init/belief.py`, `init/test_belief.py` |
| DUSt3R - nội dung khoa học | `project/A-Star-DUSt3R/docs/research.md` và paper CVPR 2024 trong `references/` |
| DUSt3R - phần nhóm cài | `project/A-Star-DUSt3R/render.py`, `src/scenes/`, `tests/test_foundation_scenes.py` |
