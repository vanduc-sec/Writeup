# MZGZ-DREAMHACK-1

**Description
`It’s not crypto.`**

Sau khi tải file về chúng ta sẽ nhận được 1 file zip, tiến hành giải nén ta sẽ nhận được 1 file txt

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

- Chúng ta mở file txt thì thấy 1 đoạn mã base 64 chúng ta sẽ deccode nó và lưu vào 1 file khác:

base64 -d can_you_solve.txt > file

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%201.png)

- Mở file lên chúng  ta sẽ thấy nó là đoạn mã hex:

cat file

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%202.png)

- Nhìn xuống cuối file mọi người sẽ nhìn thấy b8f1 đây là header file gz nhưng mà bị đảo ngược nên mình đoán chúng ta sẽ phải đảo ngược nội dung file này và biến nội dung này thành 1 file  mình sẽ dùng lệnh:

rev file | xxd -r -p > file1

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%203.png)

- Sau khi đảo ngược và kiểm tra file vừa tao thì ta biết được là 1 file gzip và ban đầu tiêu đề nó là file jpg
- Bây giờ chúng ta sẽ tổi tên file về dạng .gz để giải nén
- Tiếp theo chúng ta sẽ giải nén nó bằng lệnh: gunzip file1

➜  dh mv file1 file1.gz
➜  dh gunzip file1.gz
➜  dh ls
'71613502-8b0e-4ffe-bc29-b45fed699dcb.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=OIK4A6AORYFTHBTQUV55%2F20260106%2Fsfo2%2Fs3%2Faws4_request&X-Amz-Date=20260106T054405Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signatu'
can_you_solve.txt
file
file1

- Kiểm tra file sau khi giải nén biết được nó file jpg chúng ta tiếp tục chuyển file về dạng jpg và mở nó lên :

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%204.png)
