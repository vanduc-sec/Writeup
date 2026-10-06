# Power Cookie

Bản chất & Ví dụ: - Role cookie: Cookie như isAdmin=false là dữ liệu client gửi lên.- Broken access control: Server cho phép quyền chỉ vì cookie nói vậy là lỗi phân quyền.- Trust boundary: Quyền thật phải kiểm ở server bằng session/DB, không tin client.
Hệ sinh thái kiến thức: - Role cookie- Admin flag- Broken access control- Trust boundary- Authorization
Trạng thái: Chưa bắt đầu
Trạng thái 1: Chưa bắt đầu

![image.png](<Power Cookie/image.png>)

Tiếp là 1 bài cookie

![image.png](<Power Cookie/image%201.png>)

Bài bắt chúng ta truy cập với tư cách khách nhưng mà vào cũng không có gì

![image.png](<Power Cookie/image%202.png>)

Ở đây nhìn vào gói tin GET /check.php ta có thể thấy 1 điểm đáng ngờ là trường cookie có isAdmin=0

Có vẻ như nó sẽ sử dụng trường cookie này để xác thực xem có phải admin, giờ mình sẽ thay đổi thành admin xem có điều gì xảy ra không bằng cách thay giá trị 0 thành 1 

![image.png](<Power Cookie/image%203.png>)

Bùm chúng ta đã có được flag

academy{gr4d3_A_c00k13_7bcbf214}