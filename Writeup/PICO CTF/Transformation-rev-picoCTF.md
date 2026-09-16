# Transformation-rev-picoCTF

[**enc**](https://challenge-files.picoctf.net/c_wily_courier/acd4ffc228784496e0a2c6445bba7646a457dcf13d9faca2f390c0d6259c25cb/enc)

''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

**ord()**: Chữ sang Số

**chr()**: Số sang Chữ

ở đây ta có vòng lặp for chạy với các i là các bược chắn 0,2,4,6,…..

với mỗi bước nó sẽ chuyển kí tự đầu tiên sang số và dịch trái 8bit 

kí tự liền tiếp sẽ được cộng vào sau kí tự trước đó tạo thành 1 số 16 bit và đc chuyển thành kí tự 

ở đây sau khi mở file bài cung cấp ta nhận được chuỗi 

```python
灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸形㝦㘲捡㕽
```

để giải mã ta sẽ duyệt toàn bộ chuỗi chuyển về số 16bit và chia ra 8 bit đầu 8 bit cuối rồi lại chuyển về thành kí tự 

```python
s="灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸形㝦㘲捡㕽"
flag= []
for i in s:
     tmp=ord(i)
     kt1=chr(tmp>>8)
     kt2=chr(tmp&255)
     flag.append(kt1+kt2)
print("".join(flag))
```

```python
PS C:\> python -u "c:\Users\Admin\Downloads\Untitled-1.py"
picoCTF{16_bits_inst34d_of_8_b7f62ca5}
PS C:\> 
```
