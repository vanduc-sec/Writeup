# FFFFAAAATTT-dreamhack

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

- Bài này cung cấp cho chúng ta 1 file data ko biết là file gì có vẻ nó bị lỗi nhưng nhìn vào đề bài chúng ta có thể đoán được nó chính file hệ thống tệp tin, đối với mỗi file fat32 thì sẽ có các section và mỗi section là 512 byte.

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%201.png)

- Và section là section chứa thông tin quan trọng còn section 6 là được thiết kế để dự phòng mỗi khi section 0 bị lỗi do đó chúng ta muốn sửa section 0 thì có thể tìm đến section 6 để copy và thay thế vào.

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%202.png)

- Các bạn sẽ copy hết dữ liệu phần này và paste lên section 0 nhé.

 

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%203.png)

- Sau khi mở nó lên bằng ftk imager thì mình thấy có thư mục dreamhack.

 

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%204.png)

- Mình sẽ export thư mục này ra, sau khi export thì thấy có nhiều file ảnh và file zip có chứa mật khẩu, có lẽ flag nằm trong file zip kia.
- Sau khi mình khai thác tất cả các ảnh và mở nó bằng hxd thì tại GG.png mình thấy được mật khẩu file zip.

 

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image%205.png)

- Đến đây chúng ta sẽ extract file zip và có được flag.

 DH{3a5y_FAT32_r3bui1d}
