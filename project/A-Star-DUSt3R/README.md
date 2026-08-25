# A-Star-DUSt3R

Workspace tối giản cho nhóm hai người nghiên cứu **DUSt3R: Geometric 3D Vision Made Easy** và làm video giải thích bằng Manim theo phong cách 3Blue1Brown.

## Cốt truyện trong một câu

DUSt3R không làm camera biến mất: nó đổi camera từ điều kiện phải biết trước thành một đại lượng có thể suy ra sau khi hai ảnh đã cùng dự đoán hình học 3D.

```text
Pipeline cổ điển: camera + matches → triangulation → 3D
DUSt3R:           images → pointmaps → 3D → depth / matches / camera
```

Visual animatic hiện có đủ bảy chương và dùng một hệ màu/vật thể xuyên suốt. Lời thoại production nhắm khoảng 9 phút 20 giây; timing cuối sẽ được khóa sau khi thu giọng.

## Bảy chương

| # | Chương | File / class |
|---:|---|---|
| 1 | Một ảnh, nhiều thế giới 3D | `intro.py` / `IntroScene` |
| 2 | Hình học cổ điển và lỗi tuần tự | `classical_geometry.py` / `ClassicalGeometryScene` |
| 3 | Pixel trở thành pointmap | `pointmap.py` / `PointmapScene` |
| 4 | Hai pointmap trong frame ảnh 1 | `pairwise.py` / `PairwiseScene` |
| 5 | Shared encoder và cross-attention decoder | `network.py` / `NetworkScene` |
| 6 | Global alignment nhiều view | `global_alignment.py` / `GlobalAlignmentScene` |
| 7 | Downstream tasks, kết quả và trade-off | `takeaways.py` / `TakeawaysScene` |

## Chạy project

Yêu cầu Python 3.11 hoặc mới hơn, FFmpeg và các system dependency của Manim.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Render nhanh toàn bộ visual animatic:

```powershell
.\.venv\Scripts\python.exe -m manim -ql render.py FullVideo
```

Render một chương để chỉnh:

```powershell
.\.venv\Scripts\python.exe -m manim -ql render.py PointmapScene
```

Render 1080p sau khi đã khóa voice timing:

```powershell
.\.venv\Scripts\python.exe -m manim -qh render.py FullVideo
```

Chạy test hợp đồng scene và render dry-run của architecture:

```powershell
.\.venv\Scripts\python.exe -m unittest tests\test_foundation_scenes.py
```

## Đọc theo thứ tự

1. [research.md](docs/research.md): formulation, số liệu, giới hạn và 12 câu vấn đáp.
2. [storyboard.md](docs/storyboard.md): visual grammar và shot list 0:00–9:20.
3. [voice-script.md](docs/voice-script.md): lời thoại đồng bộ với các beat `[ON SCREEN]`.
4. [TODO.md](TODO.md): trạng thái duy nhất của nhóm.
5. [submission-checklist.md](docs/submission-checklist.md): kiểm tra trước khi nộp.

## Cấu trúc tối thiểu

```text
references/       Paper chính, arXiv, supplementary PDF/video
docs/             Research, storyboard, lời thoại, checklist
src/scenes/       7 chapter + visual primitives dùng chung
tests/            Fast contract và dry-run test
render.py         Entry point cho từng chapter hoặc FullVideo
requirements.txt  Một dependency Python trực tiếp
```

`media/` chỉ là output render và đã bị Git ignore.

## Nguồn

- Wang et al., *DUSt3R: Geometric 3D Vision Made Easy*, CVPR 2024.
- [CVPR Open Access](https://openaccess.thecvf.com/content/CVPR2024/html/Wang_DUSt3R_Geometric_3D_Vision_Made_Easy_CVPR_2024_paper.html)
- [3Blue1Brown](https://www.youtube.com/c/3blue1brown) — tham chiếu ngôn ngữ giải thích/animation, không sao chép asset.

Mọi hình chính trong animation được tái tạo bằng vector geometry. Số benchmark phải luôn đi cùng dataset, metric, setting và caveat ghi trong research brief.
