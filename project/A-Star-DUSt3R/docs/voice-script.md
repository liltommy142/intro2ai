# Voice script — DUSt3R

> Thời lượng mục tiêu: khoảng 9:20. Giọng kể gần gũi, đi từ trực giác đến cơ chế; không đọc nguyên công thức hay bảng.

## 1. 0:00–0:50 — Hook: một ảnh, quá nhiều thế giới 3D

[ON SCREEN] Một bức ảnh căn phòng. Hai đường ray camera đi qua cùng pixel rồi tách ra thành nhiều điểm 3D khả dĩ.

“Nhìn vào một pixel trên ảnh này, ta biết nó có màu gì. Nhưng ta không biết chắc nó cách camera bao xa. Cùng một ảnh 2D có thể đến từ rất nhiều thế giới 3D khác nhau: một chiếc cốc nhỏ ở gần, hay một vật lớn ở xa, đều có thể chiếm gần như cùng số pixel.

Nếu có thêm một ảnh nữa, trực giác nói rằng ta có thể đối chiếu hai góc nhìn để dựng lại không gian. Nhưng từ trước đến nay, cách làm đó thường bắt đầu bằng một yêu cầu khá nặng: hãy cho máy biết camera đang ở đâu và nhìn bằng ống kính nào.

DUSt3R không làm camera biến mất. Nó đổi vai trò của camera: từ điều kiện phải có trước khi dựng hình, thành một đại lượng có thể suy ra sau khi đã dự đoán hình học.”

[ON SCREEN] “Camera: prerequisite → recoverable quantity”

## 2. 0:50–2:00 — Hình học cổ điển: đúng, nhưng nhiều mắt xích

[ON SCREEN] Keypoints → matching → robust estimation → SfM/BA → dense MVS → reconstruction.

“Trong multi-view stereo cổ điển, máy tìm những điểm giống nhau giữa các ảnh. Khi biết intrinsic, pose và correspondence đủ đáng tin, nó mới triangulate các tia nhìn để tìm điểm 3D.

Pipeline đó thường đi qua phát hiện và matching keypoint, robust estimation, Structure-from-Motion, bundle adjustment, rồi mới dense MVS. Đây không phải những bước vô ích; rất nhiều hệ thống mạnh vẫn dựa vào chúng.

Khó ở chỗ: mỗi bước phụ thuộc bước trước. Nếu matching sai một vùng ít texture, hoặc pose lệch một chút, dense reconstruction phải gánh sai số đó. Và trong cảnh thật, camera calibration đôi khi không có sẵn, còn SfM có thể khó khi ít góc nhìn, chuyển động camera không phù hợp, hoặc bề mặt phản xạ.

Vì thế, câu hỏi của DUSt3R là: thay vì liên tục truyền kết quả trung gian từ module này sang module khác, liệu ta có thể dự đoán một biểu diễn 3D chung ngay từ cặp ảnh không?”

[ON SCREEN] Các mũi tên lỗi lan dọc pipeline; sau đó hiện “Predict a shared 3D representation”.

## 3. 2:00–3:25 — Pointmap: đổi một pixel thành một điểm 3D

[ON SCREEN] Ảnh RGB; từng pixel lần lượt hiện nhãn (x, y, z). So sánh: depth map = một số, pointmap = ba số.

“Câu trả lời là pointmap. Hãy tưởng tượng một tấm ảnh đặc biệt: thay vì lưu màu đỏ, xanh, lam, mỗi pixel lưu toạ độ x, y, z của điểm cảnh mà pixel đó nhìn thấy.

Đó là pointmap: một trường 2D dày đặc các điểm 3D. Depth map chỉ cho ta một con số, là độ sâu theo ray camera. Pointmap cho cả một vector 3D, nên nó gắn pixel với vị trí trong không gian rõ ràng hơn.

Với hai ảnh, DUSt3R không chỉ đo depth cho từng ảnh. Nó dự đoán hai pointmap, kèm hai confidence map. Điều quan trọng là các pointmap được dự đoán chỉ đúng đến một scale chưa biết: hình dạng và quan hệ tương đối có thể đúng, nhưng toàn bộ scene có thể phóng to hoặc thu nhỏ.

Trong lúc train, paper chuẩn hoá scale trước khi so sai số 3D. Vì vậy, đừng nói output luôn có metric scale tuyệt đối.”

