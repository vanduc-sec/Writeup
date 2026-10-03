# Cookie Monster Secret Recipe

Bản chất & Ví dụ: - Cookie: Dữ liệu nhỏ browser gửi kèm request cùng domain.- Application tab: Nơi xem/sửa cookie, localStorage, sessionStorage.- Encoded cookie: Cookie có thể chỉ bị encode, không phải encrypted.
Hệ sinh thái kiến thức: - Browser cookie- Encoded cookie- DevTools Application- Base64/URL decode- Client storage
Trạng thái: Hoàn tất
Trạng thái 1: dễ ko wu

![image.png](Cooki%20Monster%20Secret%20Recipe/image.png)

Đầu tiên với bài này mình có thể thấy ngay đầu bài đã hint cho mình liên quan đến cookie.

![image.png](Cooki%20Monster%20Secret%20Recipe/image%201.png)

Ở đây là 1 giao diện đăng nhập mình sẽ nhập 1 tên đăng nhập và mật khẩu nào đó.

![image.png](Cooki%20Monster%20Secret%20Recipe/image%202.png)

Nhập xong nó sẽ trả về phản hồi từ chối quyền truy cập nhưng mà ở đây bên dưới nó còn kèm theo 1 hint nhắc mình kiểm tra cookie

![image.png](Cooki%20Monster%20Secret%20Recipe/image%203.png)

Sau đó thì mình vào burp follow theo gói POST /login.php thì có nhận thấy trong gói tin phản hồi trường cookie có chuỗi base64 

```python
➜  ~ echo "YWNhZGVteXtjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzXzM0RUYyQ0U4fQ" | base64 -d                                  
academy{c00k1e_m0nster_l0ves_c00kies_34EF2CE8}%                                                                         ➜  ~
```

Cuối cùng là decode và có được flag