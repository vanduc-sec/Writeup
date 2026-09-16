# the missing piece-dh-3

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

Bạn đang có:`disk_1.bin` (Disk1),`disk_3.bin` (Disk3), **mất Disk2**

Và hint: **RAID5 – Left Symmetric, Stripe size = 1 byte, XOR**

---

## 1) Với 3 disk + RAID5, mỗi “stripe” có 3 byte

Trong RAID5, mỗi stripe luôn có: **2 byte data+ 1 byte parity**

Và parity được tính:

> **P = D_a XOR D_b**
> 

Nếu mất 1 disk, ta khôi phục bằng:

> **Byte_mất = P XOR Byte_còn_lại**
> 

---

## 2) “Left Symmetric” với 3 disk: parity xoay vòng như sau

Với đúng layout bài này (khớp ra PNG), parity sẽ lặp theo chu kỳ 3 stripe:

- i % 3 == 0 → P ở Disk3
- i % 3 == 1 → P ở Disk2
- i % 3 == 2 → P ở Disk1

---

## 3) Ví dụ

Mình lấy 3 stripe đầu tiên từ disk_1.bin và disk_3.bin:

### Stripe i = 0 (0 % 3 = 0 → parity ở Disk3)

- Disk1[0] = 0x89
- Disk3[0] = 0xD9 (đây là **parity**)

Vậy Disk2[0] (bị mất) là:

- Disk2[0] = Parity XOR Disk1[0]
- Disk2[0] = 0xD9 XOR 0x89 = 0x50

0x50 chính là ký tự ASCII **'P'**.

➡️ **2 byte data xuất ra** ở stripe này là: Disk1[0] và Disk2[0]

→ 89 50  (tức \x89P)

---

### Stripe i = 1 (1 % 3 = 1 → parity ở Disk2, nhưng Disk2 đang mất)

- Disk1[1] = 0x4E (**'N'**)
- Disk3[1] = 0x47 (**'G'**)

Ở stripe này, Disk2 là parity (bị mất) nhưng **ta không cần parity để xuất data**, vì 2 data nằm ở Disk1 và Disk3.

➡️ **2 byte data xuất ra**: Disk1[1], Disk3[1]

→ 4E 47 (tức "NG")

---

### Stripe i = 2 (2 % 3 = 2 → parity ở Disk1)

- Disk1[2] = 0x07 (parity)
- Disk3[2] = 0x0A (data)

Disk2[2] (data bị mất):

- Disk2[2] = Parity XOR Disk3[2]
- Disk2[2] = 0x07 XOR 0x0A = 0x0D

➡️ **2 byte data xuất ra**: Disk2[2], Disk3[2]

→ 0D 0A (CR LF, tức \r\n)

---

## 4) Ghép 3 stripe đầu lại bạn sẽ thấy “PNG signature” xuất hiện

Ghép output theo đúng thứ tự stripe:

- Stripe 0 output: 89 50
- Stripe 1 output: 4E 47
- Stripe 2 output: 0D 0A

Tổng 8 byte đầu:

89 50 4E 47 0D 0A 1A 0A

→ chính là header chuẩn của PNG: **\x89PNG\r\n\x1a\n**

Vì vậy mình sẽ dùng code để xor dữ liệu

```python
#!/usr/bin/env python3
import sys

def xor(a: int, b: int) -> int:
    return a ^ b

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} disk_1.bin disk_3.bin out.png")
        sys.exit(1)

    p1, p3, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    d1 = open(p1, "rb").read()
    d3 = open(p3, "rb").read()

    if len(d1) != len(d3):
        raise SystemExit("disk sizes differ -> check inputs")

    out = bytearray()
    n = len(d1)

    for i in range(n):
        if i % 3 == 0:
            
            d2 = xor(d3[i], d1[i])
            out += bytes([d1[i], d2])
        elif i % 3 == 1:
           
            out += bytes([d1[i], d3[i]])
        else:
            
            d2 = xor(d1[i], d3[i])
            out += bytes([d2, d3[i]])

    with open(out_path, "wb") as f:
        f.write(out)

    print("[+] wrote:", out_path)
    print("[+] first 16 bytes:", out[:16].hex())

if __name__ == "__main__":
    main()

```

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%201.png)

sau khi chạy ngọi người sẽ nhận được 1 ảnh là png mở nó lên là sẽ có được flag

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%202.png)

DH{R4ID_5_R3c0v3ry_1s_Fun}