[ON SCREEN] Hai point cloud cùng hình, một lớn/một nhỏ → “same shape, unknown scale”.

## 4. 3:25–4:50 — Common frame: bí quyết làm hai ảnh “nói cùng ngôn ngữ”

[ON SCREEN] I₁ và I₂ đi vào; xuất hiện X¹,¹, C¹,¹ và X²,¹, C²,¹. Cả hai cloud đặt trên hệ trục “frame of I₁”.

“Đây là chi tiết đáng nhớ nhất. Nếu input là I một và I hai, DUSt3R xuất X mũ một, một và X mũ hai, một — cùng confidence tương ứng. Dấu một ở vị trí thứ hai nói rằng cả hai pointmap đều được biểu diễn trong hệ toạ độ của ảnh I một.

Nói cách khác, cloud nhìn từ ảnh hai không ở một hệ trục riêng xa lạ. Nó đã được diễn tả trong ngôn ngữ không gian của ảnh một. Khi đó, ta có thể đặt hai cloud lên nhau, tìm điểm gần nhau trong 3D, hoặc so hình học giữa hai view mà không cần bắt đầu bằng pose camera đầu vào.

Confidence map giúp ta biết vùng nào model tin hơn, nhưng hãy cẩn thận: nó không phải xác suất đã được calibrated. Nó là trọng số được học trong loss; vùng trời, vật trong suốt hay vùng chỉ thấy ở một view có thể có confidence thấp.

Vậy pointmap không chỉ là ‘depth nhiều kênh’. Nó là chiếc cầu nối pixel, shape và quan hệ giữa hai góc nhìn.”

[ON SCREEN] Hai cloud snap vào nhau; vùng sky/translucent mờ dần, nhãn “learned confidence, not probability”.

## 5. 4:50–6:10 — Network: hai mắt, một cuộc hội thoại

[ON SCREEN] Hai encoder song song nối bằng “shared weights”; hai decoder có mũi tên cross-attention hai chiều; hai head xuất X và C.

“Bên trong network cũng phản ánh ý tưởng hai view phải hợp tác. Hai ảnh đi vào hai ViT encoder Siamese có chung trọng số. Nhờ vậy, cả hai ảnh được đọc bằng cùng một bộ quy tắc thị giác.

Nhưng encoder chung chưa đủ. Sau đó là hai Transformer decoder. Trong mỗi block, token trước hết nhìn các token trong chính view của mình; rồi nó cross-attend sang token của view còn lại; sau đó mới đi qua MLP. Cuộc trao đổi này lặp lại qua các block.

Hãy xem như hai người quan sát cùng một căn phòng từ hai cửa sổ. Mỗi người tự nhìn cửa sổ của mình, rồi liên tục hỏi người kia: ‘chi tiết này ở phía bạn trông ra sao?’ Chính cross-attention làm cho hai output có cơ hội trở thành hai pointmap đã aligned.

Cuối cùng, mỗi nhánh regression head xuất một pointmap và một confidence map. Đây vẫn là network cho một cặp ảnh; đừng vẽ global alignment như thể nó là một layer thứ ba trong head.”

[ON SCREEN] “Pairwise network output” hiện sau hai head; một đường nét đứt dẫn sang phần N-view.

## 6. 6:10–7:45 — Global alignment: từ nhiều cặp đến một scene

[ON SCREEN] N ảnh thành graph; mỗi edge có một cặp pointmap. Các cloud lệch nhau rồi hội tụ thành χ.

“Khi có nhiều hơn hai ảnh, DUSt3R làm thêm một bước hậu xử lý: global alignment. Trước hết, ta tạo một graph: ảnh là node, còn những cặp có content thị giác liên quan là edge. Với mỗi edge, network đã cho ta hai pointmap pairwise.

Tối ưu mặc định sau đó tìm ba loại biến: pointmap toàn cục ký hiệu chi, rigid transform cho từng cặp P e, và scale cho từng cặp sigma e. Mục tiêu là làm pointmap từ mọi pair nhất quán trong cùng không gian 3D, với confidence cao được tin nhiều hơn.

Điều nó tối ưu là sai số 3D giữa cloud toàn cục và cloud pairwise đã transform, không phải reprojection error 2D kiểu bundle adjustment. Ràng buộc các scale giúp tránh nghiệm co mọi cloud về không.

