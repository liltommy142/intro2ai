Được. Tao nghĩ bước này **nên chốt lời thoại trước**, còn animation Manim chỉ là lớp minh họa bám theo lời thoại. Nếu làm ngược lại rất dễ thành một video đẹp nhưng kể chuyện rời rạc.

Dưới đây tao viết **bản kịch bản V1**, nhắm khoảng **24–27 phút**, theo kiểu intuition-first, problem-driven, có “aha moment” rõ ràng. Tao cố tình chưa sa đà vào benchmark và bảng số liệu, vì dưới 30 phút thì **ý tưởng của paper quan trọng hơn việc đọc từng con số**.

---

# KỊCH BẢN VIDEO DUSt3R — V1

## 0:00–1:20 — Cold open: “Hai bức ảnh có đủ để hiểu một thế giới 3D không?”

**Lời thoại**

> Đây là hai bức ảnh của cùng một căn phòng.
>
> Chúng chỉ là những lưới pixel hai chiều.
>
> Không có thông tin nào ở đây nói trực tiếp rằng cái ghế cách camera bao nhiêu mét, bức tường nằm ở đâu trong không gian, hay camera thứ hai đã di chuyển như thế nào so với camera thứ nhất.
>
> Vậy mà chỉ cần nhìn vào hai bức ảnh này, chúng ta gần như lập tức có cảm giác về chiều sâu.
>
> Chúng ta biết vật nào ở gần hơn.
>
> Vật nào ở xa hơn.
>
> Và thậm chí có thể hình dung đại khái căn phòng trông như thế nào nếu nhìn từ một góc khác.
>
> Nhưng một máy tính sẽ làm điều đó như thế nào?
>
> Hay nói chính xác hơn:
>
> **Làm thế nào để biến một tập hợp những bức ảnh 2D thành một thế giới 3D?**

**Visual idea**

```text
2 ảnh xuất hiện
→ camera zoom vào từng pixel
→ ảnh trở thành grid phẳng
→ camera xoay, cho thấy nó hoàn toàn 2D
→ một căn phòng 3D mờ xuất hiện phía sau
```

---

# 1:20–3:00 — Một pixel đã đánh mất thứ gì?

**Lời thoại**

> Để thấy vấn đề, hãy chỉ nhìn vào một pixel.
>
> Pixel này có vị trí trên ảnh.
>
> Nó có màu.
>
> Nhưng có một thông tin cực kỳ quan trọng mà phép chiếu camera đã làm mất:
>
> **độ sâu**.
>
> Từ một pixel duy nhất, điểm ngoài đời có thể nằm ở đây...
>
> hoặc ở đây...
>
> hoặc ở bất kỳ đâu trên cùng một tia đi ra từ camera.
>
> Đây là lý do một bức ảnh đơn lẻ không cho chúng ta một nghiệm 3D duy nhất.
>
> Một hình ảnh 2D là kết quả của việc ép cả thế giới ba chiều lên một mặt phẳng.
>
> Và bài toán reconstruction là cố gắng đảo ngược quá trình đó.

**Visual**

```text
Camera ●
        \
         \
          ●
           ●
            ●

nhiều điểm khác nhau
→ cùng project về một pixel
```

---

# 3:00–4:30 — Stereo: tại sao hai góc nhìn giúp được?

**Lời thoại**

> Nhưng bây giờ hãy thêm một camera thứ hai.
>
> Cùng một điểm trong thế giới xuất hiện ở hai vị trí khác nhau trên hai ảnh.
>
> Nếu biết hai camera nằm ở đâu và hướng về đâu, chúng ta có thể dựng một tia từ mỗi camera.
>
> Và nơi hai tia gặp nhau cho ta vị trí của điểm đó trong không gian.
>
> Đây là ý tưởng cơ bản của **triangulation**.
>
> Và cũng là lý do stereo vision mạnh hơn rất nhiều so với chỉ nhìn một ảnh.

**Visual**

```text
C1 ●  \        /  ● C2
       \      /
        \    /
         \  /
          ● P
```

Rồi highlight:

```text
pixel1 ↔ pixel2
+
camera geometry
=
3D point
```

---

# 4:30–7:00 — Cách truyền thống: một cỗ máy nhiều tầng

**Lời thoại**

