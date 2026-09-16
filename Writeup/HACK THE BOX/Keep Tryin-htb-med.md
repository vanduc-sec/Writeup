# Keep Tryin-htb-med

![image.png](Keep%20Tryin-htb-med/image.png)

Bài này cung cấp cho chúng ta 1 file pcap

![image.png](Keep%20Tryin-htb-med/image%201.png)

Http có 1 post đến /flag và /lootz 

![image.png](Keep%20Tryin-htb-med/image%202.png)

Đối với /flag nó chỉ là 1 chữ TryHarder không có gì lắm, tiếp đến /lootz

![image.png](Keep%20Tryin-htb-med/image%203.png)

Trong đây có 1 base64 mình decode thử xem 

![image.png](Keep%20Tryin-htb-med/image%204.png)

Có vẻ cũng chưa có gì lắm tiếp mình chuyển sang protocol cuối cùng là dns

![image.png](Keep%20Tryin-htb-med/image%205.png)

Yêu cầu này có tên miền phụ khá giống base64 mình decode thử xem

![image.png](Keep%20Tryin-htb-med/image%206.png)

Đến đây có vẻ như có gì đó đáng ngờ ở protocol này rồi

![image.png](Keep%20Tryin-htb-med/image%207.png)

Tiếp ở gói tin thứ 2 nhìn có vẻ như nó là base64url mình sẽ thay thế  ? thành .

Nhận được 1 đoạn base64url và decode

![image.png](Keep%20Tryin-htb-med/image%208.png)

Có vẻ như bị mã hóa j đó ròi vì file pcap còn mỗi chỗ này để khai thác thôi, đến đây thì mình tìm bằng init. thì phát hiện có một số mã hóa người ta dùng rc4 cũng rất giống với bài này của chúng ta nên mình sẽ thử rc4 nhưng mà để có thể decode được rc4 thì chúng ta cần có mật khẩu nên mình lấy nội dùng trong http /flag

TryHarder

![image.png](Keep%20Tryin-htb-med/image%209.png)

Ở đây chúng ta thấy được có 1 file zip và bên trong là file secret.txt

HTB{$n3aky_DN$_Tr1ck$}
