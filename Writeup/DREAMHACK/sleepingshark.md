# sleepingshark

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

- Bài cung cấp cho chúng ta 1 file pcap

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%201.png)

- Chúng ta sẽ thấy có gói tin có nội dung lạ là một url encode nên mk sẽ decode thử

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%202.png)

- Ở đây chúng ta có thể hiểu đơn giản nó là câu lệnh payload tấn công nó sẽ check 1 ki tu nào của flag và nếu đúng thì sẽ phản hồi chậm lại 3s
- Vậy thì bây giờ chúng ta sẽ kiểm tra xem gói tin nào gửi chậm 3s thì đó sẽ là những kí tự đúng của flag, đối vưới bài này thì mình sẽ dùng python để nốt các kitu

 

```python
import pyshark
import re

pcap_file = 'dump.pcap'
cap = pyshark.FileCapture(pcap_file, display_filter='http')

http_requests = {}
flag_chars = {}

print("HTTP 200 OK packets with delay >= 3.0 seconds:\\n")

def extract_position_and_ascii(uri):
    percent_indices = [m.start() for m in re.finditer(r'%..', uri)]
    if len(percent_indices) >= 16:
        try:
            pos_start = percent_indices[11] + 3
            ascii_start = percent_indices[15] + 3

            pos = ''
            while pos_start < len(uri) and uri[pos_start].isdigit():
                pos += uri[pos_start]
                pos_start += 1

            ascii_val = ''
            while ascii_start < len(uri) and uri[ascii_start].isdigit():
                ascii_val += uri[ascii_start]
                ascii_start += 1

            return int(pos), int(ascii_val)
        except:
            return None, None
    return None, None

for pkt in cap:
    try:
        stream_id = pkt.tcp.stream
        if 'request_method' in pkt.http.field_names:
            uri = pkt.http.get('request_full_uri', '')
            http_requests[stream_id] = uri

        if 'response_code' in pkt.http.field_names and pkt.http.response_code == '200':
            delta = float(pkt.tcp.time_delta)
            if delta >= 3.0:
                uri = http_requests.get(stream_id, '[Unknown URI]')
                print(f'Delta: {delta:.6f}s\\nRequest URI: {uri}')

                pos, ascii_val = extract_position_and_ascii(uri)
                if pos is not None and ascii_val is not None:
                    char = chr(ascii_val)
                    flag_chars[pos] = char
                    print(f' -> Found flag[{pos}] = {char}\\n')

    except AttributeError:
        continue

flag = ''.join(flag_chars[i] for i in sorted(flag_chars))
print(f'\\n✅ Recovered flag: {flag}')
```

```python

```

GoN{T1mE_B4s3d_5QL_Inj3c7i0n_wI7h_Pc4p}
