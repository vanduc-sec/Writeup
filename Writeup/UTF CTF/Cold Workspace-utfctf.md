# Cold Workspace-utfctf

![image.png](Cold%20Workspace-utfctf/image.png)

Đầu tiên bài cung cấp cho mình file .dmp mình dùng lệnh file check thử

![image.png](Cold%20Workspace-utfctf/image%201.png)

- file báo *MS Windows 64bit crash dump* vì nó thấy **magic/header giống dump**
- nhưng các trường phía sau lại **vô lý hoàn toàn**:
    - MachineImageType 0x74656874
    - 1967416169 processors
    - DumpType (0x9cc0e99a)
    - 6935312830061707549 pages

Một file dump thật sẽ không có các giá trị kiểu “rác” như vậy.

Thêm nữa:

- exiftool báo Unknown file type
- binwalk không thấy gì
- kích thước chỉ **534 kB** → quá nhỏ để là memory dump Windows có ý nghĩa
- 

![image.png](Cold%20Workspace-utfctf/image%202.png)

Với đoạn hex bạn đưa trước đó:

PAGEDU64 là dấu hiệu để **đánh lừa** tool nhận dạng dump, còn chuỗi:

```
ColdWorkspaceSyntheticDump
```

cho thấy đây là **synthetic/fake dump** do tác giả challenge tự dựng.

Nói ngắn gọn:

**đây không phải file để mở bằng volatility theo kiểu bình thường**, mà là **một container giả dạng crash dump**.

Ý nghĩa với bài CTF

Đề forensic này đang lái bạn theo hướng:

- đừng tin file type
- đừng xử lý như memory dump chuẩn
- phải coi nó như **file custom format / file ngụy trang**
- dữ liệu thật có thể bị:
    - XOR
    - chia stage
    - nhét trong text/binary lạ
    - encode nhiều lớp

Tiếp theo mình sẽ khai thác strings của nó mình sẽ thử lọc các chuỗi có thể đọc được ra 

```python
strings -a -n 6 cold-workspace.dmp | grep -E '[A-Za-z]'
```

khi dùng strings mọi người sẽ thấy cso đoạn tin nhắn base64 rất lạ với nội dung env_block_start

![image.png](Cold%20Workspace-utfctf/image%203.png)

Ở đây sẽ thấy có ba cái enck encv encd với k=key v=iv mình đoán rất giống mã hóa aes-256-cbc nên mình sẽ đem nó ra hex và decode thử xem

echo 'S4wX8ml7/f9C2ffc8vENqtWw8Bko1RAhCwLLG4vvjeT2iJ26nfeMzWEyx/HlK1KmOhIrSMoWtmgu2OKMtTtUXddZDQ87FTEXIqghzCL6ErnC1+GwpSfzCDr9woKXj5IzcU2C/Ft5u705bY3b6/Z/Q/N6MPLXV55pLzIDnO1nvtja123WWwH54O4mnyWNspt5' | base64 -d | xxd -p

ENCD:4b 8c 17 f2 69 7b fd ff 42 d9 f7 dc f2 f1 0d aa d5 b0 f0 19 28 d5 10 21 0b 02 cb 1b 8b ef 8d e4 f6 88 9d ba 9d f7 8c cd 61 32 c7 f1 e5 2b 52 a6 3a 12 2b 48 ca 16 b6 68 2e d8 e2 8c b5 3b 54 5d d7 59 0d 0f 3b 15 31 17 22 a8 21 cc 22 fa 12 b9 c2 d7 e1 b0 a5 27 f3 08 3a fd c2 82 97 8f 92 33 71 4d 82 fc 5b 79 bb bd 39 6d 8d db eb f6 7f 43 f3 7a 30 f2 d7 57 9e 69 2f 32 03 9c ed 67 be d8 da d7 6d d6 5b 01 f9 e0 ee 26 9f 25 8d b2 9b 79

ENCK: 0d d7 f8 04 2b 2c 86 a1 47 27 15 cf af 95 fa 30 b3 ce 1a d2 13 02 65 ca dd da c0 a9 e6 68 14 15

ENCV: c5 7a 46 c2 ea 2a 8a 18 3f 40 71 53 33 6c 8c c4

![image.png](Cold%20Workspace-utfctf/image%204.png)

FLAG:utflag{m3m0ry_r3t41ns_wh4t_d1sk_l053s}
