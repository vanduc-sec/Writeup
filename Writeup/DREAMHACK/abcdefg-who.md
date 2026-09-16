# abcdefg-who

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

- Đầu tiên chúng ta sẽ thử đọc file txt mà bài cung cấp xem sao: cat  access_method.txt

➜  dh cat access_method.txt
ssh dream@[server IP] -p [port]%                                                                                        ➜  dh

- Nó yêu câu chúng ta kết nối bằng ssh

➜  dh ssh dream@host8.dreamhack.games -p 14660
dream@host8.dreamhack.games's password:
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 4.19.234 x86_64)

- Documentation: [https://help.ubuntu.com](https://help.ubuntu.com/)
- Management: [https://landscape.canonical.com](https://landscape.canonical.com/)
- Support: [https://ubuntu.com/pro](https://ubuntu.com/pro)

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

- Sau khi kết nối thì mình sẽ thử dùng ls nhưng mà ko có gì có vẻ là file bị ẩn nên mình sẽ thêm -la nữa:

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

ls
ls -la
total 28
drwxr-xr-x 1 dream dream 4096 Jan  9 11:56 .
drwxr-xr-x 1 root  root  4096 Jun 11  2024 ..
-rw-r--r-- 1 dream dream  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 dream dream 3771 Feb 25  2020 .bashrc
drwx------ 2 dream dream 4096 Jan  9 11:56 .cache
-rw-r--r-- 1 dream dream  807 Feb 25  2020 .profile

- Đến đây mình ko thấy có gì nên sẽ thử liệt kê thư mục gốc xem sao

ls /
bin
boot
dev
etc
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var

- Trông có vẻ nó ko có gì đặc biệt nên mình sẽ vào home xem người dùng trước nhé vì home khá quen thuộc

cd /home
ls
alice
bob
charlie
dream
eavan
frank
george
ls -la
total 44
drwxr-xr-x 1 root    root    4096 Jun 11  2024 .
dr-xr-xr-x 1 root    root    4096 Jan  9 11:50 ..
drwxr-xr-x 2 alice   alice   4096 Jun 11  2024 alice
drwxr-xr-x 2 bob     bob     4096 Jun 11  2024 bob
drwxr-xr-x 2 charlie charlie 4096 Jun 11  2024 charlie
drwxr-xr-x 1 dream   dream   4096 Jan  9 11:56 dream
drwxr-xr-x 2 eavan   eavan   4096 Jun 11  2024 eavan
drwxr-xr-x 1 frank   frank   4096 Jun 11  2024 frank
drwxr-xr-x 2 george  george  4096 Jun 11  2024 george

- Khi mà vào home thì mọi người có thể thấy ngoài người dùng dream chúng ta dùng để đăng nhập thì còn có rất nhiều người dùng khác nữa rất đáng nghi nên là mình sẽ check hết tất cả người dùng luôn nhé

ls -la frank
total 36
drwxr-xr-x 1 frank frank 4096 Jun 11  2024 .
drwxr-xr-x 1 root  root  4096 Jun 11  2024 ..
-rwxrwxrwx 1 root  root    60 Jun 11  2024 .bash.sh
-rw-r--r-- 1 frank frank  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 frank frank 3771 Feb 25  2020 .bashrc
-rw-r--r-- 1 frank frank  807 Feb 25  2020 .profile
--w--w--w- 1 root  root  2173 Jan  9 12:06 .secret_log

- Đến đây khi mà thấy người dùng frank thì mọi người có thể thấy có file secret_log khá là đáng nghi kahcs hoàn toàn với các người dùng khác và cả file [bash.sh](http://bash.sh) được chạy dưới quyền root
- Chúng ta sẽ chạy lênh: grep -aohm1 -E 'DH\{[^}]+\}' /home/frank/.secret_log

DH{MY_n3w_keYl0g9er_g0OD}
