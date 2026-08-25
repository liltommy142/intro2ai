# Production storyboard — DUSt3R (9:20)

Mục tiêu là làm rõ một thay đổi ý niệm: thay vì coi camera là điều kiện đầu vào bắt buộc, DUSt3R hồi quy pointmap rồi suy ra nhiều đại lượng hình học. Video giải thích cơ chế trước, đưa benchmark có điều kiện sau, và giữ các caveat ngay cạnh claim tương ứng.

## Visual grammar dùng xuyên suốt

- Nền `PALETTE["background"]` (`#0B0F14`); panel tối `surface`/`surface_2`; chữ chính `ink`, chú thích/caveat `muted`.
- Màu là dữ liệu, không chỉ trang trí: view 1 xanh `view_1`, view 2 cam `view_2`, pair-frame tím `pair_frame`, pose hồng `pose`, confidence cao xanh lá `confidence`, low-confidence đỏ mờ `low_confidence`, world frame vàng `world`.
- Một pixel phải giữ màu của nó khi chuyển **pixel → token → 3D point**. Khi hai view gặp nhau, chỉ point nào đã được căn vào common/world frame mới đổi sang vàng. Low confidence giảm opacity, không bị xoá lặng lẽ.
- Không dùng screenshot paper làm shot chính: tái tạo vector geometry; mỗi metric xuất hiện cùng dataset, metric, setting và caveat. Camera/axis, toy cube và floor là “vật thể liên tục” giúp khán giả giữ hướng.

## 1. 0:00–0:50 — Hook: một ảnh không quyết định được thế giới 3D

**Mục tiêu học.** Người xem cảm nhận được ambiguity: cùng một pixel/ảnh 2D không tự quyết định chiều sâu hay pose camera.

**Shot list.**

- `0:00–0:12`: một `make_image_panel` xanh giữ toy cube/pillar; một pixel xanh phóng lớn, ray depth mở ra ba vị trí 3D khả dĩ.
- `0:12–0:28`: ảnh cam thứ hai xoay vào, ray thứ hai cắt/không cắt các giả thuyết; cube morph từ flat grid thành cloud thưa nhưng còn lệch frame.
- `0:28–0:42`: cùng cặp ảnh, một camera icon bị phủ dấu `?` ở focal và pose; các đường triangulation cổ điển nhấp nháy như điều kiện còn thiếu.
- `0:42–0:50`: câu hỏi treo lại: “Can geometry come before calibration?”; pixel xanh/cam giữ nguyên để chảy sang chương 2.

**Vật thể giữ lại.** Hai panel ảnh, cube/pillar/floor, pixel màu theo view, hai camera chưa biết.

**Animation/morph.** Pixel-grid cell scale lên → `Dot`/candidate points; camera FOV rotate; candidate depth points xuất hiện rồi bị ghost-opacity. Không cắt sang slide chữ.

**Narration beat.** “Một ảnh cho appearance, không cho một đáp án 3D duy nhất. Hai ảnh giúp, nhưng cách quen thuộc đòi camera đã biết.”

**Citation.** Main paper Fig. 1, p.1; §1, pp.1–2.

**Lỗi cần tránh.** Không nói monocular depth là “impossible”; bài toán là ill-posed và mạng dùng learned priors. Không hứa two-view luôn triangulate được khi calibration chưa có.

**Manim.** `src/scenes/intro.py` — `IntroScene`.

## 2. 0:50–2:00 — Classical geometry: pipeline đúng, nhưng nhiều tiền điều kiện

**Mục tiêu học.** Phân biệt matching, pose/SfM, triangulation/MVS; hiểu vì sao lỗi upstream lan downstream.

**Shot list.**

- `0:50–1:08`: pixel màu từ hai panel nối thành sparse mutual matches; outlier đỏ rung và bị RANSAC loại.
- `1:08–1:27`: matches xoay hai camera hồng vào một sparse frame; pose error rất nhỏ được phóng đại thành lệch ray.
- `1:27–1:46`: rays triangulate thành sparse cloud, rồi MVS quét dày qua surface; mỗi khối nhận output khối trước bằng morph, không thay trang.
- `1:46–2:00`: một link pose mờ đi, cloud cuối vỡ/ghost; nhãn “calibration + pose first” co lại thành một prerequisite card.

