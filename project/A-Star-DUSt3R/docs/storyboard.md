# Storyboard

Mục tiêu là kể một câu chuyện liên tục: vì sao dựng 3D từ ảnh khó, DUSt3R thay đổi điểm nào, và bằng chứng nào cho thấy cách tiếp cận này hữu ích.

| # | Scene | Mục tiêu | Visual chính |
|---:|---|---|---|
| 1 | Intro | Tạo hook về dựng thế giới 3D từ ảnh. | Hai ảnh, lưới 2D chuyển thành point cloud. |
| 2 | Problem | Đặt bài toán dense stereo reconstruction. | Cặp ảnh, vùng che khuất và chiều sâu chưa biết. |
| 3 | Traditional Pipeline | Giải thích độ phức tạp của cách cũ. | Matching → pose camera → triangulation → point cloud. |
| 4 | DUSt3R Method | Trình bày ý tưởng pointmap trực tiếp. | Image pair → transformer → pointmaps → 3D scene. |
| 5 | Architecture | Làm rõ các thành phần mô hình. | Encoder/decoder, pointmap head và global alignment. |
| 6 | Results | Đọc kết quả một cách có bằng chứng. | Một bảng/biểu đồ đã trích dẫn và qualitative reconstruction. |
| 7 | Conclusion | Tóm tắt đóng góp, giới hạn và thông điệp cuối. | So sánh pipeline cũ/mới và ba takeaway. |

Chỉ thêm thời lượng chi tiết, asset cụ thể và transition sau khi research brief được kiểm chứng. Mọi visual dựa trên paper phải có nguồn ghi trong lời thoại hoặc credit cuối video.