> Nghe có vẻ đơn giản.
>
> Nhưng có một vấn đề.
>
> Để triangulate, trước tiên chúng ta cần biết điểm nào trong ảnh thứ nhất tương ứng với điểm nào trong ảnh thứ hai.
>
> Và để biến những correspondence đó thành geometry chính xác, chúng ta cần hiểu mối quan hệ giữa hai camera.
>
> Và với nhiều ảnh, mọi thứ trở thành một chuỗi khá dài.
>
> Ta tìm keypoints.
>
> Match chúng giữa các ảnh.
>
> Ước lượng quan hệ hình học.
>
> Tìm camera poses.
>
> Triangulate các điểm.
>
> Tạo sparse reconstruction.
>
> Rồi cuối cùng mới tiến tới dense reconstruction.
>
> Các hệ thống Structure-from-Motion và Multi-View Stereo hiện đại rất mạnh.
>
> Nhưng DUSt3R bắt đầu từ một quan sát khá đơn giản:
>
> **đây là một pipeline tuần tự, và lỗi ở một bước có thể truyền sang những bước phía sau.**

Paper cũng nhấn mạnh chính vấn đề này: SfM/MVS hiện đại giải lần lượt matching, essential matrix, triangulation, sparse reconstruction, camera estimation rồi dense reconstruction; mỗi subproblem không hoàn hảo có thể thêm noise cho bước tiếp theo. 

**Visual**

```text
Images
 ↓
Keypoints
 ↓
Matching
 ↓
Camera geometry
 ↓
Triangulation
 ↓
Sparse 3D
 ↓
Dense 3D
```

Sau đó một error nhỏ màu đỏ xuất hiện ở Matching, rồi lan xuống dưới.

---

# 7:00–8:10 — Câu hỏi thay đổi toàn bộ góc nhìn

**Lời thoại**

> Và đây là nơi DUSt3R thay đổi câu hỏi.
>
> Thay vì hỏi:
>
> **“Camera nằm ở đâu để từ đó ta có thể dựng lại 3D?”**
>
> hãy thử hỏi:
>
> **“Nếu ta dự đoán 3D trực tiếp trước thì sao?”**
>
> Không phải depth.
>
> Không phải camera pose.
>
> Không phải correspondence.
>
> Mà trực tiếp:
>
> **mỗi pixel này nằm ở đâu trong không gian 3D?**

Pause.

> Đây chính là ý tưởng trung tâm của DUSt3R.

---

# 8:10–11:00 — Pointmap: representation quan trọng nhất

**Lời thoại**

> DUSt3R sử dụng một representation gọi là **pointmap**.
>
> Một ảnh bình thường có kích thước \(W \times H\).
>
> Với mỗi pixel, ta lưu ba giá trị màu: đỏ, xanh lá và xanh dương.
>
> Một pointmap cũng có cùng lưới \(W \times H\).
>
> Nhưng thay vì mỗi pixel chứa RGB, nó chứa một tọa độ ba chiều:
>
> \(X, Y, Z\).
>
> Nói cách khác:
>
> pixel này...
>
> tương ứng với điểm này trong không gian.
>
> Pixel bên cạnh...
>
> tương ứng với điểm khác.
>
> Và nếu ta làm điều đó với toàn bộ ảnh...
>
> mặt phẳng pixel bắt đầu bung ra thành một bề mặt 3D.

Paper định nghĩa pointmap chính xác là một trường \(W\times H\times3\), tạo ánh xạ một-một giữa pixel ảnh và điểm 3D. 

**Visual chủ lực**

```text
Image plane
```

Chọn một pixel.

```text
pixel → dot
```

Dot trượt ra theo Z.

Sau đó hàng nghìn pixel cùng “bung” ra.

```text
2D image
→
3D point cloud
```

**Lời thoại tiếp**

> Đây là lúc chúng ta nên nhận ra một điều khá đẹp.
>
> Một depth map chỉ nói mỗi pixel cách camera bao xa.
>
> Một pointmap đi thẳng đến tọa độ 3D.
>
> Nó vẫn giữ được quan hệ với pixel gốc, nhưng đồng thời đã sống trong không gian ba chiều.
>
> Chính vì giữ được cả hai thế giới — image space và 3D space — pointmap trở thành một representation rất giàu thông tin.

---

# 11:00–13:20 — Cú twist lớn hơn: hai pointmap cùng một coordinate frame

**Lời thoại**

