# XXE Infiltration Lab-cyberdefen

Identifying the open ports discovered by an attacker helps us understand which services are exposed and potentially vulnerable. Can you identify the highest-numbered port that is open on the victim's web server?

**1. Phân tích (Analysis)**

- Dựa vào traffic, có thể thấy kẻ tấn công đang thực hiện kỹ thuật **TCP SYN Scan** (Half-open scan) để dò tìm các dịch vụ đang chạy.
- **Dấu hiệu nhận biết:** Khi kẻ tấn công gửi gói tin `SYN`, nếu port đích trên server **đang mở**, server sẽ phản hồi bằng gói **`SYN-ACK`**. Nếu port đóng, nó sẽ trả về cờ `RST`.
- **Hướng giải quyết:** Ta chỉ cần lọc các gói tin trả về chứa cờ `SYN-ACK` để liệt kê các port đang mở, sau đó tìm số lớn nhất.

**2. Các bước thực hiện (Steps)**

- **Bước 1:** Sử dụng cú pháp filter sau trên Wireshark để chỉ giữ lại các gói `SYN-ACK`:Plaintext
    
    ```
    tcp.flags.syn == 1 && tcp.flags.ack == 1
    ```
    
- **Bước 2:** Ở khung Packet Details (phía dưới), tìm trường `Source Port` (chính là port của server). Click chuột phải vào nó và chọn **Apply as Column** để biến nó thành một cột dễ nhìn trên giao diện chính.
- **Bước 3:** Click vào tiêu đề cột `Source Port` vừa tạo để sắp xếp các port theo thứ tự giảm dần. Đọc giá trị trên cùng.

**3. Kết quả (Answer)**

- Port có số thứ tự lớn nhất phản hồi gói `SYN-ACK` là **3306** (Dịch vụ MySQL).
- **Flag / Answer:** `3306`

**y identifying the vulnerable PHP script, security teams can directly address and mitigate the vulnerability. What's the complete URI of the PHP script vulnerable to XXE Injection?**

#### Q2: Identifying the Vulnerable Script

**Câu hỏi:** Xác định đường dẫn đầy đủ (Complete URI) của file PHP chứa lỗ hổng XXE Injection.

**1. Phân tích (Analysis)**

- Lỗ hổng XXE thường xảy ra khi người dùng tải lên hoặc gửi dữ liệu dạng XML để server xử lý.
- Để gửi file hoặc dữ liệu lên server, giao thức HTTP thường sử dụng phương thức **POST**. Do đó, ta cần lọc các gói tin HTTP POST để tìm ra file mã nguồn nào đang tiếp nhận dữ liệu này.

**2. Các bước thực hiện (Steps)**

- **Bước 1:** Trong Wireshark, áp dụng filter sau để chỉ hiển thị các request gửi dữ liệu lên server:Plaintext
    
    ```
    http.request.method == "POST"
    ```
    
- **Bước 2:** Click chuột phải vào một gói tin POST khả nghi (như hình trên), chọn **Follow -> HTTP Stream** để xem toàn bộ nội dung cuộc giao tiếp giữa Client và Server.
- **Bước 3:** Phân tích nội dung Stream:
    - Ta thấy một request gửi (upload) file tên là `ToKillaMockingbird.xml` lên server.
    - Trong nội dung file XML có chứa payload độc hại: `<!ENTITY xxe SYSTEM "file:///var/www/html/config.php">`.
    - Dòng đầu tiên của request chỉ ra file đích đang nhận payload này là: `POST /review/upload.php`.
    - Trường `Host` hiển thị domain là: `pageturner4books.net`.

**3. Kết quả (Answer)**

- File script nhận và xử lý file XML yếu kém là `upload.php`. Ghép đường dẫn gốc (Host) với đường dẫn file (Path), ta có URI hoàn chỉnh.
- **Flag / Answer:** `[http://pageturner4books.net/review/upload.php](http://pageturner4books.net/review/upload.php)`

#### Q3: Initial Point of Compromise

**Câu hỏi:** Tên của file XML độc hại đầu tiên mà kẻ tấn công tải lên là gì?

**1. Phân tích (Analysis)**

- Trong các cuộc tấn công XXE, tin tặc thường bắt đầu bằng cách dò đường (reconnaissance). Chúng sẽ cố gắng đọc các file hệ thống mặc định và phổ biến (như `/etc/passwd` trên Linux) để kiểm tra xem Server có thực sự dính lỗi hay không trước khi tiến hành các bước sâu hơn.

**2. Các bước thực hiện (Steps)**

