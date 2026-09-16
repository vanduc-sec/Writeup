# silent archive-utfctf

![image.png](Last%20Byte%20Standing-utfctf/image.png)

Chúng ta phân tích đề bài một chút

**Silent**: dữ liệu bị giấu kín, không hiện lộ ngay, có thể nằm ở:

- cuối file
- trong metadata
- trong whitespace
- trong dữ liệu tưởng là rác

### **Incident response recovered a damaged archive from an isolated workstation.**

Hàm ý:

- dữ liệu không nằm gọn trong một file rõ ràng
- có thể bị chia nhánh, thất lạc, hoặc phải khôi phục thủ công
- “damaged archive” thường là hint rằng:
    - có file nén sâu bất thường
    - có dữ liệu bị chia ra nhiều phần
    - không thể chỉ `unzip` một phát là xong

---

### **The bundle split into two branches during transfer**

Đây là câu quan trọng nhất.

Nghĩa là **gói dữ liệu bị tách thành 2 nhánh**.

Bạn phải đi **cả hai nhánh**, không được chỉ làm một bên.

Tiếp đó mình tải file zip về và giải nén

sau khi giải nén mình nhận được 2 file tar và 1 file txt mình sẽ giải nén file đầu tiên trước

Với file txt nó cũng chỉ là thông báo về tình huống mà chúng ta cần xử lí thôi

![image.png](Last%20Byte%20Standing-utfctf/image%201.png)

Sau khi giải nén mình nhận được 2 file ảnh

```python
➜  utfctf file cam_300.jpg
cam_300.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 1280x720, components 3
➜  utfctf file cam_301.jpg
cam_301.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 1280x720, components 3
➜  utfctf exiftool cam_300.jpg
ExifTool Version Number         : 13.25
File Name                       : cam_300.jpg
Directory                       : .
File Size                       : 119 kB
File Modification Date/Time     : 2026:03:12 04:43:36+07:00
File Access Date/Time           : 2026:03:14 11:13:25+07:00
File Inode Change Date/Time     : 2026:03:14 11:12:54+07:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Image Width                     : 1280
Image Height                    : 720
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 1280x720
Megapixels                      : 0.922
➜  utfctf
```

Check qua một chút thì mình khong thấy có gì lắm nên sẽ thử mở bằng hxd xem dạng raw byte của nó

Sau khi mở bằng hxd mình thấy phần cuối 2 file đề có điểm lạ nên quay lại terminal trích ra nhìn cho rõ

```python
➜  utfctf tail -n 8 cam_300.jpg
---BEGIN-TELEMETRY---
TRACE_SEGMENT=A1f9z_Qp39_Xx2
cache_blob=q9A1eR2u4T6o8P0s
noise=R0xjODlhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs=
dbg_ptr=7f3c2d1a9b887766554433221100ffaa
cam_sig=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuLi4
AUTH_FRAGMENT_B64:QWx3YXlzX2NoZWNrX2JvdGhfaW1hZ2Vz
---END-TELEMETRY---
➜  utfctf tail -n 8 cam_301.jpg
---BEGIN-TELEMETRY---
TRACE_SEGMENT=A1f9z_Qp39_Xx2
cache_blob=q9A1eR2u4T6o8P0s
noise=R0xjODlhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs=
dbg_ptr=7f3c2d1a9b887766554433221100ffaa
cam_sig=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuLi4
AUTH_FRAGMENT_B64:MHI0bmczX0FyQ2gxdjNfVDRiU3A0Y2Uh
---END-TELEMETRY---
➜  utfctf
```

mình thử decode 1 số base64 xuất hiện trong đó

```python
➜  utfctf echo 'QWx3YXlzX2NoZWNrX2JvdGhfaW1hZ2Vz' | base64 -d
Always_check_both_images%                                                                                               ➜  utfctf echo 'MHI0bmczX0FyQ2gxdjNfVDRiU3A0Y2Uh' | base64 -d
0r4ng3_ArCh1v3_T4bSp4ce!%                                                                                               ➜  utfctf
```

hết fiel thứ 1 không có gì nữa rồi, mình chuyển snag file tar thứ2

