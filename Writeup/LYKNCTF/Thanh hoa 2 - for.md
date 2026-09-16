# Thanh hoa 2 - for

```python
➜  ctf binwalk lyknctf\ \(1\).mp4

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
13758623      0xD1F09F        JBOOT STAG header, image id: 1, timestamp 0x7D90897, image size: 2516476768 bytes, image JBOOT checksum: 0x15E, header JBOOT checksum: 0xE843
22774850      0x15B8442       gzip compressed data, ASCII, has header CRC, has 32432 bytes of extra data, has comment, last modified: 1999-05-07 09:28:16
23620544      0x1686BC0       MySQL MISAM index file Version 11
27207832      0x19F2898       JBOOT STAG header, image id: 4, timestamp 0xEEDA6C43, image size: 2834329882 bytes, image JBOOT checksum: 0x66EB, header JBOOT checksum: 0x222
27547085      0x1A455CD       bix header, header size: 64 bytes, header CRC: 0x302C0D3, created: 2087-01-18 01:48:33, image size: 1356977003 bytes, Data Address: 0xFDBABDDE, Entry Point: 0x3E862476, data CRC: 0x49B8B9F9, image name: ""
28416514      0x1B19A02       JBOOT STAG header, image id: 0, timestamp 0x2000000, image size: 16777216 bytes, image JBOOT checksum: 0x0, header JBOOT checksum: 0x2C24
28554086      0x1B3B366       YAFFS filesystem root entry, big endian, type symlink, v1 root directory
28554246      0x1B3B406       PNG image, 1280 x 720, 8-bit/color RGB, non-interlaced
28554287      0x1B3B42F       Zlib compressed data, default compression
28817164      0x1B7B70C       Zip archive data, encrypted at least v2.0 to extract, compressed size: 71, uncompressed size: 45, name: flag.txt
28817349      0x1B7B7C5       End of Zip archive, footer length: 22

➜  ctf
```

bài này mình thấy có file zip chứa flag.txt và file ảnh png giwof mình sẽ extract ra 

ở đây mình sẽ thấy file cần mật khẩu và có lẽ sẽ caafn khai thác từ file ảnh được thêm\

```python
➜  ctf binwalk -D 'png image:png' -D 'zip archive:zip' "lyknctf (1).mp4"

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
28554246      0x1B3B406       PNG image, 1280 x 720, 8-bit/color RGB, non-interlaced
28554287      0x1B3B42F       Zlib compressed data, default compression
28817164      0x1B7B70C       Zip archive data, encrypted at least v2.0 to extract, compressed size: 71, uncompressed size: 45, name: flag.txt
28817349      0x1B7B7C5       End of Zip archive, footer length: 22

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented

➜  ctf ls
'lyknctf (1).mp4'             'lyknctf (1).mp4:Zone.Identifier'   lyknctf.mp4:Zone.Identifier
'_lyknctf (1).mp4.extracted'   _lyknctf.mp4.extracted
➜  ctf cd _lyknctf\ \(1\).mp4.extracted
➜  _lyknctf (1).mp4.extracted ls
1B3B406.png  1B3B42F  1B3B42F.zlib  1B7B70C.zip  1B7B7C5.zip
➜  _lyknctf (1).mp4.extracted zsteg 1B3B406.png
[?] 207 bytes of extra data after image end (IEND), offset = 0x40306
extradata:0         .. file: Zip archive data, made by v2.0, extract using at least v2.0, last modified Jul 05 2026 20:35:16, uncompressed size 45, method=AES Encrypted
    00000000: 50 4b 03 04 14 00 01 00  63 00 68 a4 e5 5c 00 00  |PK......c.h..\..|
    00000010: 00 00 47 00 00 00 2d 00  00 00 08 00 0b 00 66 6c  |..G...-.......fl|
    00000020: 61 67 2e 74 78 74 01 99  07 00 02 00 41 45 03 08  |ag.txt......AE..|
    00000030: 00 33 83 41 81 d9 16 28  1c b2 bb 2e 59 1d 3d 4d  |.3.A...(....Y.=M|
    00000040: 68 4c c6 74 48 62 0c f0  b8 78 af 69 4c 24 3c 80  |hL.tHb...x.iL$<.|
    00000050: 69 6f 71 8a eb ef 68 2a  8e 25 4f 14 c5 b4 43 2f  |ioq...h*.%O...C/|
    00000060: aa fa d7 f2 20 53 b9 59  ef 7b 05 46 42 8f ba 26  |.... S.Y.{.FB..&|
    00000070: 41 bf 97 8b da 3f 64 93  50 4b 01 02 14 00 14 00  |A....?d.PK......|
    00000080: 01 00 63 00 68 a4 e5 5c  00 00 00 00 47 00 00 00  |..c.h..\....G...|
    00000090: 2d 00 00 00 08 00 0b 00  00 00 00 00 00 00 00 00  |-...............|
    000000a0: 80 01 00 00 00 00 66 6c  61 67 2e 74 78 74 01 99  |......flag.txt..|
    000000b0: 07 00 02 00 41 45 03 08  00 50 4b 05 06 00 00 00  |....AE...PK.....|
    000000c0: 00 01 00 01 00 41 00 00  00 78 00 00 00 00 00     |.....A...x..... |
imagedata           .. file: Targa image data - Map 65536 x 1 x 1 +1
b1,rgb,lsb,xy       .. text: "NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA NEMCHUATHANHHOA "
b2,b,lsb,xy         .. file: TeX font metric data (\025)
b3,b,lsb,xy         .. file: StarOffice Gallery theme , 1207959625 objects, 1st A\004
b4,rgb,lsb,xy       .. file: Targa image data 1 x 4352 x 1 +1 +273 "\020"
b4,bgr,lsb,xy       .. file: Targa image data (4096-257) 1 x 256 x 16 +4097 +257 - 1-bit alpha ""
➜  _lyknctf (1).mp4.extracted
```

ở đây khi check lsb mình thấy được text có vẻ nhưu là mk file zip

sau khi giải nén mình sẽ thu được flag 

```python
➜  _lyknctf (1).mp4.extracted 7z x 1B7B70C.zip -pNEMCHUATHANHHOA

7-Zip 24.09 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-11-29
 64-bit locale=en_US.UTF-8 Threads:16 OPEN_MAX:10240, ASM

Scanning the drive for archives:
1 file, 207 bytes (1 KiB)

Extracting archive: 1B7B70C.zip
--
Path = 1B7B70C.zip
Type = zip
Physical Size = 207

Everything is Ok

Size:       45
Compressed: 207
➜  _lyknctf (1).mp4.extracted LS
CAzsh: command not found: LS
➜  _lyknctf (1).mp4.extracted ls
1B3B406.png  1B3B42F  1B3B42F.zlib  1B7B70C.zip  1B7B7C5.zip  flag.txt
➜  _lyknctf (1).mp4.extracted cat flag.txt
LYKNCTF{N3M_CHU4_TH4NH_H04_D4C_S4N_XU_TH4NH}
➜  _lyknctf (1).mp4.extracted
```

FLAG: LYKNCTF{N3M_CHU4_TH4NH_H04_D4C_S4N_XU_TH4NH}
