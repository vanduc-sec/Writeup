# Crack the Gate 2

![image.png](Crack%20the%20Gate%202/image.png)

Đây là 1 bài web yêu cầu mình phải vượt quá giới hạn nhập mật khẩu sai trong 1 khoảng thời gian của trang web với email và 1 list mật khẩu trong đó cố 1 mật khẩu là đúng

![image.png](Crack%20the%20Gate%202/image%201.png)

Ở đây mình chỉ nhập sai 1 lần đến lần thứ 2 là đã bị khóa luôn vì vậy để mà có thể thử hết các mật khẩu không bị khóa thì mỗi lần thử mật khẩu chúng ta sẽ cần giả mạo 1 địa chỉ ip khác nhau 

Mình sẽ sự dụng trường `X-Forwarded-For` trong header http, khi mà chúng ta gửi gói tin lên server thì server sẽ nhìn vào trường này để xem ip nguồn là bao nhiêu nếu chúng ta thao túng được trường này thì mỗi lần gửi 1 gói tin chúng ta sẽ có địa chỉ ip nguồn khác nhau và như thế thì mình sẽ không bị khóa nữa

![image.png](Crack%20the%20Gate%202/image%202.png)

Đầu tiên thì mọi người chọn 1 gói tin và gửi đến Intruder

![image.png](Crack%20the%20Gate%202/image%203.png)

Sau đó thì mọi người thêm trường X-Forwarded-For và bôi đen 2 vị trí là phần ip và password rồi nhấn Add § để chúng ta tiến hành tự động thay đổi ip và mật khẩu mỗi lần 

![image.png](Crack%20the%20Gate%202/image%204.png)

- **Payload type:** Chọn `Numbers`
- Ở mục Payload configuration, cấu hình như sau:
    - **Type:** Sequential
    - **From:** `1`
    - **To:** `20`
    - **Step:** `1`

Vì danh sách mật khẩu chúng ta có 20 mật khẩu nên mình sẽ đi từ 1-20

![image.png](Crack%20the%20Gate%202/image%205.png)

Tiếp cấu hình danh sách `password` mọi người chọn vào `Load….` và tải file mật khẩu mà bài đã cấp lên 

Sau đó là chúng ta sẽ ấn vào nút `start attack`

![image.png](Crack%20the%20Gate%202/image%206.png)

Như mọi người thấy ở gói tin số `14` với mật khẩu là: `4muRBR7J` có độ dài gói tin trả về lớn hơn các gói tin khác và đó chính là gói tin chứa cờ

`academy{xff_byp4ss_brut3_86353db7}`