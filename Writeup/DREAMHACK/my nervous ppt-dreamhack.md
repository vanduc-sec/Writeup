# my nervous ppt-dreamhack

![image.png](my%20nervous%20ppt-dreamhack/image.png)

- Bài này cung cấp cho chúng ta 1 file pcap mở nó nên các bạn sẽ thấy nó là giao thức usb

 

![image.png](my%20nervous%20ppt-dreamhack/image%201.png)

![image.png](my%20nervous%20ppt-dreamhack/image%202.png)

### 1. Giai đoạn thiết lập hệ thống (Enumeration)

- **Mục đích:** Host hỏi và Device trả lời để xác định danh tính thiết bị thông qua các gói tin **GET/SET DESCRIPTOR**.
- **Các thành phần chính:**
    - **Device Descriptor:** Chứa ID nhà sản xuất (Vendor) và sản phẩm (Product).
    - **Configuration Descriptor:** Chứa cấu trúc các Interface và Endpoint (điểm cuối truyền tin).
    - **SET CONFIGURATION:** Host chốt cấu hình để bắt đầu sử dụng thiết bị.

### 2. Giai đoạn truyền dữ liệu tương tác (HID/Interrupt)

- **Cơ chế Polling:** Host chủ động hỏi thiết bị theo chu kỳ (`bInterval`) thay vì thiết bị tự gửi dữ liệu.
- **Cấu trúc gói tin URB (USB Request Block):**
    - **URB_SUBMIT:** Host gửi yêu cầu đọc dữ liệu (gõ cửa hỏi).
    - **URB_COMPLETE:** Thiết bị trả lời, có kèm theo dữ liệu thực tế (như phím bấm hoặc di chuyển chuột) hoặc xác nhận trạng thái.

![image.png](my%20nervous%20ppt-dreamhack/image%203.png)

 HID là Keyboard/Presenter phổ biến, Input Report luôn 8 byte. Cấu trúc 8-byte dữ liệu HID (Keyboard)

- **Byte 0 (Modifier):** Dạng bitmask dùng để xác định các phím chức năng đang giữ (ví dụ: `0x02` là Left Shift).
- **Byte 1 (Reserved):** Mặc định là `0x00`.
- **Byte 2-7 (Keycodes):** Chứa tối đa 6 mã phím đang được nhấn đồng thời theo bảng mã HID.

### 2. Các trường hợp dữ liệu cụ thể phát hiện được

Dựa trên dữ liệu thực tế, tất cả các lần nhấn đều đi kèm phím **Left Shift** (`0x02`):

- **Trường hợp 1 (`0x52`):** Phím **Up Arrow** (Mũi tên lên).
- **Trường hợp 2 (`0x51`):** Phím **Down Arrow** (Mũi tên xuống).
- **Trường hợp 3 (`0x00`):** Chỉ giữ Shift, không nhấn thêm phím nào khác, ý tưởng của tôi là chuyển đổi chuỗi hành động nhấn phím (dài/ngắn hoặc lên/xuống) thành các ký tự Morse để giải mã ra nội dung cuối cùng.

![image.png](my%20nervous%20ppt-dreamhack/image%204.png)

- Sau khi dùng tshark tách ra thì mình sẽ thấy gói tin chứa mã 52 là - và gói tin chứa mã 51 là . và gói tin chứa mã 0 là dấu cách
- Đến đây chúng ta sẽ dùng code python để docode nó nhé chứ tshark kia chỉ là để xem chúng ta có đúng howngs ko thôi

 