> Nhưng DUSt3R còn làm một việc lạ hơn nữa.
>
> Giả sử ta đưa vào hai ảnh.
>
> Từ ảnh thứ nhất, model tạo ra một pointmap.
>
> Không có gì bất ngờ.
>
> Từ ảnh thứ hai, model cũng tạo ra một pointmap.
>
> Nhưng pointmap thứ hai **không được biểu diễn trong coordinate frame của camera thứ hai**.
>
> Nó cũng được biểu diễn trong coordinate frame của camera thứ nhất.

Paper gọi hai output này là \(X^{1,1}\) và \(X^{2,1}\); cả hai đều nằm trong coordinate frame của image 1. 

**Visual**

Ban đầu:

```text
Camera 1 frame           Camera 2 frame

blue cloud                pink cloud
```

Sau đó pink cloud rotate/translate sang frame 1.

**Lời thoại**

> Đây là một quyết định cực kỳ quan trọng.
>
> Bởi vì hai reconstruction giờ đây đã sống trong cùng một hệ tọa độ.
>
> Nghĩa là relationship giữa hai viewpoint không cần được xuất ra dưới dạng một biến “camera pose” riêng biệt.
>
> Nó đã được encode ngầm vào chính geometry.

Pause.

> Camera pose trở thành một thứ mà ta có thể **suy ra sau**, thay vì phải biết trước khi dựng 3D.

---

# 13:20–15:50 — DUSt3R là một neural network như thế nào?

**Lời thoại**

> Vậy ai thực sự dự đoán các pointmap này?
>
> DUSt3R là một deep neural network dựa trên Transformer.
>
> Hai ảnh đầu tiên được chia thành các patch và đi qua một Vision Transformer encoder dùng chung weights.
>
> Ta có thể hình dung hai branch như hai người quan sát cùng một scene.
>
> Mỗi người ban đầu tự phân tích những gì mình nhìn thấy.
>
> Sau đó, trong decoder, hai branch bắt đầu trao đổi thông tin thông qua cross-attention.

Paper mô tả hai ảnh được encode Siamese bằng shared ViT encoder; các decoder liên tục exchange information bằng cross-attention trước khi regression heads xuất pointmaps và confidence maps. 

**Lời thoại**

> Self-attention cho mỗi view hiểu chính nó.
>
> Cross-attention cho mỗi view hỏi:
>
> “Những gì tôi đang nhìn thấy liên quan thế nào đến những gì góc nhìn kia đang nhìn thấy?”
>
> Sau nhiều tầng như vậy, mỗi branch đi đến một prediction 3D.
>
> Và vì hai branch đã liên tục giao tiếp với nhau, hai pointmaps có thể được đặt vào một coordinate frame chung.

**Visual**

```text
I1 → Encoder → F1 → Decoder1 → X11
                       ↕
                 cross attention
                       ↕
I2 → Encoder → F2 → Decoder2 → X21
```

---

# 15:50–17:15 — Nhưng network không được “cài geometry” bằng tay

**Lời thoại**

> Có một chi tiết khiến DUSt3R khác khá nhiều với một số pipeline neural geometry trước đó.
>
> Network không bị ép phải tuân theo một camera model cứng trong lúc pairwise inference.
>
> Nó không có một module nói:
>
> “Đây là epipolar geometry.”
>
> “Đây là triangulation.”
>
> “Đây là pinhole camera.”
>
> Thay vào đó, model học các geometric priors từ training data.

Paper nói architecture không explicitly enforce geometric constraints; pointmaps được học từ training data chứa các pointmap nhất quán về hình học. 

**Lời thoại**

> Điều đó có nghĩa rằng geometry không biến mất.
>
> Nó chỉ chuyển từ một chuỗi luật được lập trình thủ công...
>
> sang một cấu trúc mà model phải học từ dữ liệu.

---

# 17:15–19:00 — Model được dạy bằng một mục tiêu rất đơn giản

**Lời thoại**

> Và cách model được train cũng đáng chú ý.
>
> Nó không có một loss riêng cho depth.
>
> Một loss khác cho camera pose.
>
> Một loss khác cho matching.
>
> Mục tiêu chính rất trực tiếp:
>
> **đặt predicted 3D point càng gần ground-truth 3D point càng tốt.**

Paper mô tả training objective là regression trực tiếp trong 3D space. 

**Visual**

```text
Pred ● ------------ ● GT
        error
```

Predicted dot trượt tới GT.

**Lời thoại**

> Có một vấn đề nhỏ.
>
> Từ ảnh, scale tuyệt đối thường không xác định được hoàn toàn.
>
> Một reconstruction có thể lớn gấp mười lần nhưng vẫn giữ đúng shape tương đối.
>
> Vì vậy DUSt3R normalize cả prediction và ground truth bằng scale trung bình của point cloud trước khi so sánh chúng. 

