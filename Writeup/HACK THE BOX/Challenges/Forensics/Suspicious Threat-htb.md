# Suspicious Threat-htb

![image.png](Suspicious%20Threat-htb/image.png)

- Chúng ta sẽ kết nối đến may chủ bằng ssh.

![image.png](Suspicious%20Threat-htb/image%201.png)

- Để điều tra về lỗi thư viện thì chúng ta sẽ dùng: cat /etc/ld.so.preload

![image.png](Suspicious%20Threat-htb/image%202.png)

- Tệp này xác nhận rằng libc.hook.so.6 đã được tải trước. Điều này rất bất thường và cho thấy thư viện này đang chặn các lệnh gọi hệ thống — một hành vi phù hợp với rootkit

![image.png](Suspicious%20Threat-htb/image%203.png)

- Mình thử đọc thì nó ra những kí tự lạ

stat /lib/x86_64-linux-gnu/libc.hook.so.6

![image.png](Suspicious%20Threat-htb/image%204.png)

- Mình kiểm tra tính chất đáng ngờ của nó và chuẩn bị vô hiệu hóa nó, và tìm các chuỗi lạ

mv /etc/ld.so.preload /etc/ld.so.preload.bak

![image.png](Suspicious%20Threat-htb/image%205.png)

HTB{Us3rL4nd_R00tK1t_R3m0v3dd!}
