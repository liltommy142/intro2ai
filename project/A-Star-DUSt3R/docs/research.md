# Research brief — DUSt3R

## Nguồn và thông điệp chính

- Nguồn chính: Wang et al., *DUSt3R: Geometric 3D Vision Made Easy*, CVPR 2024; PDF cục bộ: references/Wang_DUSt3R_Geometric_3D_Vision_Made_Easy_CVPR_2024_paper.pdf.
- DUSt3R nhận ảnh **không cần cung cấp trước** intrinsic hay pose camera, hồi quy hình học 3D dày đặc theo cặp, rồi ghép nhiều cặp bằng tối ưu 3D. “Camera-free” ở đây là *camera-free input*, không phải camera không còn cần thiết hay không thể hồi phục.

## 1. Bài toán

MVS cổ điển thường dựa vào calibration, correspondence, SfM/BA và dense MVS để triangulate. Chuỗi này hữu ích nhưng lỗi ở detection/matching, robust estimation hoặc pose có thể truyền xuống reconstruction. DUSt3R thay đầu ra trung tâm bằng **pointmap**: một ảnh 2D mà mỗi pixel mang toạ độ 3D của điểm cảnh, để mạng học đồng thời shape, liên hệ pixel–3D và liên hệ hai view.

*Paper: Introduction, PDF pp.1–2; Sec. 3, PDF p.3.*

## 2. Pointmap và output theo cặp

Pointmap là trường dày đặc:

\[
X\in\mathbb{R}^{W\times H\times3},\qquad I_{i,j}\leftrightarrow X_{i,j}.
\]

Nếu đã có depth $D$ và intrinsic $K$, thì $X_{i,j}=K^{-1}D_{i,j}[i,j,1]^\top$. Với pose world-to-camera $P_n,P_m$, pointmap từ camera $n$ đổi sang frame camera $m$ theo

\[
X_{n,m}=P_mP_n^{-1}h(X_n). \tag{1}
\]

DUSt3R không đưa $K,P$ vào network. Với hai ảnh, network xuất

\[
f(I_1,I_2)=(X_{1,1},C_{1,1},X_{2,1},C_{2,1}),
\]

trong đó **cả hai** $X_{1,1}$ và $X_{2,1}$ đều ở frame của ảnh $I_1$, còn $C$ là confidence theo pixel. Depth chỉ là một scalar theo ray camera; pointmap là vector 3D nên cho phép matching và alignment trực tiếp trong 3D.

*Paper: Sec. 3–3.1, Eq. (1), PDF p.3; Fig. 2, PDF p.4.*

## 3. Kiến trúc đúng

1. Hai ảnh đi qua **ViT encoder Siamese có chung trọng số** để tạo $F_1,F_2$.
2. Hai Transformer decoder xử lý hai nhánh; trong mỗi block, token self-attention trong view, rồi cross-attention sang token view kia, rồi MLP. Cross-attention lặp lại là cơ chế trao đổi thông tin cần để hai pointmap được aligned.
3. Hai regression head xuất pointmap và confidence map. Không nên vẽ global alignment như một layer sau decoder: đó là hậu xử lý N-view riêng.

Paper chỉ nói rõ encoder chia sẻ trọng số; vì vậy không khẳng định decoder/head chia sẻ toàn bộ trọng số.

*Paper: Sec. 3.1, Fig. 2, PDF p.4.*

## 4. Loss: scale và confidence

Pointmap dự đoán có ambiguity scale. Với pixel hợp lệ $i\in D_v$, loss regression là

\[
\ell_{\rm regr}(v,i)=\left\|z^{-1}X_i^{v,1}-\bar z^{-1}\bar X_i^{v,1}\right\|,
\]

trong đó $z,\bar z$ là khoảng cách trung bình của các điểm hợp lệ tới origin trên hai view. Confidence-aware loss là

\[
L_{\rm conf}=\sum_{v\in\{1,2\}}\sum_{i\in D_v}
\left(C_i^{v,1}\ell_{\rm regr}(v,i)-\alpha\log C_i^{v,1}\right),
\qquad C_i=1+\exp(c_i)>0. \tag{2–4}
\]

