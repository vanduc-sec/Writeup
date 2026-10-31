# Irish-Name-Repo 3

![image.png](Irish-Name-Repo%203/image.png)

![image.png](Irish-Name-Repo%203/image%201.png)

Đối với bài `**Irish-Name-Repo 3`** này thì mọi người có thể thấy giao diện vẫn giống hệt 2 bài trước đó những trong trang `Admin Login` đã có sự thay đổi

![image.png](Irish-Name-Repo%203/image%202.png)

Ở đây nó bắt mình phải truy cập vào tài khoản admin và chỉ có ô nhập mật khẩu mà thôi 

![image.png](Irish-Name-Repo%203/image%203.png)

Mình mở  burpsuite lên quan sát một chút, ở đây mọi người có thể thấy mặc dùng ko còn `username` nhưng mà bản chất lỗi ở `debug=0` vẫn còn mình sẽ thử thay đổi giá trị debug

![image.png](Irish-Name-Repo%203/image%204.png)

Sau khi thay đổi thì trong phản hồi mình đã thấy lộ ra truy vấn `sql` , nhưng có một điểm đặc biệt ở đây là rõ ràng mật khẩu mình nhập vào là `‘admin’` nhưng lúc nó truyền vào câu truy vấn sql thì lại bị biến đổi thành `‘nqzva’` , sau khi quan sát 1 lúc thì mình thấy là các kí tự có vẻ như là đã bị dịch chuyển lên 13 kí tự hay thường được gọi là `ROT13` 

**Áp dụng vào chuỗi `admin`:**

- `a` (97) + 13 = 110 ➞ **`n`**
- `d` (100) + 13 = 113 ➞ **`q`**
- `m` (109) + 13 = 122 ➞ **`z`**
- `i` (105) + 13 = 118 ➞ **`v`**
- `n` (110) + 13 = 123 ➞ Vượt quá 122, xoay vòng (123 - 26 = 97) ➞ **`a`**

Ở đây giả sử mình sẽ thử `payload sql injection` và `thử viết hoa`  xem nó bị biến đổi ra sao `payload` này sẽ làm cho mệnh đề `where` luôn đúng 

```sql
ADMIN'OR 1=1--
```

![image.png](Irish-Name-Repo%203/image%205.png)

Như mọi người thấy các chữ cái sẽ mặc định bị biến đổi còn lại số hay kí tự khác thì không sao

Mục tiêu của mình là làm sao sẽ có `payload` chuẩn truyền vào truy vấn đơn giản là mình sẽ lấy `payload` của mình trừ ngược lại cho 13 là được 

Chuỗi `or` ➞ dịch 13 ký tự ➞ `be` 

```sql
'be 1=1--
```

![image.png](Irish-Name-Repo%203/image%206.png)

Ok mình đã thành công `bytepass` và lấy được flag

academy{3v3n_m0r3_SQL_7d1b96d3}