# Old Sessions

Bản chất & Ví dụ: - Session lifecycle: Session phải được tạo, dùng, hết hạn, vô hiệu hóa đúng.- Old session: Token cũ còn dùng được là lỗi quản lý phiên.- Invalidation: Logout/reset password cần vô hiệu hóa session liên quan.
Hệ sinh thái kiến thức: - Session reuse- Stale session- Cookie/session storage- Server session invalidation- Auth lifecycle
Trạng thái: Chưa bắt đầu
Trạng thái 1: Chưa bắt đầu
Tên bài / Chủ đề: Old Sessions

![image.png](Old%20Sessions/image.png)

Đề bài cho ta biết là có lỗ hổng ở phiên đăng nhập vì phiên cũ vẫn còn sống vĩnh viễn và ta sẽ cần vào tài khoản mà không cần mật khẩu

![image.png](Old%20Sessions/image%201.png)

Ở đây đầu tiên thì mình sẽ thử đăng ký và đăng nhập xem sao 

![image.png](Old%20Sessions/image%202.png)

Sau khi đăng ký và đăng nhập tài khoản `vanduc` thành công, tại giao diện `Homepage` (`/`), mình thu thập được 2 thông tin quan trọng ở mục **Comments**:   
• Tài khoản mục tiêu là **`Admin`** (đã đăng nhập từ `2023-01-02`).   
• Bình luận của `mary_jones_8992` tiết lộ một đường dẫn ẩn: **`/sessions`** (*"Hey I found a strange page at /sessions"*).   
• **Bước tiếp theo:** Mình tiến hành truy cập vào endpoint `/sessions` để kiểm tra.

![image.png](Old%20Sessions/image%203.png)

Khi gửi request `GET /sessions`, từ phần **Response** mình thu được:   
• **Lộ Session ID của `admin`:** `1FCb9pBtwaCfNO6ivJXizYZAQm3z-2kli0WkbG9Cv3c` (vẫn còn hiệu lực do thuộc tính `'_permanent': True` và `Expires` tận năm 2058).   
• **Bước tiếp theo:** Mình thay mã session của `admin` vào `Cookie` và gửi request `GET /` (vào trang chủ) để lấy flag

![image.png](Old%20Sessions/image%204.png)

academy{s3t_s3ss10n_3xp1rat10n5_3fdcb5e2}