Visual:

```text
small cloud
big cloud

→ normalize
→ chồng khít
```

---

# 19:00–20:20 — Confidence: model cũng phải học khi nào nên tin chính mình

**Lời thoại**

> Nhưng không phải pixel nào cũng dễ.
>
> Bầu trời không có một surface hữu hạn rõ ràng.
>
> Kính và vật trong suốt phá vỡ giả định đơn giản rằng mỗi camera ray chạm đúng một surface.
>
> Và những vùng chỉ xuất hiện ở một view có thể khó hơn nhiều.
>
> Vì vậy DUSt3R còn dự đoán một confidence cho mỗi pixel. 
>
> Nếu model rất tự tin nhưng point 3D lại sai, nó bị phạt mạnh.
>
> Nếu một vùng thật sự khó, model có thể giảm confidence.
>
> Nhưng loss cũng không cho phép nó đơn giản tuyên bố:
>
> “Tôi không biết gì cả”
>
> với mọi pixel.
>
> Kết quả là network học được không chỉ một reconstruction...
>
> mà còn một bản đồ cho biết reconstruction nào đáng tin hơn.

---

# 20:20–22:30 — Aha moment thứ hai: nhiều task trở thành by-product

**Lời thoại**

> Và bây giờ ta có thể thấy tại sao pointmap lại mạnh đến vậy.
>
> Hãy lấy bài toán pixel correspondence.
>
> Nếu một pixel trong ảnh một và một pixel trong ảnh hai được dự đoán tới gần như cùng một vị trí 3D...
>
> chúng rất có khả năng là cùng một điểm ngoài đời.
>
> Vì vậy matching có thể được thực hiện bằng nearest-neighbor search trực tiếp trong 3D pointmap space. 

**Visual**

```text
pixel A → ●
pixel B → ●
          almost same location
```

**Lời thoại**

> Camera intrinsics cũng có thể được recover.
>
> Nếu biết vị trí pixel và point 3D tương ứng, ta có thể hỏi ngược lại:
>
> “Focal length nào khiến point này project trở về đúng pixel kia?”
>
> Paper giải một optimization nhỏ cho focal length dưới một số giả định đơn giản về principal point và pixel shape. 
>
> Relative camera pose cũng vậy.
>
> Biểu diễn cùng scene trong hai camera frames khác nhau.
>
> Tìm rotation, translation và scale làm hai point clouds chồng lên nhau.
>
> Transformation đó chính là relationship giữa hai camera. Paper mô tả Procrustes alignment và PnP-RANSAC cho mục tiêu này. 

**Visual**

```text
pink point cloud
rotate
translate
scale
→ overlap blue cloud
```

**Lời thoại chốt**

> Ta bắt đầu với một model được dạy chủ yếu để predict 3D points.
>
> Nhưng từ representation đó ta có thể lấy ra:
>
> depth,
>
> matching,
>
> focal length,
>
> camera pose,
>
> visual localization,
>
> và tất nhiên là reconstruction.
>
> Không phải vì network có sáu output heads cho sáu task.
>
> Mà vì tất cả chúng đều là những góc nhìn khác nhau của **cùng một geometry**.

---

# 22:30–25:00 — Nhưng hai ảnh vẫn chưa phải cả thế giới: Global Alignment

**Lời thoại**

> Cho đến lúc này, mọi thứ khá gọn khi chỉ có hai ảnh.
>
> Nhưng một reconstruction thực tế có thể gồm hàng chục hoặc hàng trăm ảnh.
>
> DUSt3R vẫn xử lý từng cặp.
>
> Và đây là vấn đề:
>
> mỗi pair tạo ra một reconstruction trong coordinate frame cục bộ của pair đó.

Visual:

```text
I1-I2 → cloud A

I2-I3 → cloud B

I3-I4 → cloud C
```

Clouds lệch nhau.

**Lời thoại**

> Nếu muốn một scene thống nhất, chúng ta cần đưa tất cả chúng vào cùng một world coordinate frame.
>
> DUSt3R xây một graph.
>
> Mỗi image là một node.
>
> Một edge nối hai image nếu chúng có đủ nội dung chung. 
>
> Với mỗi edge, network dự đoán pointmaps.
>
> Sau đó global alignment tìm pose và scale cho từng pair sao cho những reconstruction cục bộ này cùng đồng ý về một geometry toàn cục.

