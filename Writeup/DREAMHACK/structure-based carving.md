# structure-based carving

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

- Mình sẽ kiểm tra thử file

 

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%201.png)

- Kiểm tra thì thấy có vẻ file đã bị làm rối mk thử mở nó trong hxd xem sao

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%202.png)

- Đến đây chúng ta có thấy có vẻ có file zip gì đó nên mình sẽ dùng binwalk thử xem sao.

 

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%203.png)

- Check qua thì thấy có khá nhiều file được nén nhưng mà dung lượng khá ít nên chúng ta sẽ extract trên máy luôn.

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%204.png)

- Mọi người sẽ thấy file zip có file 20240421_213802.png này rất lạ vì nó được encrypted nên mình sẽ nhảy đến offset này và xem có j ko nhé và mình cx thử giải nén nó luôn

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%205.png)

- Vuốt xuống cuối để cắt file thì tôi thấy có dòng nó vẻ đó là password a1b2c3d4e5f6

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%206.png)

![image.png](please%20recover%20my%20file%20-dh/image%207.png)

Flag: DH{Y0uKn0wZ1p$TrUC7ur3?}