**Vật thể giữ lại.** Hai ảnh/pixel màu, camera, cube/pillar/floor; sparse points từ hook trở thành tracks.

**Animation/morph.** Line matches → epipolar/ray lines → sparse dots → surface dots; outlier dùng `low_confidence`, pipeline arrows nối vật thể thật.

**Narration beat.** “SfM và MVS rất mạnh, nhưng là chuỗi phụ thuộc: matching, camera, rồi dense geometry. Một sai số nhỏ ở pose đổi vị trí mọi ray.”

**Citation.** Main §1, pp.1–2; §2–§3, pp.2–3.

**Lỗi cần tránh.** Không mô tả classical pipeline là lỗi thời hay luôn thất bại. Không nói DUSt3R bỏ tất cả hậu xử lý: multi-view vẫn dùng global alignment.

**Manim.** `src/scenes/classical_geometry.py` — `ClassicalGeometryScene`.

## 3. 2:00–3:25 — Pointmap: mỗi pixel hồi quy một điểm 3D

**Mục tiêu học.** Định nghĩa pointmap, phân biệt với depth map, và thấy correspondence pixel–point còn được giữ.

**Shot list.**

- `2:00–2:18`: retained pixel grid xanh morph từng cell thành point cloud có cùng màu; một point được kéo về grid để cho thấy mapping một-một.
- `2:18–2:40`: tách cùng output thành hai “lát cắt”: `z` là depth, còn `(x,y,z)` là pointmap; depth chỉ hiện intensity, pointmap còn cho vị trí lateral.
- `2:40–3:04`: confidence halo xanh lớn quanh surface rõ; sky/translucent/occluded cells đỏ-mờ, cloud ở đó không bị biến thành fact chắc chắn.
- `3:04–3:25`: cloud xoay nhẹ và chiếu lại panel; pixel màu quay về đúng point, mở đường sang hai output trong common frame.

**Vật thể giữ lại.** Grid/pixel màu, toy world, camera từ chapter 2; thêm confidence halo và pointmap axes vàng.

**Animation/morph.** `make_pixel_grid` → `make_point_cloud`; z-coordinate flatten thành depth strip rồi reverse morph; `confidence_halo` fade theo quality.

**Narration beat.** “Depth chỉ trả lời xa gần trên camera ray. Pointmap gán một toạ độ 3D cho từng pixel — vì thế nó giữ được cả hình học lẫn liên hệ pixel–scene.”

**Citation.** Main §3, p.3; §3.1–§3.2, pp.3–4; Fig. 3, p.5.

**Lỗi cần tránh.** Không gọi pointmap là “depth map tốt hơn”. Pointmap output chỉ xác định **up to scale**; không nói nó tự bảo đảm metric scale hay camera model vật lý.

**Manim.** `src/scenes/pointmap.py` — `PointmapScene`.

## 4. 3:25–4:50 — Common frame: hai view phải nói cùng hệ toạ độ

**Mục tiêu học.** Hiểu rằng DUSt3R dự đoán `X¹,¹` và `X²,¹`: hai pointmap trong frame ảnh 1, nên pair có thể so sánh trực tiếp.

**Shot list.**

- `3:25–3:42`: panel xanh/cam vào hai lane; cloud cam ban đầu có axes tím local, cloud xanh có axes xanh.
- `3:42–4:03`: camera 1 được pin tại origin; một frame label “camera 1” bọc cả hai output; cloud cam rotate/translate vào axes của cloud xanh.
- `4:03–4:26`: các corresponding colored dots nối short 3D segments; segment ngắn đi khi common frame lock, nhưng low-confidence segment còn mờ.
- `4:26–4:50`: frame camera 1 màu xanh tiếp tục bọc cả pair; hai pointmap co thành một pair-output card để đi vào network. Màu vàng chỉ xuất hiện ở world frame của chương 6.

