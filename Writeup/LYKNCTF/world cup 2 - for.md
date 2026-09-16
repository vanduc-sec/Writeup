# world cup 2 - for

bài này ở file ảnh trong phần hex cuối chúng ta thấy có file zip và bên trong có chứa file flag.txt 

![image.png](world%20cup%202%20-%20for/image.png)

đề bài yêu cầu chúng ta kiểm tra kỹ cấu trúc file

sau khi mình dùng binwalk thì thấy ra được luôn flag

```python
➜  ctf binwalk worldcup2_challenge.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
283620        0x453E4         Zip archive data, at least v2.0 to extract, compressed size: 29, uncompressed size: 27, name: flag_hidden.txt
283755        0x4546B         End of Zip archive, footer length: 22

➜  ctf binwalk -e worldcup2_challenge.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
283620        0x453E4         Zip archive data, at least v2.0 to extract, compressed size: 29, uncompressed size: 27, name: flag_hidden.txt

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented

➜  ctf ls
worldcup2_challenge.png  _worldcup2_challenge.png.extracted
➜  ctf cd _worldcup2_challenge.png.extracted
➜  _worldcup2_challenge.png.extracted ls
453E4.zip  flag_hidden.txt
➜  _worldcup2_challenge.png.extracted cat flag_hidden.txt
LYKNCTF{RespectToCaboVerde}%                                                                                            ➜  _worldcup2_challenge.png.extracted
```

FLAG: LYKNCTF{RespectToCaboVerde}
