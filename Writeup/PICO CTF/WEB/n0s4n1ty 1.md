# n0s4n1ty 1

![image.png](n0s4n1ty%201/image.png)

Ở đây ta có thấy bài yêu cầu chúng ta vào thư mục /root thông qua lỗ hổng upload file 

![image.png](n0s4n1ty%201/image%201.png)

Sau khi upload xong 1 file ảnh thì mình thấy được đường dẫn đến file ảnh mình vừa upload  giờ mình sẽ thử truy cập vào ảnh xem được không 

![image.png](n0s4n1ty%201/image%202.png)

Có thể truy cập được, tiếp để khai thác thì mình sẽ thử upload 1 file payload php xem server có cho thực thi không

![image.png](n0s4n1ty%201/image%203.png)

Mình đã sửa extension của file thành .php và sửa nội dung file thành payload 

```python
<?php phpinfo() ?>
```

![image.png](n0s4n1ty%201/image%204.png)

Đến đây mình thấy trong gói tin trả về thì file thực thi của mình đã được chạy có vẻ như server không  có ngăn chặn gì về việc file người dùng tải lên 

![image.png](n0s4n1ty%201/image%205.png)

Tiếp mình sẽ thay đổi payload để tiến hành vào thư mục /root tìm flag 

![image.png](n0s4n1ty%201/image%206.png)

Mình đã có thể thực thi được payload và xem toàn bộ thư mục gốc rồi nhưng mà ở đây ta thấy toàn bộ các file đều thuộc quyền của người dùng root mình sẽ kiểm tra quyền đầu tiên bằng sudo -l

![image.png](n0s4n1ty%201/image%207.png)

Trong gói tin trả về dòng chữ `(ALL) NOPASSWD: ALL` ở cuối.  

 Ý nghĩa: Tài khoản `www-data` hiện tại được phép chạy bất kỳ lệnh nào dưới quyền root mà không cần mật khẩu, giờ thì mình chỉ việc dùng sudo để thực thi lệnh

![image.png](n0s4n1ty%201/image%208.png)

Ngay bây giờ ta có thể thấy trong thư mục root là có 1 file flag.txt chúng ta đọc và lấy flag thôi 

![image.png](n0s4n1ty%201/image%209.png)

academy{wh47_c4n_u_d0_wPHP_12aa2ff5}