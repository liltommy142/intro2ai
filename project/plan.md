Nhóm **24C05 – A-Star** đã chọn một paper rất mạnh:

- **Paper:** **DUSt3R: Geometric 3D Vision Made Easy**
- **Venue:** IEEE/CVF Conference on Computer Vision and Pattern Recognition (**CVPR 2024**)
- **Rank:** **A\*** (CORE)
- **Thời gian:** June 2024
- **Trạng thái:** Accepted
- **Official paper:** [CVPR Open Access Paper](https://openaccess.thecvf.com/content/CVPR2024/html/Wang_DUSt3R_Geometric_3D_Vision_Made_Easy_CVPR_2024_paper.html?utm_source=chatgpt.com)
- **Official implementation:** [GitHub (naver/dust3r)](https://github.com/naver/dust3r?utm_source=chatgpt.com)

Paper này đề xuất một hướng tiếp cận mới cho **Dense and Unconstrained Stereo 3D Reconstruction**: thay vì phải biết trước thông số camera (intrinsic/extrinsic), mô hình dự đoán trực tiếp **pointmaps** từ ảnh và sau đó suy ra nhiều đại lượng hình học như độ sâu, pose camera và mô hình 3D. Đây là điểm mới cốt lõi của DUSt3R. 

---

# Outline toàn bộ project

Nếu mục tiêu là **điểm cao (9–10)** thì mình khuyên nhóm chuẩn bị theo cấu trúc này.

## Phase 1. Research

### 1. Background

Mọi thành viên phải hiểu:

- 3D Vision
- Stereo Vision
- Multi-view Stereo (MVS)
- Camera Intrinsic
- Camera Extrinsic
- Triangulation
- Depth Estimation
- Point Cloud
- Structure from Motion (SfM)

Nếu chưa hiểu các khái niệm này thì sẽ rất khó theo dõi paper, vì DUSt3R xây dựng trên nền các bài toán đó. 

---

## Phase 2. Paper Analysis

Đọc paper theo thứ tự:

```
Abstract

↓

Introduction

↓

Related Work

↓

Method

↓

Experiments

↓

Limitations

↓

Conclusion
```

Không nên đọc từ đầu đến cuối một lượt; hãy quay lại phần Method sau khi đã nắm được bài toán.

---

## Phase 3. Chia việc

Ví dụ nhóm 4 người:

| Member | Công việc |
|---------|-----------|
| A | Background + Introduction |
| B | Related Work |
| C | Method |
| D | Experiments + Results |

Sau đó họp để ghép lại thành một câu chuyện thống nhất.

---

# Phase 4. Technical Report

Tạo một tài liệu nội bộ gồm:

```
1. Problem

2. Previous methods

3. Weaknesses

4. DUSt3R idea

5. Architecture

6. Training

7. Inference

8. Experiments

9. Ablation

10. Limitations

11. Future work
```

Đây sẽ là "nguồn gốc" để viết lời thoại và làm slide/video.

---

# Phase 5. Storyboard

Video nên kể chuyện theo kiểu 3Blue1Brown.

Ví dụ:

## Scene 1

Hook

> "Nếu chỉ có hai tấm ảnh, liệu AI có thể dựng cả thế giới 3D?"

---

## Scene 2

Problem

Giới thiệu:

- Multi-view Stereo
- Camera Calibration
- Pose Estimation

---

## Scene 3

Tại sao cách cũ khó?

Cho animation:

```
Image

↓

Feature Matching

↓

Camera Pose

↓

Triangulation

↓

Point Cloud
```

Giải thích vì sao pipeline truyền thống phụ thuộc mạnh vào hiệu chuẩn camera.

---

## Scene 4

Ý tưởng DUSt3R

Đây là phần quan trọng nhất.

Cho animation:

```
Image A

+

Image B

↓

Transformer

↓

Point Maps

↓

3D Scene
```

Nhấn mạnh rằng mô hình **dự đoán pointmaps trực tiếp**, thay vì đi qua pipeline camera calibration truyền thống. 

---

## Scene 5

Architecture

Minh họa:

```
Encoder

↓

Decoder

↓

Pointmap Regression

↓

Global Alignment
```

---

## Scene 6

Results

Hiển thị:

- bảng
- biểu đồ
- qualitative results

---

## Scene 7

Conclusion

- Contributions
- Strengths
- Weaknesses

---

# Phase 6. Manim

Chia scene:

```
Scene01

Title

Scene02

Problem

Scene03

Old pipeline

Scene04

DUSt3R

Scene05

Architecture

Scene06

Experiments

Scene07

Conclusion
```

---

# Phase 7. Voice Script

Mỗi scene có:

- thời lượng
- lời thoại
- animation
- hiệu ứng
- asset cần dùng

Ví dụ:

```
Scene 4

Time

3 phút

Narration

Animation

Objects

Transition
```

---

# Phase 8. Assets

Chuẩn bị trước:

- SVG
- icon
- point cloud
- camera icon
- coordinate axis
- grid
- arrows
- LaTeX equations
- hình từ paper (tuân thủ trích dẫn nếu sử dụng)

---

# Phase 9. Demo

Nếu có thời gian, chạy thử repository chính thức:

- inference trên vài ảnh
- point cloud
- depth map

Việc này giúp nhóm trả lời phần vấn đáp tự tin hơn. [Official GitHub Repository](https://github.com/naver/dust3r?utm_source=chatgpt.com)

---

# Phase 10. Question Bank

Chuẩn bị trước các câu hỏi như:

- Vì sao DUSt3R không cần camera calibration ban đầu?
- Pointmap là gì?
- Tại sao dùng Transformer?
- Global Alignment hoạt động thế nào?
- So với MVS truyền thống khác gì?
- Paper đóng góp gì?
- Hạn chế của paper?
- Nếu làm tiếp research thì sẽ cải tiến gì?

---

## Đề xuất sản phẩm cuối cùng của nhóm

Để quản lý công việc hiệu quả, mình khuyên nhóm A-Star tạo cấu trúc dự án như sau:

```
A-Star-DUSt3R/

├── 01_Paper/
│   ├── paper.pdf
│   ├── supplementary.pdf
│   └── notes.md
│
├── 02_Research/
│   ├── summary.md
│   ├── glossary.md
│   ├── architecture.md
│   └── question_bank.md
│
├── 03_Storyboard/
│   ├── storyboard.md
│   ├── narration.md
│   └── timeline.md
│
├── 04_Assets/
│   ├── images/
│   ├── svg/
│   ├── icons/
│   └── equations/
│
├── 05_Manim/
│   ├── scene01_intro.py
│   ├── scene02_problem.py
│   ├── scene03_pipeline.py
│   ├── scene04_dust3r.py
│   ├── scene05_architecture.py
│   ├── scene06_results.py
│   └── scene07_conclusion.py
│
├── 06_Audio/
├── 07_FinalVideo/
└── README.md
```

Với paper này, mình có thể đồng hành cùng nhóm từ đầu đến cuối: **:chatgpt-content-reference{index="7"}, :chatgpt-content-reference{index="8"}, :chatgpt-content-reference{index="9"}, và :chatgpt-content-reference{index="10"}**.