# strike back-htb-med

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image.png)

Bài này thì cho chúng ta 1 file pcap và 1 file .dmp

```python
➜  Strike_Back file *                                                                                                   capture.pcap:                  pcap capture file, microsecond ts (little-endian) - version 2.4 (Ethernet, capture length 262144)
capture.pcap:Zone.Identifier:  ASCII text, with CRLF line terminators
freesteam.dmp:                 Mini DuMP crash report, 17 streams, Fri Nov 19 20:45:38 2021, 0x469925 type
freesteam.dmp:Zone.Identifier: ASCII text, with CRLF line terminators
```

mình đọc thử strinhs file dmp thì thấy chưa có gì lắm

```python
strings -el freesteam.dmp | head -n 200
MDMP
`FMw
\%Uw
`FMw
`FMw
`FMw
`FMw
`FMw
RSDS
ntdll.pdb
RSDSkbP
v#/u
wow64.pdb
RSDS
oQC4
wow64win.pdb
RSDS
wow64cpu.pdb
RSDS
wntdll.pdb
RSDS
wkernel32.pdb
RSDS|
wkernelbase.pdb
RSDS(S
apphelp.pdb
RSDS
msvcrt.pdb
RSDS
B5G'7,
wininet.pdb
RSDSs
PO2y
iertutil.pdb
RSDS`t
combase.pdb
RSDS
Bt@|6
ucrtbase.pdb
RSDS
wrpcrt4.pdb
RSDSA_C
ikzD
sechost.pdb
RSDS0n
advapi32.pdb
RSDS
shcore.pdb
RSDS
Lpi*
wsspicli.pdb
RSDS
wuser32.pdb
RSDS/
l3Db
wwin32u.pdb
RSDS
wgdi32.pdb
RSDS
wgdi32full.pdb
RSDS
msvcp_win.pdb
RSDS*j
wimm32.pdb
RSDS
Windows.Storage.pdb
RSDSs
WLDP.pdb
RSDS
shlwapi.pdb
RSDSW
profapi.pdb
RSDSYo
ws2_32.pdb
RSDS
OnDemandConnRouteHelper.pdb
RSDSa
U}|M
winhttp.pdb
RSDS
Kernel.Appcore.pdb
RSDS
wmswsock.pdb
RSDS
iphlpapi.pdb
RSDS~-uX
winnsi.pdb
RSDS
nsi.pdb
RSDS
urlmon.pdb
RSDStM)A
oleaut32.pdb
RSDS
crypt32.pdb
RSDS
dpapi.pdb
RSDS
cryptsp.pdb
RSDS
rsaenh.pdb
RSDS
bcrypt.pdb
RSDS#:.
$Baq
cryptbase.pdb
RSDSj
bcryptprimitives.pdb
RSDSl
NapiNSP.pdb
RSDS
qSZa_
pnrpnsp.pdb
RSDSS!
wshbth.pdb
RSDS
nlaapi.pdb
RSDS
dnsapi.pdb
RSDS
winrnr.pdb
RSDSU
fwpuclnt.pdb
RSDS
rasadhlp.pdb
pMw
pMw
pMw
pMw
pMw
!This program cannot be run in DOS mode.
lRich
.text
`.rdata
@.data
.reloc
BBAA
_^[]
SVWh
QSVW
@@AA
$SVWh
YPVS
~=SW
0_[^]
(_^]
JxV3
F$mj
DSVWh
Yj@h
WVh$
Y_^[
D$$P
D$0P
D$ P
j2ZI
VWj#Z
WWj Z
u3j!Z
Pj!Z
Pj+W
Pj"Z
WWWW
WWWj
SVW3
SVW3
v];E
sX9]
SWjD_W3
tSVWjD^V3
Y_^[
4SVWh
pVWjD_W3
$SVWh
YY^[
t8hd
lSVW
t@VVV
S}cV
SSSSj
ShO.
YYt$
~.S;u
GFF;}
FF;u
-G;>r
1+A;
SVW3
tU9~
9=8`
@_[Y
SVWh
jD_W
$SVWh
SVW3
_^[]
tQ9~
Y_^]
Y_^]
SVWh
Pacific Standard Time
Pacific Daylight Time
19041.1.amd64fre.vb_release.191206-1406
dbgcore.amd64,10.0.19041.546
C:\Users\npatrick\Downloads\freesteam.exe
C:\Windows\System32\ntdll.dll
C:\Windows\System32\wow64.dll
```

Tiếp đến vào pcap 

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%201.png)

Ơ đây mình thấy có file .exe mình sẽ export nó ra và vứt lên virustotal

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%202.png)

Ở đây mọi người thấy nó là mã độc và bên dưới chúng ta cũng thấy nó có vẻ là mã hóa cobal strike ròi

Tiếp để giải thì mọi tìm trên github sẽ có một số bài dẫn để giải bài này 

[https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/cs-extract-key.py](https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/cs-extract-key.py)

Để giải bài này đầu tiên mọi ng sẽ cần tìm key để tìm key thì mọi người sẽ cần phải có hex body của tin nhắn mã hóa

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%203.png)

Trong wireshark mọi người có thể thấy ở protocol http còn post 1 số submit.php khá là giống phần tin nhắn mã hóa nên mình sẽ lấy nó input cho hex body để chạy codee cs-extract-key.py

```python
python3 cs-extract-key.py -c 00000040317639faf73648274ba8a66d11182283f7fa26fe44b3982a36d80f6ffba4949e5ec759fffb372775d2ac002425547a11ddf2e05c2cb914e09ac033f01db0b60c freesteam.dmp
```

```python
➜  Strike_Back python3 cs-extract-key.py -c 00000040317639faf73648274ba8a66d11182283f7fa26fe44b3982a36d80f6ffba4949e5ec759fffb372775d2ac002425547a11ddf2e05c2cb914e09ac033f01db0b60c freesteam.dmp
File: freesteam.dmp
Searching for AES and HMAC keys
Found 2 instance(s) of string sha256\x00
Searching after sha256\x00 string (0x4048a)
AES key position: 0x00447f81
AES Key:  3ae7f995a2392c86e3fa8b6fbc3d953a :....9,....o.=.: 76.666667
HMAC key position: 0x0044b2a1
HMAC Key: bf2d35c0e9b64bc46e6d513c1d0f6ffe
SHA256 raw key: bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a
Searching for raw key
Searching after sha256\x00 string (0x441a49)
AES key position: 0x00447f81
AES Key:  3ae7f995a2392c86e3fa8b6fbc3d953a :....9,....o.=.: 76.666667
HMAC key position: 0x0044b2a1
HMAC Key: bf2d35c0e9b64bc46e6d513c1d0f6ffe
Searching for raw key
➜  Strike_Back
```

Ở đây chúng ta đã lấy được 

- AES key: `3ae7f995a2392c86e3fa8b6fbc3d953a`
- HMAC key: `bf2d35c0e9b64bc46e6d513c1d0f6ffe`
- raw key: `bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a`

Tiếp chúng ta sẽ dựa và key này để giải mã tiếp

[https://github.com/DidierStevens/DidierStevensSuite/blob/master/cs-parse-traffic.py](https://github.com/DidierStevens/DidierStevensSuite/blob/master/cs-parse-traffic.py)

```python
ython3 cs-parse-traffic.py -k bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a capture.pcap
```

```python
Packet number: 217
HTTP response (for request 214 GET)
Length raw data: 80
Timestamp: 1637354965 20211119-204925
Data size: 43
Command: 53 COMMAND_LS
 Arguments length: 35
 b'\xff\xff\xff\xfe\x00\x00\x00\x1bC:\\Users\\npatrick\\Desktop\\*'
 MD5: 2211925feba04566b12e81807ff9c0b4

