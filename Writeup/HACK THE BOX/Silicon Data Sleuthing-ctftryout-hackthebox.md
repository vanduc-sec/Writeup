# Silicon Data Sleuthing-ctftryout-hackthebox

![image.png](Silicon%20Data%20Sleuthing-ctftryout-hackthebox/image.png)

- Đối với bài này thì mọi người sẽ nhận được 1 file bin, bản chất của nó chính  là 1 file nén zip chứa thông tin về cái router đó, mọi người dùng : binwalk -e chal_router_dump.bin

![image.png](Silicon%20Data%20Sleuthing-ctftryout-hackthebox/image%201.png)

- Chúng ta sẽ kết nối đến ip và port mà bài cung cấp xem mình phải làm gì.

forensics_silicon_data_sleuthing.zip:Zone.Identifier
➜  hackthebox nc 83.136.251.11 35508

+------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|         Title          |                                                                                       Description                                                                                        |
+------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Silicon Data Sleuthing |                         In the dust and sand surrounding the vault, you unearth a rusty PCB... You try to read the etched print, it says Open..W...RT, a router!                         |
|                        |                                                         You hand it over to the hardware gurus and to their surprise the ROM Chip is intact!                                             |
|                        |                                                    They manage to read the data off the tarnished silicon and they give you back a firmware image.                                       |
|                        |              It's now your job to examine the firmware and maybe recover some useful information that will be important for unlocking and bypassing some of the vault's countermeasures! |
+------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

What version of OpenWRT runs on the router (ex: 21.02.0)

> 
> 
- Ở đây nó yêu cầu chúng ta cung cấp phiên bản của cái router này, thương thông tin phiên bản này sẽ nằm trong  /squashfs-root/etc/banner, mọi người dùng lệnh cat đọc file banner là được

![image.png](Silicon%20Data%20Sleuthing-ctftryout-hackthebox/image%202.png)

What version of OpenWRT runs on the router (ex: 21.02.0)

> 23.05.0
[+] Correct!
> 

What is the Linux kernel version (ex: 5.4.143)

> 
> 
- Câu này nó hỏi về phiên bản hạt nhân của linux cái này nó sẽ nằm trong lib/modules/

![image.png](Silicon%20Data%20Sleuthing-ctftryout-hackthebox/image%203.png)

What is the Linux kernel version (ex: 5.4.143)

> 5.15.134
[+] Correct!
> 

What's the hash of the root account's password, enter the whole line (ex: root:$2$JgiaOAai....)

> 
> 
- Tiếp theo nó yêu cầu chúng ta nhập mã băm(hash) mật khẩu của tài khoản root, trong hệ điều hành linux thì mật khẩu người dùng ko được lưu dưới dạng văn bản rõ mà sẽ được mã hóa(băm) và nó sẽ đươc ở /etc/shadow của phân vùng Read-Write(JFFS2).
- Bây giờ chúng ta sẽ quay lại bên trong thư mục: _chal_router_dump.bin.extracted và giải nén file jffs2
- Đối với file jffs2 thì mọi người cần tải tool jefferson thì mới giải nén được nhé, ở đây mình cài tool rôi nên sẽ giải nén luôn, sau khi giải nén xong thì mọi người tìm đệ quy toàn thư mục là được.

➜  _chal_router_dump.bin.extracted jefferson -d output_folder 7C0000.jffs2
dumping fs to /home/vanduc123/ctf/hackthebox/_chal_router_dump.bin.extracted/output_folder (endianness: <)
Jffs2_raw_inode count: 47
Jffs2_raw_dirent count: 48
writing S_ISREG upper/sysupgrade.tgz
writing S_ISLNK .fs_state
writing S_ISDIR upper
writing S_ISDIR upper
writing S_ISDIR work
writing S_ISDIR work/work
writing S_ISDIR work/work
writing S_ISREG work/work/#2

➜  _chal_router_dump.bin.extracted ls
18168C     42C2C8.squashfs  7C0000.jffs2   squashfs-root
18168C.7z  70000            output_folder  squashfs-root-0
➜  _chal_router_dump.bin.extracted cd output_folder
➜  output_folder ls
1  upper  work
➜  output_folder grep -r "root:" .
./work/work/#32:root:$1$YfuRJudo$cXCiIJXn9fWLIt8WY2Okp1:19804:0:99999:7:::
./work/work/#2c:root:x:0:0:root:/root:/bin/ash
./work/work/#1a:root:x:0:
./work/work/#2e:if ( grep -qs '^root::' /etc/shadow && \
grep: ./work/work/#2: Permission denied
➜  output_folder

> root:$1$YfuRJudo$cXCiIJXn9fWLIt8WY2Okp1:19804:0:99999:7:::
[+] Correct!
> 

