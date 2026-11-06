# It is my Birthday

![image.png](It%20is%20my%20Birthday/image.png)

Đọc đề bài có vẻ như là nó đang minh họa về 1 điểm yếu của mã băm md5 về khả năng chống va chạm

Chống va chạm tức là khi ta có:

```sql
file(a) ≠ file(b) → md5(a) ≠md5(b)
```

Tuy nhiên md5 lại không đảm bảo được điều đó

![image.png](It%20is%20my%20Birthday/image%201.png)

Nhìn vào trang web có vẻ như muốn chúng ta hãy tải lên 2 file pdf khác nhau nhưng có cùng md5 rồi 

[md5-1.pdf](It%20is%20my%20Birthday/md5-1.pdf)

[md5-2.pdf](It%20is%20my%20Birthday/md5-2.pdf)

Ở đây mình đã lấy luôn 2 file pdf có cùng md5 của dự án [https://github.com/corkami/collisions/tree/master/examples/free](https://github.com/corkami/collisions/tree/master/examples/free)

Giờ mình sẽ tải nó lên web

![image.png](It%20is%20my%20Birthday/image%202.png)

Mình đã lấy được flag 

academy{c0ngr4ts_u_r_1nv1t3d_44f9d0a}