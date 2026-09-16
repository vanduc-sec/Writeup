# Thanh hoa 1 - for

Bài cung cấp cho chúng ta 1 file âm thanh xem spectrogram phát hiện có đoạn chữ lạ 

![image.png](Thanh%20hoa%201%20-%20for/image.png)

“RAUMAPHATAU”

```python
  ctf binwalk lyknctf.mp4

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
263737        0x40639         JBOOT STAG header, image id: 0, timestamp 0x1000000, image size: 16777216 bytes, image JBOOT checksum: 0x0, header JBOOT checksum: 0x2C24
401329        0x61FB1         YAFFS filesystem root entry, big endian, type symlink, v1 root directory
6184150       0x5E5CD6        bix header, header size: 64 bytes, header CRC: 0x29C019F, created: 1972-07-26 22:38:55, image size: 19264 bytes, Data Address: 0xA177004A, Entry Point: 0xB80DA7A4, data CRC: 0xEFAF6603, image name: "?}"
6908986       0x696C3A        gzip compressed data, last modified: 2004-06-17 16:04:17
10997718      0xA7CFD6        bix header, header size: 64 bytes, header CRC: 0x67B019E, created: 2093-10-13 03:39:43, image size: 172167 bytes, Data Address: 0x2616F6B5, Entry Point: 0x792873BE, data CRC: 0xBFF64A4E, image name: "("
16004203      0xF4346B        JBOOT STAG header, image id: 1, timestamp 0x7D90897, image size: 2516476768 bytes, image JBOOT checksum: 0x15E, header JBOOT checksum: 0xE843
20286483      0x1358C13       bix header, header size: 64 bytes, header CRC: 0xD47419A, created: 2024-07-14 12:18:38, image size: 1285948527 bytes, Data Address: 0xE4400005, Entry Point: 0x47934B0E, data CRC: 0xE9A7EDD9, image name: ""
25914084      0x18B6AE4       gzip compressed data, ASCII, has header CRC, has 32432 bytes of extra data, has comment, last modified: 1999-05-07 09:28:16
26827241      0x19959E9       MySQL MISAM index file Version 11
27422934      0x1A270D6       gzip compressed data, last modified: 2067-04-24 00:40:36 (bogus date)
31910541      0x1E6EA8D       Zip archive data, encrypted at least v2.0 to extract, compressed size: 79, uncompressed size: 49, name: flag.txt
31910734      0x1E6EB4E       End of Zip archive, footer length: 22

➜  ctf
```

dùng lệnh binwalk thấy có 1 file zip trong đó có file flag.txt mình sẽ extract nó ra

```python
➜  ctf binwalk -D 'zip archive:zip' lyknctf.mp4

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
31910541      0x1E6EA8D       Zip archive data, encrypted at least v2.0 to extract, compressed size: 79, uncompressed size: 49, name: flag.txt
31910734      0x1E6EB4E       End of Zip archive, footer length: 22

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented
```

sau đó dùng đoạn chữ cta thu thập được bắt đầu giải mã

```python
➜  _lyknctf.mp4.extracted 7z x 1E6EA8D.zip -pRAUMAPHATAU

7-Zip 24.09 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-11-29
 64-bit locale=en_US.UTF-8 Threads:16 OPEN_MAX:10240, ASM

Scanning the drive for archives:
1 file, 215 bytes (1 KiB)

Extracting archive: 1E6EA8D.zip
--
Path = 1E6EA8D.zip
Type = zip
Physical Size = 215

Everything is Ok

Size:       49
Compressed: 215
➜  _lyknctf.mp4.extracted LS
zsh: command not found: LS
➜  _lyknctf.mp4.extracted ls
1E6EA8D.zip  1E6EB4E.zip  flag.txt
➜  _lyknctf.mp4.extracted cat flag.txt
LYKNCTF{NGU01_TH4NH_H04_4N_R4U_M4_PH4_DU0NG_T4U}
➜  _lyknctf.mp4.extracted
```

FLAG: LYKNCTF{NGU01_TH4NH_H04_4N_R4U_M4_PH4_DU0NG_T4U}
