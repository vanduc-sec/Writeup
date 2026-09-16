# TrueSecrets-htb

![image.png](TrueSecrets-htb/image.png)

- Bài này theo mô tả chúng ta biết được đây là 1 file được dump từ bộ nhớ máy tính nên chúng ta sẽ sử dụng volatility 3.
- Đầu tiên mình sẽ xem danh sách các tiến trình trước

 

![image.png](TrueSecrets-htb/image%201.png)

- Chúng ta sẽ thấy được tiến trình TrueCrypt.exe khá là nó là một tiến trình mã hóa, tiếp theo mình sẽ dùng cmdline để check các lệnh đang được sử dụng.

 

![image.png](TrueSecrets-htb/image%202.png)

- Ở đay chúng ta sẽ thấy truecrypt đang được chạy và có 7zFm.exe đang chạy với  backup_developmen khá đáng nghi, vì bài này có liên quan đến truecrypt nên mình sẽ dùng tiến trình truecrypt để quét.

![image.png](TrueSecrets-htb/image%203.png)

 

- Ở đây mọi người sẽ thấy được 1 password, tiếp theo mình sẽ check các file của tiến trình lạ

![image.png](TrueSecrets-htb/image%204.png)

- Đây mọi người sẽ thầy file zip mình nghi ngờ ở trên nên mình sẽ dump ra và dùng mk vừa tìm được
- Mọi người sẽ dùng handles để xem file object để dump.

  

![image.png](TrueSecrets-htb/image%205.png)

![image.png](TrueSecrets-htb/image%206.png)

Sau khi nhận được file .tc mọi ngừi sẽ mở nó lên bằng truecrypt 

![image.png](TrueSecrets-htb/image%207.png)

![image.png](TrueSecrets-htb/image%208.png)

Chúng ta sẽ nhận được file python với nội dung như này đọc xong chúng ta sẽ biết đây là kiểu madx hóa DES/CBC cơ bản cùng với key và iv, bây giờ chúng ta sẽ dùng key iv và decode bằng mã sau

echo "<BASE64_LINE>" | base64 -d | openssl enc -d -des-cbc -K 414b615064536756 -iv 51655468576d5971

![image.png](TrueSecrets-htb/image%209.png)

HTB{570r1ng_53cr37_1n_m3m0ry_15_n07_g00d}
