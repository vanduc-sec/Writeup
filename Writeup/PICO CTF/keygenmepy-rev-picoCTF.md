# keygenmepy-rev-picoCTF

# Bài này cung cấp cho mình 1 file python

### 1. Điểm khởi đầu (Entry Point)

Khi bạn chạy file Python này, máy tính sẽ bỏ qua các hàm định nghĩa (như `def intro_trial():`, `def check_key():`...) và bắt đầu thực thi ở những dòng code không bị thụt lề ở tận cùng bên dưới:

```
# Enter main loop
ui_flow()

if jump_into_full:
    exec(full_version_code)
```

Code gọi hàm `ui_flow()`, bắt đầu mở giao diện cho người dùng.

### 2. Giao diện và Nhập liệu (UI Flow)

- Bên trong `ui_flow()`, nó gọi `intro_trial()` để in ra câu chào (có chứa tên `BENNETT`).
- Tiếp theo, nó đi vào một vòng lặp `while arcane_loop_trial:`, liên tục gọi `menu_trial()` để hiện các tùy chọn (a, b, c, d).
- Để giải bài này, luồng đi vào tùy chọn **(c) Enter License Key**, chương trình sẽ gọi hàm `enter_license()`.
- Hàm `enter_license()` yêu cầu bạn nhập một chuỗi khóa (license key) và đẩy chuỗi đó vào hàm `check_key()` để kiểm tra xem đúng hay sai.

### 3. Trái tim của thử thách: Hàm `check_key()`

Đây là nơi giấu logic tạo ra flag. Khi bạn phân tích hàm này, luồng kiểm tra diễn ra qua 3 lớp phòng ngự:

**Lớp 1: Kiểm tra độ dài**
Độ dài của key bạn nhập phải bằng chính xác độ dài của biến `key_full_template_trial` (tức là "picoCTF{1n_7h3_kk3y_of_xxxxxxx}").

**Lớp 2: Kiểm tra phần tĩnh (Static Part)**
Vòng lặp `for c in key_part_static1_trial:` sẽ kiểm tra từng ký tự đầu tiên của bạn xem có khớp với chuỗi `picoCTF{1n_7h3_kk3y_of_` hay không.

**Lớp 3: Kiểm tra phần động (Dynamic Part) - Nơi bạn tìm ra flag**
Đây là mấu chốt của mảng Reverse. 8 ký tự tiếp theo không được code sẵn mà được tính toán trực tiếp thông qua hàm băm (hash) SHA-256 của chữ **"BENNETT"** (biến `username_trial`). Code sẽ lấy mã băm này, chuyển thành dạng chuỗi hex (chữ và số), và nhặt ra các ký tự ở những vị trí (index) cụ thể để so sánh với key bạn nhập.

Cụ thể luồng code yêu cầu các vị trí sau của mã băm:

1. `hexdigest()[4]`
2. `hexdigest()[5]`
3. `hexdigest()[3]`
4. `hexdigest()[6]`
5. `hexdigest()[2]`
6. `hexdigest()[7]`
7. `hexdigest()[1]`
8. `hexdigest()[8]`

Đó là lý do bạn giải được flag bằng cách tự chạy lệnh băm chữ "BENNETT" ra SHA-256 và ghép các ký tự ở các vị trí 4, 5, 3, 6, 2, 7, 1, 8 lại, sau đó đóng ngoặc `}`.

### 4. Phần thưởng: Hàm `decrypt_full_version()`

Nếu hàm `check_key()` trả về `True` (bạn nhập đúng flag), luồng code nhảy tiếp vào `decrypt_full_version()`.

- Nó lấy chính cái flag bạn vừa nhập, biến thành một dạng khóa mã hóa Base64.
- Nó sử dụng thư viện **Fernet** (một chuẩn mã hóa đối xứng của Python) cùng với chìa khóa trên để giải mã đoạn văn bản rối rắm `b"""gAAAAABpRaL..."""` ở cuối file.
- Nó tạo ra một file mới tên là `keygenme.py`, ghi đoạn code bản full (đã được giải mã) vào đó.
- Cuối cùng, vòng lặp dừng lại, biến `jump_into_full = True`, hàm `exec(full_version_code)` ở cuối cùng được kích hoạt và chạy thẳng đoạn code xịn bạn vừa giải mã ra.

để giải bài này thì mình sẽ chỉ tập trung vào hàm check_key thôi ở đây t thiếu là phần động, để giải được thì chúng ta chỉ cần chỉnh sửa 1 chút để nó in ra các kí tự tương ứng với vị trí băm là xong 

```python
import hashlib
username_trial = "BENNETT"
busername_trial = b"BENNETT"

key_part_static1_trial = "picoCTF{1n_7h3_kk3y_of_"
key_part_dynamic1_trial = "xxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
def check_key():
        print(hashlib.sha256(busername_trial).hexdigest()[4])            
        print(hashlib.sha256(busername_trial).hexdigest()[5])          
        print(hashlib.sha256(busername_trial).hexdigest()[3])          
        print(hashlib.sha256(busername_trial).hexdigest()[6])         
        print(hashlib.sha256(busername_trial).hexdigest()[2])            
        print(hashlib.sha256(busername_trial).hexdigest()[7])            
        print(hashlib.sha256(busername_trial).hexdigest()[1])           
        print(hashlib.sha256(busername_trial).hexdigest()[8])
check_key()
```
