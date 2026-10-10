# An unusual sighting-ctftryout-hackthebox

![image.png](An%20unusual%20sighting-ctftryout-hackthebox/image.png)

- Bài này cung câp cho chúng ta 1 file bash_history và file log, chúng ta sẽ kết nối với ip và port xem có gì không

➜  forensics_an_unusual_sighting nc 83.136.255.170 45893

+---------------------+---------------------------------------------------------------------------------------------------------------------+
|        Title        |                                                     Description                                                     |
+---------------------+---------------------------------------------------------------------------------------------------------------------+
| An unusual sighting |                        As the preparations come to an end, and The Fray draws near each day,                        |
|                     |             our newly established team has started work on refactoring the new CMS application for the competition. |
|                     |                  However, after some time we noticed that a lot of our work mysteriously has been disappearing!     |
|                     |                     We managed to extract the SSH Logs and the Bash History from our dev server in question.        |
|                     |               The faction that manages to uncover the perpetrator will have a massive bonus come the competition!   |
|                     |                                                                                                                     |
|                     |                                            Note: Operating Hours of Korp: 0900 - 1900                               |
+---------------------+---------------------------------------------------------------------------------------------------------------------+

Note 2: All timestamps are in the format they appear in the logs

What is the IP Address and Port of the SSH Server (IP:PORT)

> 
> 
- Có vẻ là chúng ta sẽ phải dựa vào 2 file mà người ta cúng cấp để trả lời các câu hỏi rồi, câu đầu tiên là nó hỏi địa chỉ ip và cổng của server , câu này khá dễ vì chúng ta chỉ cần tìm dòng nào có chữ connection là được

[2024-01-28 15:24:23] Connection from 100.72.1.95 port 47721 on 100.107.36.130 port 2221 rdomain "”

- Nhìn là mọi người thấy được nó đang kết nối đến ip: 100.107.26.130 và port: 2221

![image.png](An%20unusual%20sighting-ctftryout-hackthebox/image%201.png)

- Câu tiếp theo nó hỏi lần đăng nhập thành công thì mọi người cũng tìm dòng đầu tiên có accepted là được

 [2024-02-13 11:29:50] Accepted password for root from 100.81.51.199 port 63172 ssh2

What time is the first successful Login

> 2024-02-13 11:29:50
[+] Correct!
> 

What is the time of the unusual Login

> 
> 
- Đối với câu hỏi này thì chúng ta phải kết hợp cả file txt và file, đáng ngờ sẽ là việc thực hiện nhiều lần đăng nhập faild liên tiếp hoặc việc đăng nhập xong dùng các câu lệnh đáng nghi, ở đây chúng ta sẽ thấy ngày 19-2 khi mà đăng nhập xong người ta dùng các câu lệnh: whoami, uname -a, cat /etc/passwd, cat /etc/shadow ,… việc thực hiện này có thể giúp khai thác mật khẩu user người dùng

[2024-02-19 04:00:14] Connection from 2.67.182.119 port 60071 on 100.107.36.130 port 2221 rdomain "”

What is the time of the unusual Login

> 2024-02-19 04:00:14
[+] Correct!
> 

What is the Fingerprint of the attacker's public key

> 
> 
- Câu này nó hỏi fingerprint của kẻ tấn công thì đó chính là mã sha256 chúng ta nhìn vào ngày 19-2 ngày mà chúng ta nghi là kẻ tấn công đáng ngờ ở đó chúng ta sẽ thấy sha256 của ip đó

![image.png](An%20unusual%20sighting-ctftryout-hackthebox/image%202.png)

What is the Fingerprint of the attacker's public key

> OPkBSs6okUKraq8pYo4XwwBg55QSo210F09FCe1-yj4
[+] Correct!
> 

What is the first command the attacker executed after logging in

> 
> 
- Câu tiếp theo là hỏi lệnh đầu tiên mà kẻ tấn công dùng sau khi đăng nhập la gì, viêc tìm lệnh thì chúng sẽ dùng file bash_history vì đây là file lưu những lệnh đã được dùng

![image.png](An%20unusual%20sighting-ctftryout-hackthebox/image%203.png)

- Mọi người có thể thấy lệnh đầu tiên được sử dụng vào ngày 19-2 là: whoami , này mọi người nhớ chuyển bàn phím sang english mà viết lệnh nhé lúc đầu mình để tiếng việt viết nó coi sai và out luôn.

What is the first command the attacker executed after logging in

> whoami
[+] Correct!
> 

What is the final command the attacker executed before logging out

- Tiếp theo là lệnh cuối cùng thì nó chính là: ./setup

What is the final command the attacker executed before logging out

> ./setup
[+] Correct!
> 

[+] Here is the flag: HTB{4n_unusual_s1ght1ng_1n_SSH_l0gs!}
➜  forensics_an_unusual_sighting