What is the PPPoE username

- Tiếp theo là tên đăng nhập của giao thức PPPoE, này nó cx nằm trong thư mục mà mọi người vừa giải nén file jffs2 vào nhé.
- Mọi người vào thư mục upper và giải nén file .tgz ra sau đó truy cập  etc/config/network

➜  output_folder cd upper
➜  upper ls
sysupgrade.tgz
➜  upper tar -zxvf sysupgrade.tgz
etc/config/dhcp
etc/config/dropbear
etc/config/firewall
etc/config/luci
etc/config/network
etc/config/rpcd
etc/config/system
etc/config/ucitrack
etc/config/uhttpd
etc/config/wireless
etc/dropbear/dropbear_ed25519_host_key
etc/dropbear/dropbear_rsa_host_key
etc/group
etc/hosts
etc/inittab
etc/luci-uploads/.placeholder
etc/nftables.d/10-custom-filter-chains.nft
etc/nftables.d/README
etc/opkg/keys/b5043e70f9a75cde
etc/passwd
etc/profile
etc/rc.local
etc/shadow
etc/shells
etc/shinit
etc/sysctl.conf
etc/uhttpd.crt
etc/uhttpd.key
➜  upper ls
etc  sysupgrade.tgz
➜  upper

- Sau đó mọi người đọc file network là ra thôi

 

config interface 'wan'
option device 'wan'
option proto 'pppoe'
option username 'yohZ5ah'
option password 'ae-h+i$i^Ngohroorie!bieng6kee7oh'
option ipv6 'auto'

- Tiếp theo là đến tên wifi(ssid) thì cái này cũng được lưu trong thư mục config và mọi người đọc file wireless là ra nhé.

 

What is the PPPoE username

> yohZ5ah
[+] Correct!
> 

What is the PPPoE password

> ae-h+i$i^Ngohroorie!bieng6kee7oh
[+] Correct!
> 

What is the WiFi SSID

> 
> 

➜  config cat wireless

config wifi-device 'radio0'
option type 'mac80211'
option path '1e140000.pcie/pci0000:00/0000:00:01.0/0000:02:00.0'
option channel 'auto'
option band '2g'
option htmode 'HT20'
option txpower '20'
option cell_density '0'

config wifi-iface 'default_radio0'
option device 'radio0'
option network 'lan'
option mode 'ap'
option ssid 'VLT-AP01'
option encryption 'sae-mixed'
option key 'french-halves-vehicular-favorable'
option ieee80211r '1'
option ft_over_ds '0'
option wpa_disable_eapol_key_retries '1'

What is the WiFi Password

> french-halves-vehicular-favorable
[+] Correct!
> 

What are the 3 WAN ports that redirect traffic from WAN -> LAN (numerically sorted, comma sperated: 1488,8441,19990)

- Câu hỏi cuối này yêu cầu chúng ta tìm các cổng để chuyển tiếp từ mạng ngoài(WAN) vào mạng trong(LAN), cái này thì mọi người sẽ nghĩ ngay đến firewall nhé.

 

dhcp  dropbear  firewall  luci  network  rpcd  system  ucitrack  uhttpd  wireless
➜  config cat firewall

config defaults
option syn_flood '1'
option input 'REJECT'
option output 'ACCEPT'
option forward 'REJECT'

config zone
option name 'lan'
list network 'lan'
option input 'ACCEPT'
option output 'ACCEPT'
option forward 'ACCEPT'

config zone
option name 'wan'
list network 'wan'
list network 'wan6'
option input 'REJECT'
option output 'ACCEPT'
option forward 'REJECT'
option masq '1'
option mtu_fix '1'

config redirect
option dest 'lan'
option target 'DNAT'
option name 'DB'
option src 'wan'
option src_dport '1778'
option dest_ip '192.168.1.184'
option dest_port '5881'

config redirect
option dest 'lan'
option target 'DNAT'
option name 'WEB'
option src 'wan'
option src_dport '2289'
option dest_ip '192.168.1.119'
option dest_port '9889'

config redirect
option dest 'lan'
option target 'DNAT'
option name 'NAS'
option src 'wan'
option src_dport '8088'
option dest_ip '192.168.1.166'
option dest_port '4431'

- Mọi người lấy port ở src_dport nhé.

 

What are the 3 WAN ports that redirect traffic from WAN -> LAN (numerically sorted, comma sperated: 1488,8441,19990)

> 1778,2289,8088
[+] Correct!
> 

[+] Here is the flag: HTB{Y0u'v3_m4st3r3d_0p3nWRT_d4t4_3xtr4ct10n!!_193dfef20a27de29666819f341730507}
➜  hackthebox
