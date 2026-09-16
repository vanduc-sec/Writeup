# deadly arthropod-htb-med

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image.png)

Bài này cung cấp cho chúng ta 1 file pcap

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%201.png)

Trong Wireshark đang có:

- `Protocol: USB`, `USBHID`
- `GET DESCRIPTOR Request DEVICE`
- `GET DESCRIPTOR Request CONFIGURATION`
- `GET DESCRIPTOR Request STRING`
- `GET DESCRIPTOR Request HID Report`

Đây là chuỗi rất điển hình khi **host enumerate một thiết bị HID**.

HID = Human Interface Device, thường là:

- bàn phím
- chuột
- keypad
- thiết bị giả bàn phím kiểu Rubber Ducky / BadUSB

Ở dưới pane chi tiết còn thấy:

- `Device address: 12`
- `Endpoint: 0x00, Direction: OUT`
- `URB_CONTROL`
- `bRequest: GET DESCRIPTOR (6)`
- `bDescriptorType: DEVICE (0x01)`

=> nghĩa là **máy host đang gửi control request tới endpoint 0** để xin descriptor của thiết b

sau đó mình cso thấy hid là 6 byte đây thường là hid của bàn phím nên mình sẽ decode nó

```python
import subprocess

pcap = "deadly_arthropod.pcap"
dev  = "12"

cmd = [
    "tshark", "-r", pcap,
    "-Y", f"usb.device_address == {dev} && usbhid.data",
    "-T", "fields", "-e", "usbhid.data"
]

lines = subprocess.check_output(cmd, text=True).splitlines()

keys = {
    **{i+4:(chr(97+i), chr(65+i)) for i in range(26)},
    0x1e:("1","!"), 0x1f:("2","@"), 0x20:("3","#"), 0x21:("4","$"),
    0x22:("5","%"), 0x23:("6","^"), 0x24:("7","&"), 0x25:("8","*"),
    0x26:("9","("), 0x27:("0",")"),
    0x28:("\n","\n"), 0x2a:("[BS]","[BS]"), 0x2b:("\t","\t"), 0x2c:(" "," "),
    0x2d:("-","_"), 0x2e:("=","+"), 0x2f:("[","{"), 0x30:("]","}"),
    0x31:("\\","|"), 0x33:(";",":"), 0x34:("'",'"'), 0x35:("`","~"),
    0x36:(",", "<"), 0x37:(".", ">"), 0x38:("/", "?")
}

prev = set()
out = ""

for line in lines:
    data = bytes.fromhex(line.replace(":", ""))
    mod = data[0]
    cur = set(k for k in data[2:8] if k)

    for k in cur - prev:
        if k in keys:
            shift = mod & 0x22   # left/right shift
            ch = keys[k][1] if shift else keys[k][0]
            if ch == "[BS]":
                out = out[:-1]
            else:
                out += ch
        else:
            out += f"[{k:02x}]"

    prev = cur

print(out)
```

```python
  hackthebox python3 1.py