Đây là điểm cần nói thật chính xác: global alignment mặc định không trực tiếp tối ưu pose camera riêng cho từng ảnh. Nếu ta chọn biến thể có mô hình pinhole, ta mới có thể suy ra pose, intrinsic và depth. Và nếu graph ảnh bị rời vì không có liên hệ thị giác đủ để nối các phần, không có phép màu nào tự ghép mọi ảnh lại.”

[ON SCREEN] “Default: χ, Pₑ, σₑ” → “Optional pinhole: K, P, D”; bên cạnh hiện “3D residual ≠ 2D reprojection”.

## 7. 7:45–9:20 — Downstream, kết quả và kết luận

[ON SCREEN] Pointmap → depth / matches / focal / relative pose / reconstruction.

“Từ pointmap, nhiều tác vụ quen thuộc trở nên là các phép đọc ra. Với monocular depth, paper đưa cùng một ảnh vào hai nhánh; depth là toạ độ z của pointmap. Với matching, ta tìm nearest neighbor trong không gian 3D rồi chỉ giữ các match hai chiều cùng chọn nhau.

Focal và pose cũng có thể được suy ra, nhưng không nên gọi đó là output trực tiếp của network. Ví dụ, cách fit focal trong paper giả sử principal point gần tâm ảnh và pixel vuông; Procrustes cho pose tương đối thì nhạy với outlier, nên có thể cần PnP-RANSAC hoặc epipolar geometry.

Kết quả cho thấy biểu diễn này thực sự hữu ích. Trên NYUD-v2, DUSt3R512 báo Rel 6.50 và delta một phẩy hai lăm là 94.09. Trên CO3Dv2 với global alignment, RRA@15 là 96.2, RTA@15 là 86.8 và mAA@30 là 76.7. Nhưng đừng nói global alignment thắng mọi metric: route PnP lần lượt là 94.3, 88.4 và 77.2, tức mAA cao hơn.

Ở ETH3D trong setting không có GT camera/pose/depth range nhưng có alignment, Rel là 2.91 và InlierRatio là 76.91; evaluation dùng median alignment vì scale chưa xác định. Còn DTU zero-shot đạt accuracy 2.677 mm, completeness 0.805 mm, overall 1.741 mm — sau khi prediction được align vào hệ toạ độ ground truth để đánh giá. Các specialist có GT camera và train riêng DTU vẫn chính xác hơn nhiều.

Vậy thông điệp cuối cùng không phải ‘camera không còn quan trọng’. DUSt3R cho ta một cách khác để bắt đầu: dự đoán pointmap chung trước, rồi từ đó suy ra depth, match, camera hoặc reconstruction khi cần. Camera đã đổi từ prerequisite thành quantity có thể recover — và chính sự đổi vai trò đó làm nhiều bài toán hình học trở nên trực tiếp hơn.”

[ON SCREEN] “Pointmaps first → geometry downstream”; sau đó “Camera: prerequisite → recoverable quantity”.

## Bảng kiểm claim cho người thu âm

| Claim | Cách nói được phép | Không nói quá | Căn cứ paper |
|---|---|---|---|
| Camera | “Không cần cung cấp trước calibration/pose.” | “Không cần camera” hoặc “camera biến mất”. | Intro; Secs. 3.3–3.4, pp.1–6 |
| Pair output | “X¹,¹ và X²,¹ cùng frame I₁, kèm confidence.” | “Hai depth map độc lập.” | Sec. 3.1, Fig. 2, p.4 |
| Confidence | “Trọng số/độ tin cậy được học.” | “Xác suất calibrated.” | Sec. 3.2, Eq. (4), p.4 |
| N-view | “Hậu xử lý 3D tối ưu χ, Pₑ, σₑ.” | “Một layer mạng trực tiếp xuất toàn bộ scene/camera.” | Sec. 3.4, Eq. (5), pp.5–6 |
| CO3Dv2 | “GA: 96.2 / 86.8 / 76.7; PnP mAA 77.2.” | “GA thắng mọi metric.” | Table 2, p.8 |
| DTU | “1.741 mm overall sau GT-coordinate evaluation alignment.” | “Tự xuất metric mm tuyệt đối” hoặc “hơn specialist.” | Sec. 4.5, Table 3, p.8 |