**Vật thể giữ lại.** Hai panels, per-pixel colors, confidence halos, toy world; camera 1 ở origin trở thành anchor.

**Animation/morph.** Tím local axes rotate/translate → vàng/common axes; match segments co, không dùng mũi tên “magic alignment”.

**Narration beat.** “Điểm quan trọng không chỉ là hai cloud: cả hai được biểu diễn trong frame của ảnh một. Do đó khoảng cách 3D đã có nghĩa giữa hai view.”

**Citation.** Main §3.1 và Fig. 2, pp.3–4; §3.3, p.5.

**Lỗi cần tránh.** Không nói common frame là GT world frame hoặc global reconstruction; ở đây mới là **pairwise common frame**. Không bỏ confidence.

**Manim.** `src/scenes/pairwise.py` — `PairwiseScene`.

## 5. 4:50–6:10 — Network: shared encoder, cross-view decoder, regression heads

**Mục tiêu học.** Nêu đúng vai trò Siamese ViT/cross-attention/DPT heads mà không biến video thành sơ đồ block tĩnh.

**Shot list.**

- `4:50–5:08`: retained blue/orange grids break thành token grids cùng màu; hai đường đi qua một encoder shell có nhãn “shared weights”.
- `5:08–5:31`: token rows chạy qua decoder lanes; cross-attention arcs trao đổi token màu giữa lanes, mỗi block pulse thay phiên.
- `5:31–5:52`: regression heads morph token grids thành hai pointmap + confidence maps; head output giữ pair common frame từ chapter 4.
- `5:52–6:10`: một loss ruler so prediction với supervised 3D points; confidence chọn trọng số, camera icon vẫn không được feed làm input.

**Vật thể giữ lại.** Pixel/token/point colors, pair common axes, confidence halos.

**Animation/morph.** Cell → token rounded-rect → Dot; cross-attention dùng arcs moving, head là morph chứ không fade-in card. Pair-frame purple không bị đổi world vàng ở chapter này.

**Narration beat.** “Hai encoder chia trọng số; decoder trao đổi thông tin giữa view. Head hồi quy pointmap và confidence, còn camera geometry được học ngầm từ data chứ không được hard-code lúc inference.”

**Citation.** Main §3.1–§3.2, pp.3–4; Fig. 2, p.4; §4 training/evaluation, p.6.

**Lỗi cần tránh.** Không gọi network ‘geometry-free’: paper nói architecture không enforce ràng buộc camera rõ ràng, không phải output chắc chắn phi vật lý. Không nói confidence có GT supervision riêng.

**Manim.** `src/scenes/network.py` — `NetworkScene`.

## 6. 6:10–7:45 — Global alignment: nhiều pair-frame thành một world frame

**Mục tiêu học.** Biết global alignment là **hậu xử lý** sau pairwise network, tối ưu consistency 3D thay vì BA reprojection residual 2D.

**Shot list.**

- `6:10–6:28`: năm image nodes tạo co-visibility graph; edges tím là pairs, một edge `low confidence` mờ thay vì bị tin bằng nhau.
- `6:28–6:49`: ba point clouds local tím xuất hiện với axes/scale khác nhau; residual đỏ kéo từ cloud local về vị trí world candidate.
- `6:49–7:12`: các local frames rotate, translate và rescale thành clouds vàng trong world axes; residual đỏ co thành dot. Nhãn hiện: “post-processing: global alignment” và `∏ σₑ = 1`.
- `7:12–7:31`: inset so sánh “BA: 2D reprojection residual” và “GA: 3D pointmap residual”; cả hai residual cùng co để nhấn khác không gian tối ưu.
- `7:31–7:45`: world cloud giữ lại, camera intrinsics/poses xuất hiện như quantities recovered — chuyển cảnh sang downstream tasks.

**Vật thể giữ lại.** Pair clouds, confidence opacity, point colors và axes; vàng chỉ dùng khi world-consistent.