Packet number: 217
HTTP request
http://192.168.1.9/match
Length raw data: 80
HMAC signature invalid

Packet number: 224
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 324
Counter: 6
Callback: 22 CALLBACK_PENDING
b'\xff\xff\xff\xfe'
----------------------------------------------------------------------------------------------------
C:\Users\npatrick\Desktop\*
D       0       11/19/2021 12:24:08     .
D       0       11/19/2021 12:24:08     ..
F       5175    11/11/2021 03:24:13     cheap_spare_parts_for_old_blimps.docx
F       282     11/10/2021 07:02:24     desktop.ini
F       24704   11/11/2021 03:22:16     gogglestown_citizens_osint.xlsx
F       62393   11/19/2021 12:24:10     orders.pdf

----------------------------------------------------------------------------------------------------

Packet number: 237
HTTP response (for request 234 GET)
Length raw data: 80
Timestamp: 1637355025 20211119-205025
Data size: 44
Command: 11 COMMAND_DOWNLOAD
 Arguments length: 36
 b'C:\\Users\\npatrick\\Desktop\\orders.pdf'
 MD5: b25952a4fd6a97bac3ccc8f2c01b906b

Packet number: 237
HTTP request
http://192.168.1.9/match
Length raw data: 80
HMAC signature invalid

Packet number: 254
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 62572
Counter: 7
Callback: 2 CALLBACK_FILE
 parameter1: 0
 length: 62393
 filenameDownload: C:\Users\npatrick\Desktop\orders.pdf

Counter: 8
Callback: 8 CALLBACK_FILE_WRITE
 Length: 62393
 MD5: 00f542efefccd7a89a55c133180d8581

Counter: 9
Callback: 9 CALLBACK_FILE_CLOSE
b'\x00\x00\x00\x00'
```

Sau khi chạy xong mọi người sẽ thấy hacker liệt kê thư mục desktop sau đó lấy file orders.pdf, tiesp chúng ta sẽ extract ra và check thử xem

```python
cs-parse-traffic.py -k bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a capture.pcap -e
```

```python
➜  Strike_Back file *
capture.pcap:                                 pcap capture file, microsecond ts (little-endian) - version 2.4 (Ethernet, capture length 262144)
capture.pcap:Zone.Identifier:                 ASCII text, with CRLF line terminators
cs-extract-key.py:                            Python script, ASCII text executable, with very long lines (1869)
cs-parse-traffic.py:                          Python script, ASCII text executable
freesteam.dmp:                                Mini DuMP crash report, 17 streams, Fri Nov 19 20:45:38 2021, 0x469925 type
freesteam.dmp:Zone.Identifier:                ASCII text, with CRLF line terminators
freesteam.exe:                                PE32 executable for MS Windows 4.00 (GUI), Intel i386 (stripped to external PDB), 7 sections
payload-00f542efefccd7a89a55c133180d8581.vir: PDF document, version 1.4, 1 page(s)
payload-1e4b88220d370c6bc55e213761f7b5ac.vir: PE32 executable for MS Windows 5.00 (DLL), Intel i386, 4 sections
payload-2211925feba04566b12e81807ff9c0b4.vir: data
payload-851cbc5a118178f5c548e573a719d221.vir: PE32+ executable for MS Windows 5.02 (DLL), x86-64, 5 sections
payload-b0cfbef2bd9a171b3f48e088b8ae2a99.vir: PE32+ executable for MS Windows 5.02 (DLL), x86-64, 5 sections
payload-b25952a4fd6a97bac3ccc8f2c01b906b.vir: ASCII text, with no line terminators
➜  Strike_Back
```

sau khi mở pdf lên thì mình đã có được flag

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%204.png)

HTB{Th4nk_g0d_y0u_f0und_1t_0n_T1m3!!!!}
