# 31

Bản chất & Ví dụ: - Path traversal: Dùng đường dẫn để thoát khỏi thư mục cho phép.- ../: Nghĩa là đi lên một cấp thư mục.- Directory sandbox: Server phải chuẩn hóa path và chặn truy cập ngoài root.
Hệ sinh thái kiến thức: - Path traversal- ../- Absolute path- File read endpoint- Directory sandbox
Trạng thái: Chưa bắt đầu
Trạng thái 1: Chưa bắt đầu
Tên bài / Chủ đề: Forbidden Paths

![image.png](31/image.png)

Đây là 1 bài web theo như mình đọc miêu tả thì  khá giống `Path Traversal`, giờ mình sẽ mở web lên kiểm tra thử

![image.png](31/image%201.png)

Trang web này cho phép mình nhập tên file hiện có và nó sẽ đọc cho mình, mình sẽ thử đọc 1 file

![image.png](31/image%202.png)

Nó gọi đến hàm read.php để đọc file mà mình đã điền, có vẻ như file read.php sẽ nhận đối số của filename để tiến hành đọc file, đến đây mình tự hỏi sẽ ra sao nếu mình truyền vào đường dẫn đến file /flag.txt 

Nhưng vì các file đang được đọc này thì ở trong thư mục document root và trang web đã filter đường dẫn tuyệt đối nên để có thể truyền đường dẫn đến file flag.txt thì mình sẽ dùng 1 loại đường dẫn khác gọi là đường dẫn tương đối (relative path)

![image.png](31/image%203.png)

Sau khi thử thì mình đã có được flag luôn khá là ngon