# JaWT Scratchpad

Bản chất & Ví dụ: - HS256: JWT ký bằng HMAC với secret chung.- Weak secret: Secret yếu có thể bị đoán bằng wordlist.- Resigning: Nếu biết secret, người dùng có thể tạo token mới hợp lệ.
Hệ sinh thái kiến thức: - JWT HS256- Weak secret- Wordlist cracking- Cookie token- Token resigning concept
Trạng thái: Chưa bắt đầu
Trạng thái 1: Chưa bắt đầu

![image.png](JaWT%20Scratchpad/image.png)

Với bài này tên bài JaWT cũng đã gợi ý lỗ hổng là jwt cho chúng ta rồi 

![image.png](JaWT%20Scratchpad/image%201.png)

![image.png](JaWT%20Scratchpad/image%202.png)

Trang web có một form đăng nhập, yêu cầu nhập tên bất kỳ ngoại trừ `admin`, vì `admin` có một "special scratchpad". Phía dưới có gợi ý dùng tên ngắn gọn như `John` (link trỏ tới công cụ John the Ripper).   Sau khi nhập tên `duc`, trang web hiển thị thông báo "Hello duc!" và cung cấp một ô văn bản (scratchpad). Đến đây chúng ta có vẻ sẽ phải đăng nhập với tư cách admin thì mới lấy được flag

![image.png](JaWT%20Scratchpad/image%203.png)

Công cụ John the Ripper là 1 công cụ chuyên dùng để crack password và dò tìm các loại mã băm 

![image.png](JaWT%20Scratchpad/image%204.png)

Kiểm tra request trong Burp Suite, mình phát hiện trình duyệt gửi đi một `Cookie` có tên là `jwt` chứa chuỗi token.  Mình sẽ copy chuỗi JWT này và đem đi giải mã (có thể dùng trang jwt.io) để xem cấu trúc dữ liệu (Header và Payload) bên trong.

![image.png](JaWT%20Scratchpad/image%205.png)

Giải mã token trên trang jwt.io, mình thấy thuật toán được sử dụng ở Header là `HS256` và Payload xác thực người dùng bằng trường `"user": "duc"`.  HS256: Thuật toán này dùng chung duy nhất một Secret Key cho cả hai việc: tạo chữ ký và xác thực token.  Dựa vào gợi ý về `John` ở trang chủ trước đó, mình sẽ lưu chuỗi JWT này lại và sử dụng công cụ John the Ripper (với wordlist `rockyou.txt`) để bẻ khóa (crack) tìm Secret Key.

```python
➜  ~ echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZHVjIn0.-CxOXSk5sh8Tp3h2FHP_AbiMKoF5cGux1jWKZK-pY6Y" > jwt.txt
➜  ~ john jwt.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA256                                      Using default input encoding: UTF-8
Loaded 1 password hash (HMAC-SHA256 [password is key, SHA256 256/256 AVX2 8x])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
ilovepico        (?)
1g 0:00:00:01 DONE (2026-10-17 10:05) 0.6211g/s 4599Kp/s 4599Kc/s 4599KC/s iluve.p..ilovejesus789
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
➜  ~
```

- John the Ripper đã chạy xong và bẻ khóa thành công, tìm được Secret Key là `ilovepico`.
- Hướng làm tiếp theo: Mình sẽ mang Secret Key này quay lại trang jwt.io để tạo một token mới với phần payload là `{"user": "admin"}`.

![image.png](JaWT%20Scratchpad/image%206.png)

Mình đã tạo thành công token mới với payload `"user": "admin"` và nhập Secret Key `ilovepico` trên jwt.io

Mình sẽ thay đoạn cookie mới vào cookie cũ và gửi lại request

![image.png](JaWT%20Scratchpad/image%207.png)

Và mình đã lấy được flag: academy{jawt_was_just_what_you_thought_5f6b65b1}