eks@hackthebox.eu
Th1sC0uldB3MyR3alP@ssw0rd
QK[50]_[4f].[50][50][50][50]H[4f]5[50][50]{_[50]I[4f][4f]ck[4f]'[4f][4f]b0[50][50][50][50][50][50][50][50][50]I[50][50][50][50]T[4f][4f]f[4f][4f][4f][4f][4f][4f]_[4f][4f][4f][4f][4f][4f]}[50].[50].[50][50][50][50]3[50][50][50][50][50][50][50][50]u[50][50]t_[4f][4f]a[50][50][50][50][50][50][50][50][50][50]B[4f][4f][4f][4f][4f][4f][4f][4f][4f][4f][4f][4f][4f][4f]t[4f]5[50][50][50]I[4f][4f][4f]_[4f][4f][4f][4f][4f]a[50][50][50][50][50][50]a[4f][4f][4f][4f][4f][4f]d[50][50][50][50]y[4f][4f][4f]r
➜  hackthebox   
```

Sau khi chạy xong thì mình cso tháy 2 dòng đầu ra text khá chuẩn rồi nhưng mà phần sau có vẻ hơi lạ 50 và 4f là các phín mũi tên dịch trái và phải có vẻ như bài này là học nhập 1 số kí tguwj xong dịch trái phải và nhập thêm các kí tự do đó khi mà mình decode theo text bình thường thì nó bị như vậy nên là mình sẽ cdoe lại 

Điều đó chứng tỏ người dùng không gõ thẳng một mạch. Họ:

- gõ một phần
- di chuyển con trỏ sang trái
- chèn thêm ký tự vào giữa
- di chuyển tiếp
- sửa vị trí khác

```python
import subprocess
import re

TSHARK = "tshark"
PCAP = "deadly_arthropod.pcap"
DEV = "12"

KEYS = {
    **{i + 0x04: (chr(97 + i), chr(65 + i)) for i in range(26)},
    0x1E: ("1", "!"), 0x1F: ("2", "@"), 0x20: ("3", "#"), 0x21: ("4", "$"),
    0x22: ("5", "%"), 0x23: ("6", "^"), 0x24: ("7", "&"), 0x25: ("8", "*"),
    0x26: ("9", "("), 0x27: ("0", ")"),
    0x28: ("<ENTER>", "<ENTER>"),
    0x2A: ("<BACKSPACE>", "<BACKSPACE>"),
    0x2C: (" ", " "),
    0x2D: ("-", "_"), 0x2E: ("=", "+"),
    0x2F: ("[", "{"), 0x30: ("]", "}"),
    0x31: ("\\", "|"),
    0x33: (";", ":"), 0x34: ("'", '"'),
    0x35: ("`", "~"),
    0x36: (",", "<"), 0x37: (".", ">"), 0x38: ("/", "?"),
    0x4C: ("<DELETE>", "<DELETE>"),
    0x4F: ("<RIGHT>", "<RIGHT>"),
    0x50: ("<LEFT>", "<LEFT>"),
    0x51: ("<DOWN>", "<DOWN>"),
    0x52: ("<UP>", "<UP>"),
}

def get_reports():
    cmd = [
        TSHARK, "-r", PCAP,
        "-Y", f"usb.device_address == {DEV} && usbhid.data",
        "-T", "fields", "-e", "usbhid.data"
    ]
    return subprocess.check_output(cmd, text=True).splitlines()

def hid_to_tokens(lines):
    prev = set()
    out = []

    for line in lines:
        data = bytes.fromhex(line.replace(":", "").strip())
        mod = data[0]
        shift = bool(mod & 0x22)
        cur = set(k for k in data[2:8] if k)

        for k in cur - prev:
            token = KEYS.get(k, (f"[{k:02x}]", f"[{k:02x}]"))[1 if shift else 0]
            out.append(token)

        prev = cur

    return out

def replay(tokens):
    buf = []
    cur = 0

    for t in tokens:
        if t == "<LEFT>":
            cur = max(0, cur - 1)
        elif t == "<RIGHT>":
            cur = min(len(buf), cur + 1)
        elif t == "<BACKSPACE>":
            if cur > 0:
                del buf[cur - 1]
                cur -= 1
        elif t == "<DELETE>":
            if cur < len(buf):
                del buf[cur]
        elif t == "<ENTER>":
            buf.insert(cur, "\n")
            cur += 1
        elif t.startswith("<") and t.endswith(">"):
            pass
        else:
            buf.insert(cur, t)
            cur += 1

    return "".join(buf)

lines = get_reports()
tokens = hid_to_tokens(lines)

print("===== TOKENS =====")
print("".join(tokens))
print("\n===== REPLAYED TEXT =====")
print(replay(tokens))
```

```python
➜  hackthebox python3 1.py
===== TOKENS =====
eks@hackthebox.eu<ENTER>Th1sC0uldB3MyR3alP@ssw0rd<ENTER>QK<LEFT>_<RIGHT>.<LEFT><LEFT><LEFT><LEFT>H<RIGHT>5<LEFT><LEFT>{_<LEFT>I<RIGHT><RIGHT>ck<RIGHT>'<RIGHT><RIGHT>b0<LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT>I<LEFT><LEFT><LEFT><LEFT>T<RIGHT><RIGHT>f<RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT>_<RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT>}<LEFT>.<LEFT>.<LEFT><LEFT><LEFT><LEFT>3<LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT>u<LEFT><LEFT>t_<RIGHT><RIGHT>a<LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT><LEFT>B<RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT>t<RIGHT>5<LEFT><LEFT><LEFT>I<RIGHT><RIGHT><RIGHT>_<RIGHT><RIGHT><RIGHT><RIGHT><RIGHT>a<LEFT><LEFT><LEFT><LEFT><LEFT><LEFT>a<RIGHT><RIGHT><RIGHT><RIGHT><RIGHT><RIGHT>d<LEFT><LEFT><LEFT><LEFT>y<RIGHT><RIGHT><RIGHT>r

===== REPLAYED TEXT =====
eks@hackthebox.eu
Th1sC0uldB3MyR3alP@ssw0rd
HTB{If_It_Quack5_It'5_a_K3yb0ard...}
➜  hackthebox
```

HTB{If_It_Quack5_It'5_a_K3yb0ard...}
