# the epstein files-CryptoniteCTF

![image.png](the%20epstein%20files-CryptoniteCTF/image.png)

Bài này cung cấp cho chúng ta 1 file pdf mở nó lên thì mình thấy có nhiều phần bị bôi đen mình sẽ copy toàn bộ và dán sang notepad

![image.png](the%20epstein%20files-CryptoniteCTF/image%201.png)

![image.png](the%20epstein%20files-CryptoniteCTF/image%202.png)

Sau khi dán qua notepad mọi người sẽ thấy gần như những chỗ bị bôi đen đều có nội dung những hộp màu đen kia chỉ là người ta đề lên mà thôi thực ra bên dưới nó vẫn có nội dung

Đến đây mình có được key aes: 3f9c2a7b8d4e1f609a2b3c4d5e6f7081

Tiếp theo là mình sẽ mở nó trong hxd để xem ở dạng rawbyte thì mình tiếp tục phát hiện được key iv của mã aes: a1b2c3d4e5f60718293a4b5c6d7e8f90

![image.png](the%20epstein%20files-CryptoniteCTF/image%203.png)

Tìm một hồi ở bề mặt nổi có vẻ như không còn gì nữa tiếp theo đó là mình sẽ đi sâu hơn vào cấu trúc pdf 

![image.png](the%20epstein%20files-CryptoniteCTF/image%204.png)

Khi mà mình dùng qpdf để kiểm tra thì thấy xref của nó đã có vấn đề mình sẽ chuyển nó sang json và khai thác tiếp

```python
qpdf --json output.pdf > cau_truc.json
```

![image.png](the%20epstein%20files-CryptoniteCTF/image%205.png)

Ở đây mọi người sẽ thấy obj: 4 0 R nó là có 3 trang là 7 8 9 nhưng mà ngay xuống dưới có ngay 1 trang 6 0 R xuất hiện 

- **Sự bất thường:** Mặc dù obj:6 là một trang, nhưng nó **hoàn toàn không có mặt trong danh sách /Kids của đối tượng số 4**.
- **Hậu quả:** Vì không nằm trong danh sách /Kids, các phần mềm đọc PDF bình thường sẽ coi obj:6 là "trang mồ côi" và bỏ qua không hiển thị nó lên màn hình. Đây chính là nửa nội dung không được render (hiển thị).

Tiếp để khai thác trang này thì mọi người sẽ thêm page này vào obj 4 0 R

![image.png](the%20epstein%20files-CryptoniteCTF/image%206.png)

Sau khi đã sửa mọi người sẽ lưu file json này lại và tạo pdf mới 

```python
qpdf output.pdf --update-from-json=cau_truc.json PDF_Da_Sua.pdf
```

Sau khi có được file pdf mới mọi người mở nó lên là xuất hiện thêm 1 trang mưới có đoạn hex

![image.png](the%20epstein%20files-CryptoniteCTF/image%207.png)

Mọi người đảo ngược lại xem là sẽ được đoạn hex: 4fc80625b049f68462f7d02e79a8cbc1875ecd11a2b331eaccc998fc9ffb3647d0adb35e993015f4aa88c894c09a9a67

Tổng hết lại các thông tin:

aes-iv: a1b2c3d4e5f60718293a4b5c6d7e8f90

aes-key: 3f9c2a7b8d4e1f609a2b3c4d5e6f7081

hex text: 4fc80625b049f68462f7d02e79a8cbc1875ecd11a2b331eaccc998fc9ffb3647d0adb35e993015f4aa88c894c09a9a67

Cuối cùng mọi người lên cyberchef decode là được

![image.png](the%20epstein%20files-CryptoniteCTF/image%208.png)

TACHYON{PDF_St3g4n0gr4phy_i5_kool_5tau36}
