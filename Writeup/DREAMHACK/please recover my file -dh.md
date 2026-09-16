# please recover my file -dh

![image.png](please%20recover%20my%20file%20-dh/image.png)

Bài này cung cấp cho mình 1 file data mình check bằng vol3 banners thì biết được là linux nên mình sẽ tải kernel bản này về

![image.png](please%20recover%20my%20file%20-dh/image%201.png)

ở đây mình check linux.bash.Bash

![image.png](please%20recover%20my%20file%20-dh/image%202.png)

Sau khi thấy có ./su mình sẽ tìm nó bằng psscan và  khoanh vùng nó bằng vol3 -f chall.raw linux.proc.Maps --pid 

![image.png](please%20recover%20my%20file%20-dh/image%203.png)

![image.png](please%20recover%20my%20file%20-dh/image%204.png)

Ở đây mọi người sẽ tháy có debidan.log và flag rất khả nghi, nên mình sẽ dump nó ra vol3 -f chall.raw -o dumps linux.proc.Maps --pid 2261 --dump

![image.png](please%20recover%20my%20file%20-dh/image%205.png)

![image.png](please%20recover%20my%20file%20-dh/image%206.png)

![image.png](please%20recover%20my%20file%20-dh/image%207.png)

ở đây mọi người sẽ thấy file flag và .log đều rất khả nghi vì có 48 và 32 byte có theer là để lmaf gì đó

![image.png](please%20recover%20my%20file%20-dh/image%208.png)

ngoài ra ở đây troogn như còn mã háo aes mấy cái kia co stheer là key và ciphertext rồi

![image.png](please%20recover%20my%20file%20-dh/image%209.png)

phát hienj là aes nên mình có tìm qua các file và tiafm được 1 key iv sau đó còn file nặng nhất mọi người reverse sẽ biết có key ascs2025 được dùng là key để mã hóa aes key nên mingf sẽ decode lại

Với từng byte `b` trong `key.bin` ở vị trí `i`, làm ngược lại như sau:

1. **rotate trái lại** byte đó
2. **trừ** `(i ^ 0x13)`
3. **XOR** với `acsc2025[i % 8]`

Mọi ngwuowif sễ lấy hex ở file cso 32 byte vì đấy key aes bị mã hóa, sau đó ta sẽ nhận dduocj key aess thật

![image.png](please%20recover%20my%20file%20-dh/image%2010.png)

![image.png](please%20recover%20my%20file%20-dh/image%2011.png)

acsc{4m4z1n9_4nd_c001_m3m0ry_r39i0n~}
