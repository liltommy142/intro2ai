# A-Star-DUSt3R: Tối giản cấu trúc project

## Mục tiêu

Biến project thành workspace gọn, đủ cho hai người nghiên cứu paper DUSt3R và sản xuất video Manim. Chỉ giữ các tệp phục vụ trực tiếp cho nghiên cứu, kịch bản, mã nguồn và nộp bài.

## Phạm vi giữ lại

- `README.md`: điểm vào và cách dùng project.
- `TEAM.md`: hai thành viên và vai trò.
- `TODO.md`: backlog duy nhất, có trạng thái và người phụ trách.
- `references/`: paper, supplementary, BibTeX và tài liệu tham khảo đã có.
- `docs/research.md`: tóm tắt, đóng góp, background, kỹ thuật, kết quả, giới hạn, FAQ và citations.
- `docs/storyboard.md`: bảy scene đã thống nhất, thời lượng, hình ảnh và chuyển cảnh.
- `docs/voice-script.md`: lời thoại theo từng scene.
- `docs/submission-checklist.md`: kiểm tra trước khi nộp.
- `src/scenes/`: mã Manim thực tế, chỉ được thêm khi scene tương ứng đã chốt.

## Phạm vi loại bỏ

- Hai tệp trùng hoàn toàn ở `project/plan.md` và `project/note.md`; bản chuẩn nằm trong workspace A-Star và nội dung hữu ích sẽ được chắt lọc vào các tài liệu giữ lại.
- Các tài liệu template phân mảnh trong `docs/01_Project`, `docs/02_Paper`, `docs/03_Technical`, `docs/04_Video`.
- `ROADMAP.md`, `TIMELINE.md`, `MEETING.md`, `CHANGELOG.md` và `CONTRIBUTING.md`; chúng chưa chứa lịch sử hay quy trình thực tế, và nhiệm vụ của chúng được thay bởi `TODO.md`/README.
- `docs/meetings/meeting-01.md` rỗng.
- Bảy tệp Python placeholder hiện tại trong `src/` và `utils.py`; chúng không dùng Manim, không render được và không phải nền tảng tái sử dụng.

## Chuyển đổi nội dung

- Chắt lọc `plan.md` thành `docs/research.md`, `docs/storyboard.md` và `docs/voice-script.md`; bỏ các lời dẫn chung, cấu trúc đề xuất cũ và ký hiệu tham chiếu lỗi.
- Dùng đúng bảy scene: Intro, Problem, Traditional Pipeline, DUSt3R Method, Architecture, Results, Conclusion.
- `TODO.md` là nguồn trạng thái duy nhất; mỗi mục có người phụ trách (`Tuấn` hoặc `Anh Tuấn`) và tiêu chí hoàn thành.

## Tiêu chí hoàn thành

- Không còn file trùng lặp, template rỗng hoặc code placeholder.
- Một người mới có thể biết ngay phải đọc gì, làm gì và đặt output ở đâu từ README/TODO.
- Không xoá paper, supplementary, BibTeX hay tài liệu khóa học ngoài workspace A-Star.
