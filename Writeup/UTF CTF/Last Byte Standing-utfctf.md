# Last Byte Standing-utfctf

![image.png](Last%20Byte%20Standing-utfctf/image.png)

Bài này cung cấp cho chúng ta 1 file pcap 

## 1) **Last Byte Standing**

Tên đề thường là hint.

- **Last Byte** = “byte cuối cùng”
- **Standing** = “còn sót lại”, “đứng trơ ra”, “không bị chú ý”

Tên này gợi ý rất mạnh rằng:

- có thể có **1 byte cuối cùng bất thường**
- hoặc dữ liệu/flag nằm ở **phần cuối**
- hoặc có chuyện liên quan đến:
    - **trailing byte**
    - **padding**
    - **EOF marker**
    - **byte bị dư / thiếu / lệch**
    - **gói cuối cùng**
    - **fragment cuối**
    - **ký tự cuối trong payload**

![image.png](Last%20Byte%20Standing-utfctf/image%201.png)

Ở đây với giao thức http nó chỉ gửi 1 số file .js và nội dung không có gì đặc biệt 

có vẻ như nó chỉ là rác

![image.png](Last%20Byte%20Standing-utfctf/image%202.png)

tiếp theo mọi người sẽ nhìn vào giao thức dns ở mỗi dns.payload sẽ có byte dư thừa cuối thay đổi liên tục giữa 30 và 31 tức 0 1 đ

phần DNS payload là:

```
be ef 01 00 00 01 00 00 00 00 00 00
0a 73 79 6e 63 2d 63 61 63 68 65
0b 6e 65 78 74 68 6f 70 2d 6c 61 62
03 6e 65 74
00
00 01
00 01
31
```

Tách ra:

- be ef 01 00 00 01 00 00 00 00 00 00 = **DNS header** (12 byte)
- 0a ... 03 6e 65 74 00 = **QNAME** = sync-cache.nexthop-lab.net
- 00 01 = **QTYPE = A**
- 00 01 = **QCLASS = IN**
- 31 = **byte dư**, tức ký tự ASCII '1'

Bây giờ việc chúng ta là sẽ cắt phần byte dư này ra và check xem nếu nó là 30 thì chuyển thành 0 và in ra còn nếu là 31 thì chúng ta sẽ in nó ra là 1

```python
tshark -r last-byte-standing.pcap -Y 'dns.flags.response==0' -T fields -e udp.payload | \
awk '{b=substr($0,length($0)-1,2); if(b=="30") printf "0"; else if(b=="31") printf "1"} END{print ""}'
```

## 1) Phần tshark

```
tshark-r last-byte-standing.pcap
```

- tshark = bản command-line của Wireshark
- r last-byte-standing.pcap = đọc file pcap này, không bắt live

Tức là:

**“mở file pcap ra để duyệt từng packet”**

---

## 2) Phần filter DNS query

```
-Y'dns.flags.response==0'
```

- Y = display filter của Wireshark/tshark
- dns.flags.response==0 nghĩa là:
    - chỉ lấy packet DNS
    - và chỉ lấy **query**
    - không lấy response

Trong DNS:

- 0 = query
- 1 = response

Tức là đoạn này đang nói:

**“chỉ xét các gói DNS hỏi đi”**

---

## 3) Chỉ in ra UDP payload

```
-T fields-e udp.payload
```

- T fields = xuất theo kiểu field text
- e udp.payload = chỉ in trường udp.payload

Với packet DNS qua UDP, udp.payload chính là phần data DNS.

Ví dụ một dòng có thể in ra kiểu:

```
beef010000010000000000000a73796e632d63616368650b6e657874686f702d6c6162036e6574000001000131
```

Đây là **hex** của toàn bộ DNS payload.

Nó gồm:

```
[DNS header 12 byte][QNAME][00][QTYPE][QCLASS][byte dư]
```

Ở packet trong ảnh bạn gửi, byte cuối là:

```
31
```

tức ASCII của ký tự:

```
"1"
```

---

## 4) Dấu |

```
|awk ...
```

Dấu pipe nghĩa là:

- output của tshark
- được chuyển làm input cho awk

Tức là:

**mỗi dòng hex payload do tshark in ra sẽ được awk xử lý tiếp**

---

## 5) Phần awk

```
awk'{b=substr($0,length($0)-1,2); if(b=="30") printf "0"; else if(b=="31") printf "1"} END{print ""}'
```

awk xử lý **từng dòng một**.

---

### 5.1) $0

Trong awk:

- $0 = toàn bộ dòng hiện tại

Ví dụ dòng hiện tại là:

```
beef010000010000000000000a73796e632d63616368650b6e657874686f702d6c6162036e6574000001000131
```

thì $0 chính là chuỗi đó.

---

### 5.2) length($0)-1

```
length($0)-1
```

- length($0) = độ dài chuỗi hex hiện tại
- 1 để lùi về vị trí bắt đầu của **2 ký tự cuối**

Vì 1 byte hex được viết bằng 2 ký tự:

- 30
- 31

nên muốn lấy byte cuối thì phải lấy **2 ký tự cuối dòng**.

---

### 5.3) substr($0,length($0)-1,2)

```
b=substr($0,length($0)-1,2)
```

- substr(string, start, length)
- lấy từ chuỗi $0
- bắt đầu tại vị trí length($0)-1
- lấy 2 ký tự

Kết quả:

- nếu cuối dòng là ...31 thì b="31"
- nếu cuối dòng là ...30 thì b="30"

Tức là:

**đoạn này đang cắt đúng 1 byte cuối của UDP payload**

---

### 5.4) Vì sao là 30 và 31, không phải 0 và 1?

Vì udp.payload đang ở dạng **hex**, không phải text.

ASCII của:

- ký tự '0' là hex 30
- ký tự '1' là hex 31

Nên:

```
if(b=="30") printf "0";
else if(b=="31") printf "1";
```

nghĩa là:

- nếu byte cuối là ASCII '0' thì in 0
- nếu byte cuối là ASCII '1' thì in 1

---

### 5.5) Vì sao dùng printf chứ không dùng print?

- print "0" sẽ in 0 rồi xuống dòng
- printf "0" sẽ in 0 **không xuống dòng**

Nên lệnh này sẽ ghép các bit liền nhau thành:

```
0111010101110100...
```

chứ không phải:

```
0
1
1
1
0
...
```

---

### 5.6) END{print ""}

Sau khi awk xử lý xong tất cả dòng:

```
END{print ""}
```

mới in 1 dòng trống / xuống dòng cuối cùng.

Mục đích là để prompt terminal không bị dính ngay sau chuỗi bit.

Sau khi chạy xong mọi người sẽ nhận được mã nhị phân

![image.png](Last%20Byte%20Standing-utfctf/image%203.png)

```python
01110101011101000110011001101100011000010110011101111011011001000011000101100111010111110111010000110000010111110111010001101000001100110101111101101100001101000111001101110100010111110110001001111001011101000011001101111101010101011100001101010101110000110101010111000011010101011100001101010101110000110101010111000011001110100101011000111010010101100011101001010110001110100101011000111010010101100011101001010110001110100101011001010110
```

Sau đó mình lên cyber chef decode

![image.png](Last%20Byte%20Standing-utfctf/image%204.png)

flag: utflag{d1g_t0_th3_l4st_byt3}
