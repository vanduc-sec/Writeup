# Web Gauntlet

![image.png](Web%20Gauntlet/image.png)

![image.png](Web%20Gauntlet/image%201.png)

![image.png](Web%20Gauntlet/image%202.png)

Bài này cung cấp cho mình 2 link 1 cái là đến trang đăng nhập và yêu cầu đăng nhập bằng admin và 1 trang còn lại là có vẻ như là cung cấp cho chúng ta biết round này đăng chặn cái gì

![image.png](Web%20Gauntlet/image%203.png)

Đầu tiên thì mình kiểm tra xem web có bị lỗ hổng `sql injection` không và câu trả lời là có, chúng ta còn thấy được cả câu truy vấn 

![image.png](Web%20Gauntlet/image%204.png)

`Payload:`

```sql
admin'-- 
```

Này là mình biến cho mệnh đề `where` để chỉ kiểm tra đúng `username` là `admin` thôi mà không kiểm tra `password`

![image.png](Web%20Gauntlet/image%205.png)

Đến round 2 mọi người load lại trang `/filter.php` là sẽ thấy lần này sẽ chặn thêm `comment ‘--’` rồi, nhưng mà ở `sqllite` thì còn một cách nữa để `comment` đó chính là dùng `‘/*’`, áp dụng vào bài 

```sql
admin'/*
```

![image.png](Web%20Gauntlet/image%206.png)

Mình đến được round 3 rồi tiếp là load lại trang `filter.php` 

![image.png](Web%20Gauntlet/image%207.png)

Lần này thì nó chặn thêm 1 số thứ nhưng mà có vẻ như payload trước đó của mình không bị filter nên mình sẽ nhập lại payload trước đó ở round 2

![image.png](Web%20Gauntlet/image%208.png)

Qua đến round 4 rồi 

![image.png](Web%20Gauntlet/image%209.png)

Lần này thì nó chặn luôn `username admi`n không cho mình nhập chuỗi `admin` vào nữa ở đây để tiếp tục thì mình sẽ dùng `'||'` để nối chuỗi

```sql
admi'||'n'/*
```

![image.png](Web%20Gauntlet/image%2010.png)

Mình đã đến round cuối cùng rồi 

![image.png](Web%20Gauntlet/image%2011.png)

Có vẻ lại giống như 1 round trước đó vì lần này nó chặn thêm `‘union’` nhưng mà payload trước đó mình không hề dùng đến câu lệnh này vì vậy mình sẽ tiếp tục dùng lại `payload` ở round 4

![image.png](Web%20Gauntlet/image%2012.png)

Nó yêu cầu mình qua `filter.php` để kiểm tra 

![image.png](Web%20Gauntlet/image%2013.png)

Mình qua filter.php load lại và đã thấy flag cũng như code mà web dùng để chặn các đầu vào mà mình nhập