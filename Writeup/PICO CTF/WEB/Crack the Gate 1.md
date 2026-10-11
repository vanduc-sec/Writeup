# Crack the Gate 1

Bản chất & Ví dụ: - Web gate: Trang chỉ cho qua khi request thỏa điều kiện.- Encoding hint: Tên/chuỗi có thể gợi ý cần decode/transform.- Header manipulation: Gate đôi khi dựa vào header như User-Agent/Referer/custom header.
Hệ sinh thái kiến thức: - Web gate- ROT/encoding hint- Header manipulation- Portal logic- Request inspection
Trạng thái: Chưa bắt đầu
Trạng thái 1: Chưa bắt đầu

![image.png](Crack%20the%20Gate%201/image.png)

Tiếp là 1 bài web mức độ easy của cylab

![image.png](Crack%20the%20Gate%201/image%201.png)

Bài cho ta 1 email nhưng mà không có mật khẩu và bắt chúng ta phải đăng nhập

![image.png](Crack%20the%20Gate%201/image%202.png)

Khi mà mở bằng burp suite thì ngay trong mã nguồn được trả về mình có thấy 1 đoạn comment có vẻ như dev đã viết và quên không xóa

![image.png](Crack%20the%20Gate%201/image%203.png)

Ở đây sau khi giải mã bằng ROT13 thì mình thấy đây là note chúng ta có thể đăng nhập bằng 1 trường header có vẻ như được thiết lập riêng cho người dev

![image.png](Crack%20the%20Gate%201/image%204.png)

Sau khi thêm header của dev vào mình đã đăng nhập thành công và lấy được flag

academy{brut4_f0rc4_dc8f7ab6}