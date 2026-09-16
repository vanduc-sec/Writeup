# patchme.py-rev-picoCTF

### 1. Phân tích luồng Code (Execution Flow)

Chương trình sẽ chạy theo thứ tự từ trên xuống dưới như sau:

1. **Định nghĩa hàm `str_xor(secret, key)`:** Máy tính nạp vào bộ nhớ một hàm có chức năng mã hóa/giải mã bằng phép toán XOR.
2. **Đọc file `flag.txt.enc`:** Chương trình mở một file chứa cờ bị mã hóa bằng chế độ **`rb`** (đọc byte thô nguyên bản) và lưu toàn bộ dữ liệu vào biến `flag_enc`.
3. **Định nghĩa hàm `level_1_pw_check()`:** Khai báo một hàm yêu cầu người dùng nhập mật khẩu, kiểm tra mật khẩu đó, nếu đúng thì tiến hành giải mã cờ.
4. **Thực thi:** Gọi hàm `level_1_pw_check()` để bắt đầu tương tác với người dùng.

### 2. Phân tích các "Bẫy" và Logic giải mã

Tác giả để một dòng comment in hoa rất to:
`### THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG --LT ###` *(Hàm này sẽ không giúp bạn tìm được cờ đâu)*.

Nhưng nếu bạn nhìn xuống hàm `level_1_pw_check()`, khi bạn nhập đúng mật khẩu, chương trình lại dùng chính xác lệnh `decryption = str_xor(...)` để giải mã. **B**

#### B. Lỗ hổng "Hardcoded Password" (Mật khẩu được nhúng thẳng vào code)

Chương trình yêu cầu bạn nhập mật khẩu, nhưng nó lại để tơ hơ cái mật khẩu đúng ngay trong mã nguồn. Tác giả chỉ cố gắng làm rối mắt một chút bằng cách chia nhỏ chuỗi ra thành nhiều phần nối với nhau bằng dấu `+`:

Python

```
"ak98" + "-=90" + "adfjhgj321" + "sleuth9000"
```

Thực chất, máy tính sẽ tự động ghép chúng lại thành một chuỗi duy nhất: **`ak98-=90adfjhgj321sleuth9000`**

#### C. Sự xuất hiện của `rb` và `.decode()`

Như đã giải thích ở phần trước, file `flag.txt.enc` được đọc bằng `rb`, nên biến `flag_enc` đang chứa **byte thô** (raw bytes).
Nhưng hàm `str_xor` lại được viết để xử lý **chuỗi văn bản (string)**. Do đó, tác giả phải dùng lệnh `flag_enc.decode()` để "phiên dịch" cục byte thô đó thành chuỗi text bình thường trước khi ném vào hàm giải mã.

### 3. Thuật toán mã hóa XOR (`str_xor`)

Hàm `str_xor` sử dụng phép toán XOR (`^`), một phép toán xương sống trong bộ môn Cryptography (Mật mã học).
Đặc tính kỳ diệu nhất của XOR là **tính thuận nghịch**.

- Nếu bạn lấy `Văn bản gốc` XOR với `Chìa khóa` -> Ra `Văn bản mã hóa`.
- Nếu bạn lấy `Văn bản mã hóa` XOR lại với chính `Chìa khóa` đó -> Trở về `Văn bản gốc`.

Trong bài này, `secret` chính là cờ bị mã hóa (`flag_enc.decode()`), còn `key` là chữ `"utilitarian"`. Hàm này kéo dài chìa khóa ra cho bằng với độ dài của cờ, sau đó lấy từng ký tự chập (XOR) vào nhau để nhả ra cờ gốc.

### 4. Cách lấy cờ (Flag)

**Chơi đúng luật (Nhập mật khẩu)**
Chạy chương trình này bằng terminal/cmd. Khi nó hiện dòng chữ `Please enter correct password for flag:` , bạn chỉ cần copy chuỗi mật khẩu đã được ghép nối hoàn chỉnh dán vào và nhấn Enter:

Plaintext

```
ak98-=90adfjhgj321sleuth9000
```