- Tiếp tục sử dụng filter `http.request.method == "POST"` để lọc các gói tin upload dữ liệu.
- Theo dõi HTTP Stream của gói tin POST đầu tiên gửi đến `/review/upload.php`.
- Phân tích dữ liệu, ta thấy kẻ tấn công tải lên một file XML chứa payload `<!ENTITY xxe SYSTEM "file:///etc/passwd">`.
- Tên của file này được định nghĩa ở mục `filename` trong gói tin HTTP chính là **`TheGreatGatsby.xml`**.

#### Q4: Identifying Accessed Sensitive Files

**Câu hỏi:** Tên file cấu hình ứng dụng web (config file) mà kẻ tấn công đã đọc trộm được là gì?

**1. Phân tích (Analysis)**

- Sau khi thử nghiệm thành công ở Q3, kẻ tấn công bắt đầu nhắm tới các file chứa thông tin nhạy cảm hơn để leo thang đặc quyền. Các ứng dụng web PHP thường lưu thông tin kết nối Cơ sở dữ liệu, API keys ở các file cấu hình.

**2. Các bước thực hiện (Steps)**

- Kiểm tra HTTP Stream của các request tải file XML tiếp theo.
- Ta phát hiện kẻ tấn công đã tải lên một file có tên `ToKillAMockingbird.xml`.
- Payload bên trong file này chứa đường dẫn tuyệt đối trỏ tới: `/var/www/html/config.php`.
- Server phản hồi lại toàn bộ nội dung của file này. Tên file bị lộ chính là **`config.php`**.

#### Q5: Assessing the Breach Scope

**Câu hỏi:** Mật khẩu của tài khoản Database bị lộ là gì?

**1. Phân tích (Analysis)**

- Đây là hậu quả trực tiếp của Q4. File `config.php` thường chứa mã nguồn khai báo các hằng số hoặc biến kết nối đến MySQL.

**2. Các bước thực hiện (Steps)**

- Đọc phần Body của gói tin HTTP Response (Mã 200 OK) mà Server trả về sau khi nhận file `ToKillAMockingbird.xml`.
- Nội dung file cấu hình bị phơi bày dạng plaintext (chưa mã hóa). Ta thấy thông số cấu hình: `$db_user = 'pageturner'` và `$db_pass = 'Winter2024'`.
- Vậy mật khẩu Database bị lộ là **`Winter2024`**.

#### Q6: Database Compromise Timeline

**Câu hỏi:** Mốc thời gian (timestamp) lần kết nối đầu tiên của kẻ tấn công vào server MySQL bằng thông tin đánh cắp được là khi nào?

**1. Phân tích (Analysis)**

- Khi đã có tài khoản và mật khẩu, kẻ tấn công không cần thông qua lỗ hổng web nữa. Chúng dùng công cụ kết nối thẳng vào cổng dịch vụ MySQL (thường là port 3306) để thao tác trực tiếp với dữ liệu.

**2. Các bước thực hiện (Steps)**

- Sử dụng cú pháp filter `mysql.login_request` trong Wireshark để chỉ giữ lại các gói tin mang cờ yêu cầu xác thực đăng nhập MySQL.
- Tìm gói tin đầu tiên xuất phát từ IP của kẻ tấn công (source port: 44984) gửi đến IP của Server (port: 3306).
- Kiểm tra metadata của gói tin này (Sequence number: 88348), cột Time hiển thị thời điểm chính xác là **`2024-05-31 12:08`**.

#### Q7: Identifying the Web Shell

**Câu hỏi:** Tên của Web shell (công cụ điều khiển từ xa) mà kẻ tấn công đã tải lên để duy trì quyền truy cập là gì?

**1. Phân tích (Analysis)**

- Web shell là kịch bản độc hại cho phép kẻ tấn công thực thi lệnh hệ thống từ xa (RCE).
- Trong trường hợp này, kẻ tấn công dùng XXE kết hợp với tính năng **PHP Wrapper** (cụ thể là `php://filter/read=convert.base64-encode/...`) để lén lút kéo một file mã độc từ bên ngoài về và mã hóa nội dung bằng Base64 nhằm qua mặt các cơ chế bảo mật (như Firewall/IDS).

**2. Các bước thực hiện (Steps)**

- Phân tích tiếp các gói tin HTTP POST. Ta thấy kẻ tấn công tải lên file `PrideandPrejudice.xml`.
- Đọc nội dung file này, payload XXE định nghĩa một entity trỏ tới một địa chỉ IP từ xa của kẻ tấn công: `[http://203.0.113.15/booking.php](http://203.0.113.15/booking.php)`.
- Dựa vào đường dẫn này, ta xác định được tên của file web shell được chuẩn bị sẵn chính là **`booking.php`**.
