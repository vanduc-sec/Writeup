# Find the USB-dreamhack

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

Sau khi tải về mọi người mở nó lên bằng ftk và đi đến /root/Windows/System32/config/SYSTEM

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%201.png)

Sau đó mọi người export nó ra, để khai thác registry thì mọi người dùng RegRipper
`perl ~/RegRipper3.0/rip.pl -r SYSTEM -p usb`

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%202.png)

DH{058F_6387_03A49E66}
