# suspicious threat-htb

![image.png](suspicious%20threat-htb/image.png)

Bài này nó bắt chúng ta thực hiện kết nối với máy chủ từ xa

![image.png](suspicious%20threat-htb/image%201.png)

Theo mô tả đề bài thì bài này có vẻ như sẽ liên quan đến thư viện gì đó bị làm sao

Nên hướng tiếp theo mình sẽ phân tích bằng cách liệt kê các thư viện liên kết động bằng 1 số lệnh như sau:

```python
ldd /bin/ls
```

![image.png](suspicious%20threat-htb/image%202.png)

Thông thường ls sẽ phụ thuộc vào:

- libc.so.6
- libselinux.so.1
- libpcre2-8.so.0
- loader ld-linux

Nhưng ở đây lại có thêm:

- **libc.hook.so.6**

Tên này rất lạ:

- không phải thư viện chuẩn của hệ
- có chữ **hook**
- lại được nạp **trước** cả libc.so.6

Đây là dấu hiệu rất mạnh của một thư viện được chèn vào để:

- hook hàm
- sửa hành vi chương trình
- ẩn file/thư mục/process

Trong challenge này, đó chính là **userland rootkit**.

Tiếp theo mình sẽ sử  dụng 

```python
cat /etc/ld.so.preload
```

để xem có ai đó chèn thư viện vào chương trình không

![image.png](suspicious%20threat-htb/image%203.png)

Đến đây mọi người sẽ thấy thư viện đang người chúng ta vừa tìm thấy đã bị chèn vào

Tiếp theo để vô hiệu hóa việc nap vào preload như này thì mình sẽ di chuyển cái thư viện này ra chỗ khác 

```python
mv /lib/x86_64-linux-gnu/libc.hook.so.6 ./
```

Tiếp đến là mình có liệt kê 1 số thư mục đặc biệt thì phăt hiện

![image.png](suspicious%20threat-htb/image%204.png)

có 1 thư mục tên pr3… khá là đáng nghi nên mình sẽ thử liệt kê sâu hơn thư mục này xem sao

![image.png](suspicious%20threat-htb/image%205.png)

Đến đây thì mọi người thấy ngay là có 1 file flag.txt nên chúng ta se đọc nó

![image.png](suspicious%20threat-htb/image%206.png)

HTB{Us3rL4nd_R00tK1t_R3m0v3dd!}
