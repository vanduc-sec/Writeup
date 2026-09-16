# half awake-utfctf

![image.png](Last%20Byte%20Standing-utfctf/image.png)

Bài này cung cấp cho mình 1 fiel pcap 

![image.png](Last%20Byte%20Standing-utfctf/image%201.png)

sau khi mở lên vào http stream thì mọi người sẽ thấy có 1 số gợi ý

Ba cái tên:

- alert.chunk
- chef.decode
- key.version

nhiều khả năng **không phải tên ngẫu nhiên**. Chúng đang gợi ý cho bạn các thao tác hoặc từ khóa cần nghĩ tới.

### alert.chunk

Gợi tới:

- dữ liệu bị chia thành **chunk**
- có thể phải ghép lại nhiều mảnh payload
- hoặc tìm trong traffic những phần dữ liệu kiểu chunked transfer

### chef.decode

Gợi tới:

- “chef” có thể là tên đánh lạc hướng
- nhưng trọng tâm là **decode**
- tức là có một lớp mã hóa/biến đổi nào đó chứ không phải đọc thô

### key.version

Gợi tới:

- có thể có **key**
- có thể có nhiều **version**
- hoặc phải chọn đúng biến thể / đúng phiên bản định dạng

Hai byte đầu `PK` thường là dấu hiệu của **ZIP format**.

Tiếp mọi người sẽ thấy trong file pcap có tls với khá nhiều gói tin lạ

![image.png](Last%20Byte%20Standing-utfctf/image%202.png)

Ở đây mọi người sẽ thấy có những gói tin rất giống với file zip vì có pk nên mình sẽ dùng tshark để tách nó ra 1 file để xem

```python
tshark -r half-awake.pcap -Y "frame.number==36" -T fields -e tcp.payload | tr -d ':\n' | xxd -r -p > 1.zip
```

![image.png](Last%20Byte%20Standing-utfctf/image%203.png)

Nhìn vào chỗ này có thể thấy ở các vị trí chẵn thì các ký tự là rác dạng rawbyte có vẻ như bị xor nhưng mà do biết format flag là utflag{} thì chúng ta có thể cắt vị trí chẵn ra và dùng thử brutce-force key xor tìm flag

```python

data = open("stage2.bin", "rb").read()
a = data[::2]
b = data[1::2]

print("A raw :", a)
print("B hex :", b.hex())

for key in range(256):
    dec = bytes(x ^ key for x in b)
    if len(dec) >= 3 and dec[:3] == b"tlg":
        print("KEY =", hex(key))
        print("B dec =", dec)
        out = bytearray()
        for i in range(max(len(a), len(dec))):
            if i < len(a):
                out.append(a[i])
            if i < len(dec):
                out.append(dec[i])
        print("FLAG? =", out.decode(errors="replace"))

```

![image.png](Last%20Byte%20Standing-utfctf/image%204.png)

flag: utflag{h4lf_aw4k3_s33_th3_pr0t0c0l_tr1ck}
