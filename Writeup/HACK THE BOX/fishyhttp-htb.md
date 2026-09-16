# fishyhttp-htb

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image.png)

Ở đây bài cho chúng ta 1 file pcap và 1 file .exe 

trong file pcap theo dõi theo luông http stream mọi người se nhận được đoạn tn bị mã hóa khi mà cắt các chữ cái đầu ra thì nó sẽ là base64 để mọi người decoe

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%201.png)

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%202.png)

h77P_s73417hy_revSHELL}

còn 1 số gói tin cũng sẽ decode ra như vậy nhưng mà mình ko liệt kê vào  đay  mọi người có thể thử sau

thì nó lấy:

- `ol -> 6`
- `img -> 4`
- `ol -> 6`
- `span -> 9`
- `button -> 7`
- `p -> 2`
- `cite -> 0`

ghép lại thành chuỗi hex, rồi convert sang text.

cite=0

h1=1

p=2

a=3

img=4

ul=5

ol=6

button=7

div=8

span=9

label=a

textarea=b

nav=c

b=d

i=e

blockquote=f

Day là doanj code nó sẽ dùng đẻ decode html trong wireshark

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%203.png)

HTB{Th4ts_d07n37_h77P_s73417hy_revSHELL}