Paper tối ưu transform \(P_e\) và scale \(\sigma_e\) để các pairwise pointmaps khớp với global pointmaps. 

---

# 25:00–26:10 — Khác Bundle Adjustment ở đâu?

**Lời thoại**

> Có một điểm rất đáng chú ý.
>
> Bundle Adjustment truyền thống thường điều chỉnh camera và 3D structure bằng cách giảm **2D reprojection error**.
>
> DUSt3R có một lựa chọn tự nhiên khác.
>
> Vì nó đã có pointmaps, nó có thể align chúng trực tiếp trong **3D space**.
>
> Paper nhấn mạnh rằng global optimization này không minimize reprojection error 2D như BA truyền thống, mà tối ưu disagreement trực tiếp giữa các point 3D. 

Visual:

```text
Classical BA
3D → project → image → measure 2D error

DUSt3R
3D cloud ↔ 3D cloud
measure 3D disagreement
```

---

# 26:10–27:30 — Điều gây ngạc nhiên: ít hoặc không overlap

**Lời thoại**

> Có lẽ một trong những kết quả trực quan gây bất ngờ nhất của paper là những trường hợp hai viewpoint khác nhau rất mạnh.
>
> Trong supplementary material, tác giả cho thấy những reconstruction mà visual overlap rất nhỏ, thậm chí có ví dụ hai ảnh không có overlap rõ ràng mà model vẫn suy ra được một scene 3D hợp lý.  
>
> Điều này nói cho ta một điều quan trọng:
>
> DUSt3R không chỉ đang thực hiện triangulation ngầm giữa những pixel match hoàn hảo.
>
> Network còn dựa trên những geometric và shape priors đã học từ dữ liệu.
>
> Nó đã học một phần về việc thế giới 3D thường trông như thế nào.

---

# 27:30–29:00 — Ending: vậy DUSt3R thực sự đã thay đổi điều gì?

**Lời thoại**

> Nếu phải tóm tắt DUSt3R bằng một ý duy nhất, tôi sẽ không bắt đầu từ Transformer.
>
> Tôi cũng sẽ không bắt đầu từ loss.
>
> Tôi sẽ bắt đầu từ **representation**.
>
> 3D vision truyền thống thường cố gắng giải từng câu hỏi:
>
> Pixel nào match nhau?
>
> Camera ở đâu?
>
> Depth là bao nhiêu?
>
> Sau đó ghép những câu trả lời này lại để dựng scene.
>
> DUSt3R thử một góc nhìn khác.
>
> Nó hỏi:
>
> **Nếu trước tiên ta học cách đặt mỗi pixel vào đúng vị trí trong không gian 3D thì sao?**
>
> Và một khi ta đã có representation đó...
>
> nhiều câu hỏi trước kia từng là những bài toán riêng biệt bắt đầu trở thành các hệ quả của cùng một cấu trúc.

---

# 29:00–29:40 — Final line

**Lời thoại**

> Có lẽ đó là ý nghĩa hay nhất của cái tên:
>
> **Dense and Unconstrained Stereo 3D Reconstruction.**
>
> Nhưng “Geometric 3D Vision Made Easy” không có nghĩa 3D vision bỗng trở nên dễ.
>
> Nó có nghĩa rằng đôi khi, cách tốt nhất để đơn giản hóa một chuỗi bài toán...
>
> không phải giải từng bước tốt hơn.
>
> Mà là tìm một representation khiến nhiều bước không còn cần phải tồn tại riêng biệt nữa.

Fade out:

```text
DUSt3R

Geometric 3D Vision Made Easy
```

---

# Cái tao muốn giữ xuyên suốt video

Nếu phải đóng đinh **một câu thesis** để tất cả animation và narration xoay quanh, tao chọn:

> **DUSt3R changes the order of reasoning: instead of recovering cameras first to obtain 3D, it predicts a shared 3D representation first, from which camera geometry and other tasks can be recovered.**

Bản tiếng Việt để dùng trong video:

> **DUSt3R đảo thứ tự suy luận: thay vì phải tìm camera trước rồi mới dựng được 3D, nó học một representation 3D trước, rồi từ representation đó suy ra camera và nhiều đại lượng hình học khác.**

Và đây cũng là nguyên tắc khi sau này code Manim:

```text
Không animate paper.
Animate ý tưởng.
```

Architecture, công thức và equation chỉ xuất hiện **sau khi trực giác đã được dựng xong**.