```python
#!/usr/bin/env python3
import sys, struct, re

EPB_TYPE = 0x00000006  # Enhanced Packet Block

MORSE = {
 ".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E","..-.":"F","--.":"G","....":"H","..":"I",".---":"J",
 "-.-":"K",".-..":"L","--":"M","-.":"N","---":"O",".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T",
 "..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z",
 "-----":"0",".----":"1","..---":"2","...--":"3","....-":"4",".....":"5","-....":"6","--...":"7","---..":"8","----.":"9",
 ".-.-.-":".","--..--":",","..--..":"?","-.-.--":"!","-....-":"-","-..-.":"/",".--.-.":"@","-.--.":"(","-.--.-":")","..--.-":"_"
}

def read_pcapng_epbs(path):
    epbs = []
    data = open(path, "rb").read()
    pos, n = 0, len(data)
    while pos + 8 <= n:
        bt, bl = struct.unpack_from("<II", data, pos)
        if bl < 12 or pos + bl > n: break
        if bt == EPB_TYPE:
            # EPB fixed fields after type/len
            iface, ts_hi, ts_lo, cap_len, orig_len = struct.unpack_from("<IIIII", data, pos+8)
            pkt_start = pos + 8 + 20
            pkt_end   = pkt_start + cap_len
            if pkt_end <= pos + bl:
                epbs.append((ts_hi, ts_lo, data[pkt_start:pkt_end]))
        pos += bl
    return epbs

def decode_hid_candidates(pkt_bytes):
    """Scan for HID 8-byte report windows: [mod][res=0][k1..k6], >=1 key non-zero, small number of simultaneous keys."""
    cands = []
    L = len(pkt_bytes)
    for i in range(0, L-7):
        chunk = pkt_bytes[i:i+8]
        if chunk[1] != 0:  # reserved must be 0
            continue
        keys = chunk[2:]
        if not any(keys):
            continue
        # keep reports with up to 2 non-zero keys (reduce false positives)
        if sum(1 for k in keys if k != 0) > 2:
            continue
        cands.append(chunk)
    return cands

def keydown_events(epbs):
    """Emit key-down events (newly pressed HID codes) with timestamps."""
    prev_pressed = set()
    events = []
    for ts_hi, ts_lo, pkt in epbs:
        # Just scan raw payload for HID-like 8-byte windows
        for rep in decode_hid_candidates(pkt):
            mod = rep[0]
            keys = [k for k in rep[2:] if k != 0]
            cur  = set(keys)
            new_keys = [k for k in keys if k not in prev_pressed]
            t = ts_hi + ts_lo/1e9  # relative time ok
            for k in new_keys:
                events.append((t, k, mod))
            prev_pressed = cur
    return events

def decode_morse_from_arrows(events):
    """Use only UP/DOWN (0x52/0x51) with timestamps, infer unit timing, segment Morse, try two mappings."""
    # filter to arrows and sort by time
    arr = [(t, 'U' if k==0x52 else 'D') for (t,k,_) in events if k in (0x51,0x52)]
    arr.sort()
    if not arr: 
        return "", None, 0.05

    # build dt sequence
    seq = []
    for i,(t,sym) in enumerate(arr):
        dt = 0.0 if i==0 else max(0.0, t - arr[i-1][0])
        seq.append((sym, t, dt))

    # estimate unit from small non-zero gaps (10–40 percentile avg)
    nonzero = sorted([dt for _,_,dt in seq if dt>0])
    if nonzero:
        p10 = nonzero[int(0.10*len(nonzero))]
        p40 = nonzero[int(0.40*len(nonzero))]
        unit = (p10 + p40)/2 if p40>0 else (p10 or 0.05)
    else:
        unit = 0.05

    def decode_with(mapping_u_dot=True, intra=1.5, word=4.5):
        # mapping: True -> U='.', D='-'; False -> U='-', D='.'
        def gap(dt):
            if dt <= intra*unit: return 'intra'
            if dt <= word*unit:  return 'letter'
            return 'word'
        blocks, cur = [], []
        for i,(sym, _, dt) in enumerate(seq):
            ch = ('.' if mapping_u_dot else '-') if sym=='U' else ('-' if mapping_u_dot else '.')
            cur.append(ch)
            if i+1 < len(seq):
                g = gap(seq[i+1][2])
                if g=='letter': blocks.append("".join(cur)); cur=[]
                elif g=='word': blocks.append("".join(cur)); blocks.append(" "); cur=[]
        if cur: blocks.append("".join(cur))
        text = "".join(" " if b==" " else MORSE.get(b, "?") for b in blocks)
        return text, blocks

    # try both mappings; pick fewer '?' (tie-breaker: prefers 'KHK','LOOK','PPT','AT','MY')
    t1,_ = decode_with(mapping_u_dot=True)
    t2,_ = decode_with(mapping_u_dot=False)
    def score(tx): return -5*tx.count("?") + 3*tx.count("KHK") + 2*tx.count("LOOK") + 2*tx.count("PPT") + tx.count("AT") + tx.count("MY")
    best = (t1, True) if score(t1) >= score(t2) else (t2, False)
    return best[0], best[1], unit

def normalize_flag(text):
    # collapse spaces, map () -> {} then look for KHK{...}
    norm = "".join(text.split()).replace("(", "{").replace(")", "}")
    m = re.search(r"KHK\{[A-Z0-9_]+\}", norm.upper())
    return m.group(0) if m else None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 usb_presenter_morse_solver.py <file.pcapng>")
        sys.exit(1)

    epbs = read_pcapng_epbs(sys.argv[1])
    events = keydown_events(epbs)
    text, u_is_dot, unit = decode_morse_from_arrows(events)

    print(f"[*] arrow-events: {sum(1 for e in events if e[1] in (0x51,0x52))}, unit≈{unit:.4f}s, mapping: {'U=.' if u_is_dot else 'U=-'}")
    print("[*] decode:", text)
    flag = normalize_flag(text)
    if flag:
        print("[*] flag:", flag)

if __name__ == "__main__":
    main()

```

- python3 1.py My_PPT.pcapng

 

![image.png](my%20nervous%20ppt-dreamhack/image%205.png)

- Sau khi deocde thì mọi người sẽ thất flag nó hơi khê

lúc này thfi mọi người hãy bỏ  những từ mà có 2 kí tự liền nhau đu và ptt có vẻ là ppt phù hợp với đề bài hơn:)))

KHK{LOOK_AT_MY_PPT}
