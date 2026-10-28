# More SQLi

![image.png](More%20SQLi/image.png)

![image.png](More%20SQLi/image%201.png)

Truy cập trang web nó bắt mình phải đăng nhập, mình sẽ thử  1 `username` và `password` nào đó

![image.png](More%20SQLi/image%202.png)

Sau khi nhập `username` và `pass` thì ta thấy nó in ra luôn cho mình câu `sql query` được sử dụng để kiểm tra đầu vào mà chúng ta đã nhập, giờ mình sẽ thử dùng `sql injection` để `bytepass`

Mình sẽ chèn payload vào trường username 

```python
'or 1=1-- 
```

![image.png](More%20SQLi/image%203.png)

Mọi người có thể thấy mình đã không thành công, nhưng mà mọi người hãy để ý rằng câu query này của người có điểm rất lạ là bình thường thì ta sẽ dùng `WHERE username = 'ad' AND password = 'ad'` nhưng trong bài này nó đã bị đảo ngược`WHERE password = 'ad' AND username = 'ad'` 

![image.png](More%20SQLi/image%204.png)

Mình đã thay đổi `payload` xuống trường `password` thì đã đăng nhập thành công mặc dù theo mình thì khi ta nhập `payload` vào `username` hay `password` thì mệnh đề `where` sẽ luôn đúng dù `username` hay `password` có bị đổi thứ tự cho nhau và chúng ta đều phải login được nhưng mà có thể do phía backend có logic xử lí khác, thật may mắn vì mình cũng đã dù flag sau 1 thời gian khá lâu mặc kẹt ở nhét `payload` vào `username`

Flag: academy{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_eb64a27a}