```python
➜  utfctf tar -xf File2.tar
➜  utfctf ls
999.tar  cam_300.jpg  cam_301.jpg  File1.tar  File2.tar  freem4.zip  freem4.zip:Zone.Identifier  README.txt
➜  utfctf tar -xf 999r
tar: 999r: Cannot open: No such file or directory
tar: Error is not recoverable: exiting now
➜  utfctf tar -xf 999.tar
➜  utfctf ls
998.tar  999.tar  cam_300.jpg  cam_301.jpg  File1.tar  File2.tar  freem4.zip  freem4.zip:Zone.Identifier  README.txt
➜  utfctf
```

Đối với file tar số 2 mk giải nén thì nó lại ra file 999.tar xong xuongs 998.tar thấy có vẻ như là nó sẽ phải giải nén về đến tận 0 hoặc 1 .tar làm tay ko khả hti nên mk sẽ dùng python để tự động giải nén

```python
while ls *.tar >/dev/null 2>&1; do
  f=$(ls *.tar | sort -V | head -n 1)
  tar -xf "$f" && rm -f "$f"
done
```

```python
➜  utfctf while ls *.tar >/dev/null 2>&1; do
  f=$(ls *.tar | sort -V | head -n 1)
  tar -xf "$f" && rm -f "$f"
done
zsh: no matches found: *.tar
➜  utfctf ls
cam_300.jpg  cam_301.jpg  freem4.zip  freem4.zip:Zone.Identifier  Noo.txt  README.txt
➜  utfctf
```

Sau khi giải nén thấy xuất hiện Noo.txt

```python
➜  utfctf cat Noo.txt
PK     r�k\p���u

NotaFlag.txtUT ��iux
�6=d6Q�o_��X�-�֜���kPp���ur��N,��zի�vF`��ӥn��{�p�\�oj�~$��␦�P�"������!J�-�M����pLk�ŀO�)й]���
PK     r�k\���hnotes.mdUT      ��iux
                                    �෡{��b`oֆ)�:uГ>���  �u]�?�����YЁ�X���=nr TR#bS�     �������C�'�_`Hمfe^6���M�'��ui5�8y�HR1>P���hjPK r�k\p���u

��NotaFlag.txtU�iux
                   �PK r�k\���h���notes.mdU�iux
                                               �PK��%                                                                   ➜  utfctf
```

mình đọc nó thì thấy có pk có vẻ như nó là file zip nên mình thử kiểm tra lại 

```python
➜  utfctf file Noo.txt
Noo.txt: Zip archive data, made by v3.0 UNIX, extract using at least v2.0, last modified Mar 11 2026 16:43:36, uncompressed size 522, method=deflate
➜  utfctf unzip Noo.txt
Archive:  Noo.txt
[Noo.txt] NotaFlag.txt password:
```

Sau khi kiểm tra biết nó là file zip va giải nén thì nó yêu cầu password nhớ đến 2 đoạn tn mk vừa cso được ở file 1 có vẻ như là mk nên mình thử ghép lịa và thử từng cái 1 thì mk là 0r4ng3_ArCh1v3_T4bSp4ce!

```python
➜  utfctf unzip Noo.txt
Archive:  Noo.txt
[Noo.txt] NotaFlag.txt password:
  inflating: NotaFlag.txt
  inflating: notes.md
➜  utfctf
```

Tiếp tục nhận được 1 file mk và 1 file txt, đọc thử file md

```python
➜  utfctf cat notes.md
# Incident Notes
Focus on camera deltas and archive chain integrity.
No direct IOC included in this file.
➜  utfctf
```

Có vẻ như khong có gì lắm nó giống như là ghi chú về việc hai ảnh ở file 1 có vấn đề , tiếp đến mk khai thác fiel còn lại

```python
➜  utfctf cat NotaFlag.txt

➜  utfctf
```

Đọc thì nó ra 1 khoảng trắng rất giống ngôn ngữ whitespace hoặc là bị mã hóa bit bằng tap/space

![image.png](Last%20Byte%20Standing-utfctf/image%202.png)

mọi ngươi sẽ find space và thayt thế bằng 0 sau đó là tìm tab và thay bằng 1

![image.png](Last%20Byte%20Standing-utfctf/image%203.png)

Tiếp là sẽ thửu decode binary

![image.png](Last%20Byte%20Standing-utfctf/image%204.png)

Flag: utflag{d1ff_th3_tw1ns_unt4r_th3_st0rm_r34d_th3_wh1t3sp4c3}