Confidence không có nhãn trực tiếp và không nên gọi là xác suất calibrated. Nó là trọng số được học: vùng khó như sky, vật trong suốt hoặc bị che khuất có thể nhận confidence thấp hơn.

*Paper: Sec. 3.2, Eqs. (2)–(4), PDF p.4.*

## 5. Downstream từ pointmap

- **Monocular depth:** chạy $f(I,I)$; depth là toạ độ $z$ của pointmap dự đoán.
- **Pixel matching:** nearest neighbor trong không gian 3D pointmap, chỉ giữ mutual nearest neighbors để giảm false match.
- **Focal/intrinsic:** có thể fit focal từ pointmap, nhưng paper giả sử principal point gần tâm ảnh và pixel vuông; không phải hồi phục intrinsic hoàn toàn vô điều kiện.
- **Relative pose:** có thể weighted Procrustes giữa hai pointmap để lấy scaled pose, nhưng nhạy outlier; hoặc dùng matches cùng intrinsics/essential matrix hay PnP-RANSAC.
- **Absolute pose:** cần route downstream như PnP-RANSAC hoặc pose tương đối + scale; không phải output pose trực tiếp của head.

*Paper: Sec. 3.3, PDF p.5; Sec. 4.3, PDF p.7.*

## 6. N-view global alignment

Với $N$ ảnh, tạo graph $G=(V,E)$ từ image retrieval hoặc chạy pair rồi lọc edge confidence thấp. Mỗi edge $e=(n,m)$ có hai pointmap pairwise $X_{n,e},X_{m,e}$; default optimization tìm pointmap toàn cục $\chi$, rigid transform theo cặp $P_e$ và scale theo cặp $\sigma_e$:

\[
\chi^*=\arg\min_{\chi,P,\sigma}
\sum_{e\in E}\sum_{v\in e}\sum_{i=1}^{HW}
C_i^{v,e}\left\|\chi_i^v-\sigma_eP_eX_i^{v,e}\right\|,
\qquad\prod_{e\in E}\sigma_e=1. \tag{5}
\]

Ràng buộc tích scale chặn nghiệm suy biến mọi $\sigma_e=0$. Đây tối ưu residual **3D**, không phải reprojection error 2D của BA; mặc định nó không trực tiếp tối ưu pose camera cho từng ảnh. Nếu thay $\chi_n$ bằng back-projection pinhole, biến thể tùy chọn mới ước lượng $P_n,K_n,D_n$. Collection vẫn cần graph đủ liên thông về content thị giác để ghép được các ảnh.

*Paper: Sec. 3.4, Eq. (5), PDF pp.5–6.*

## 7. Training

- Fully supervised với 8 dataset: Habitat, MegaDepth, ARKitScenes, StaticScenes3D, BlendedMVS, ScanNet++, CO3D-v2 và Waymo; tổng 8.5M pair.
- GT đến từ synthetic, reconstruction SfM hoặc sensor. Train tuần tự 224×224 rồi ảnh cạnh lớn 512 px; random aspect ratio/crop, augmentation chuẩn.
- Encoder ViT-L, decoder ViT-B, patch 16×16, DPT head; khởi tạo từ CroCo pretrained. Test resize cạnh lớn về 512 px, giữ aspect ratio.
- Không có geometric constraint được ép tường minh khi inference; network học prior hình học từ dữ liệu.

*Paper: Sec. 4 “Training data” và “Training details”, PDF p.6.*

## 8. Bằng chứng nên đưa lên video