**Animation/morph.** `Transform` cloud local tím → cloud world vàng kèm rotate/shift/scale; red residual `Line` → short line → dot; graph edges không biến thành calibrated poses.

**Narration beat.** “Với nhiều ảnh, network vẫn chỉ dự đoán theo cặp. Global alignment là bước sau đó: tìm global pointmap cùng rigid transform và scale của từng edge trực tiếp trong 3D; gauge `∏ σₑ = 1` chặn nghiệm scale tầm thường.”

**Citation.** Main §3.4, pp.5–6; Supplement §F–G, pp.7–8; Supplement Fig. 7, p.4.

**Lỗi cần tránh.** Không nói GA là end-to-end network hoặc bundle adjustment chuẩn. Không nói pairwise cloud đã metric-scale; `σₑ` tồn tại chính vì ambiguity scale.

**Manim.** `src/scenes/global_alignment.py` — `GlobalAlignmentScene`.

## 7. 7:45–9:20 — Downstream tasks và kết luận có điều kiện

**Mục tiêu học.** Thấy một pointmap sinh nhiều output, đồng thời biết metric nào thuộc dataset/setting nào và trade-off reconstruction.

**Shot list.**

- `7:45–8:05`: retained central pointmap spawn bốn nhánh thật: `z → depth`, nearest-neighbour reciprocal → mutual-NN matches, pointmap geometry → focal + pose, nhiều pairmaps → multi-view cloud.
- `8:05–8:21`: glyph 1: **NYUD-v2, transfer** — `Rel 6.50↓`, `δ1.25 94.09↑`.
- `8:21–8:37`: glyph 2: **CO3Dv2, GA, 10 random frames** — `RRA@15 96.2↑`, `RTA@15 86.8↑`. Không hiện claim “best every metric”.
- `8:37–8:59`: glyph 3: **DTU zero-shot; no GT cameras input** — `accuracy 2.677 mm`, `completeness 0.805 mm`, `overall 1.741 mm`; ngay dưới là “after GT evaluation alignment” và “specialist accuracy trade-off”.
- `8:59–9:12`: compact caveat strip: predicted pointmaps up-to-scale; multi-view depth uses median GT alignment for evaluation; DTU evaluation aligns GT coordinate system.
- `9:12–9:20`: camera card morph từ “prerequisite” thành “downstream quantity”; world cloud còn ở background, không lặp metric.

**Vật thể giữ lại.** Central pointmap/point colors, golden global cloud, camera/axes; metric glyphs thay phiên, không thành bảng số liệu.

**Animation/morph.** Pointmap dots emit four spokes, branch icons materialize từ chính dots; metric rings draw theo thứ tự và fade trước câu kết; caveat strip xuất hiện đồng thời với DTU, không ở end-card nhỏ khó đọc.

**Narration beat.** “Cùng một representation có thể cho depth, matches, focal, pose và multi-view geometry. Bằng chứng mạnh, nhưng luôn theo setting: pointmap chưa cho metric scale tự động, và DTU vẫn đánh đổi độ chính xác chuyên biệt để đổi lấy plug-and-play.”

**Citation.** Main §3.3, p.5; §4.2–§4.5, pp.7–8; Table 2–3, p.8; Supplement §D/F, pp.7–8.

**Lỗi cần tránh.** Không gọi NYUD/CO3Dv2/DTU là một “SOTA” chung. Không diễn giải DTU 1.741 mm là reconstruction tự căn hệ metric; không ẩn evaluation alignment. Không hứa global alignment luôn thắng PnP trên mọi metric.

**Manim.** `src/scenes/takeaways.py` — `TakeawaysScene`.

## Handoff tối thiểu cho hai người

- Người A: chapters 1–4, bảo toàn màu pixel/view và kiểm tra terminology pointmap/common frame.
- Người B: chapters 5–7, bảo toàn transition token→point/point→world và kiểm tra mọi metric/caveat đúng citation.
- Khi ghép render, chapter chỉ được cắt ở 0:50, 2:00, 3:25, 4:50, 6:10, 7:45, 9:20; toy world và palette là continuity check nhanh nhất.
