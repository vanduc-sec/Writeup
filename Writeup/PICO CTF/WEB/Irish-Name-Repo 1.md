# Irish-Name-Repo 1

![image.png](Irish-Name-Repo%201/image.png)

![image.png](Irish-Name-Repo%201/image%201.png)

Truy cập vào web ta thấy danh sách người Irish cùng với 2 trang `Support` và `Admin Login`

Trang đầu không có gì nên mình sẽ thử chuyển sang trang `Support`

![image.png](Irish-Name-Repo%201/image%202.png)

Ở trang này mọi người có thể thấy có nhắc đến lỗi thêm người bằng `sql` và mọi người đều được phản hồi từ `admin`

![image.png](Irish-Name-Repo%201/image%203.png)

Tiếp đến trang `Admin login` thình sẽ dùng burp để kiểm tra quá trình đăng nhập 

![image.png](Irish-Name-Repo%201/image%204.png)

Ở đây trong gói tin `POST /login.php` mình thấy 1 biến `debug=0` khá lạ ở đây

Có vẻ như biến này được dùng cho quá trình gỡ lỗi vậy nên nếu giờ mình  thay đổi giá trị 0 thành 1 để chuyển sang gỡ lỗi thì sao

![image.png](Irish-Name-Repo%201/image%205.png)

Chúng ta thấy trong gói tin trả về đã khác trước nó có thêm cả câu truy vấn sql kèm theo giờ mình sẽ khai thác bằng `sql injection` 

Như chúng ta đã biết đây là trang đăng nhập `admin` cùng với đó trong `support` ta cũng thấy có `admin` nên mình nghĩ trong cơ sở dữ liệu sẽ có người dùng admin nên giờ mình sẽ thử đăng nhập bằng người dùng `admin` kết hợp với `sql injection`

Payload:

```sql
admin'-- 
```

![image.png](Irish-Name-Repo%201/image%206.png)

Mình đã truy cập thành công và lấy được flag 

academy{s0m3_SQL_c090aeb0}