| Task / setting | DUSt3R | Cách đọc đúng và caveat |
|---|---:|---|
| Monocular depth, NYUD-v2, DUSt3R512 | Rel **6.50**; $\delta_{1.25}$ **94.09** | Table 2; cùng model, setting transfer/zero-shot của paper. |
| Multi-view pose, CO3Dv2, 10 random frames, global alignment | RRA@15 **96.2**; RTA@15 **86.8**; mAA@30 **76.7** | GA không thắng mọi metric: PnP là **94.3 / 88.4 / 77.2**, nên PnP có mAA@30 cao hơn. |
| Multi-view depth, ETH3D, Table 3 setting (d) | Rel **2.91**; InlierRatio(1.03) **76.91** | Không GT camera/pose/depth range, có alignment; prediction được **median-aligned** khi đánh giá do ambiguity scale. |
| Full reconstruction, DTU zero-shot | Acc. **2.677 mm**; Comp. **0.805 mm**; Overall **1.741 mm** | Đánh giá sau khi prediction được align vào hệ toạ độ GT. GeoMVSNet chuyên DTU/GT cameras đạt **0.331 / 0.259 / 0.295 mm**, nên không che giấu trade-off accuracy. |

*Paper: Table 2 và Secs. 4.2–4.3, PDF pp.7–8; Table 3 và Secs. 4.4–4.5, PDF p.8.*

## 9. Giới hạn cần nói trung thực

- Pointmap không bị ép phải tuân camera model vật lý ở inference; paper nói chúng gần phù hợp thực tế, không bảo đảm tuyệt đối.
- Scale metric không tự xuất hiện chỉ vì network không cần camera input; nhiều đánh giá cần scale/GT-coordinate alignment.
- Global alignment vẫn là post-processing numerical optimization trên graph pair, không phải phép màu thay thế mọi điều kiện connectivity/overlap.
- DTU cho thấy đánh đổi rõ: plug-and-play không calibration/pose input, nhưng accuracy không bằng specialist có GT cameras và train chuyên domain.
- Không gọi mọi kết quả là zero-shot tuyệt đối: paper ghi ScanNet test có overlap với Habitat training split.

*Paper: Secs. 3.1, 3.4, 4.4–4.5, PDF pp.4, 6–8.*

## 10. 12 câu hỏi vấn đáp nhanh

1. **Pointmap khác depth map?** Pointmap là vector 3D theo pixel, depth chỉ là scalar theo ray; depth cần $K$ để thành pointmap. *Sec. 3, Eq. (1), p.3.*
2. **“Camera-free” nghĩa gì?** Không cần intrinsic/pose làm input; camera vẫn có thể được recover bằng route downstream hoặc biến thể pinhole. *Secs. 3.3–3.4, pp.5–6.*
3. **Vì sao $X_{1,1}$ và $X_{2,1}$ chung frame $I_1$?** Để so cloud/match/alignment trực tiếp trong 3D. *Sec. 3.1, Fig. 2, p.4.*
4. **Cross-attention làm gì?** Mỗi decoder block trao đổi token hai view; paper nói điều này quan trọng để output aligned. *Sec. 3.1, p.4.*
5. **Vì sao phải chuẩn hoá scale?** Hình học từ ảnh có scale ambiguity; Eqs. (2)–(3) tránh phạt khác biệt scale toàn cục. *Sec. 3.2, p.4.*
6. **Confidence có phải xác suất đúng?** Không; nó được học gián tiếp làm trọng số loss, không có supervision confidence. *Sec. 3.2, Eq. (4), p.4.*
7. **Pairwise khác N-view?** Pair network chỉ ra hai pointmap; N-view cần graph pair và tối ưu global alignment. *Secs. 3.1, 3.4, pp.3–6.*
8. **Global alignment có phải BA?** Không; Eq. (5) giảm residual 3D thay vì reprojection error 2D. *Sec. 3.4, Eq. (5), pp.5–6.*
9. **Tại sao $\prod_e\sigma_e=1$?** Để chặn nghiệm suy biến mọi scale bằng 0. *Sec. 3.4, p.6.*
10. **Match pixel thế nào?** Mutual nearest neighbor giữa hai pointmap trong không gian 3D. *Sec. 3.3, p.5.*
11. **Lấy relative pose thế nào?** Procrustes cho scaled pose nhưng nhạy outlier; có thể dùng matches + essential/PnP-RANSAC. *Sec. 3.3, p.5.*
12. **Trade-off DTU?** DUSt3R zero-shot/no camera input đạt 1.741 mm overall sau GT-coordinate alignment, nhưng accuracy không bằng specialist GT-camera/train-DTU. *Sec. 4.5, Table 3, p.8.*
