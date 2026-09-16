# the missing image frag ment-dh-4

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

Bài này cung cấp cho chúng ta 1 file disk imge nên mình sẽ mở nó bằng autopsy, vì bài có nhắc đến những dữ liệu bị xóa nên mình sẽ xkhai thác các file bị xóa

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%201.png)

Ở 1 trong các file bị xóa mọi người sẽ thấy có 1 đoạn mã base64 vô cùng đáng nghi nên mình mang nó đi decode 

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%202.png)

Đây có vẻ như alf mật khẩu của file nào đó, nhưng mà tìm trong disk mình ko thấy còn gì nữa nên đã ra tìm ở rawbyte của file disk và phát hiện của mình là có 1 file zip với file secret.jpg trong đó

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%203.png)

offest bắt đầu file zip: 5f8161

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%204.png)

Kết thúc file zip: 5fca3a

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%205.png)

mình cắt ra và check sau đó sẽ dùng thử mật khẩu vừa lấy đươc kai để giải nén 

![secret.jpg](the%20missing%20image%20frag%20ment-dh-4/secret.jpg)

INCOGNITO{EVID-68eb-4ac5-hd19}
