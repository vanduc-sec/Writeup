# Phreaky-htb-med(pcap-smtp(email exfiltration))

![image.png](Phreaky-htb-med%28pcap-smtp%28email%20exfiltration%29%29/image.png)

- `192.168.68.108 (phreak-ubuntu01)` gửi nhiều email qua **SMTP** tới `192.168.68.111 (mailserver-phreak)`.
- Mỗi email có:
    - 1 file `.eml` = nội dung email
    - 1 file `.zip` = file đính kèm
- Tên lặp `SecureFile[1]`, `SecureFile[2]`, ... cho thấy dữ liệu bị **chia nhỏ thành nhiều phần** rồi gửi đi.

Tiếp đến mình tab message thì thấy có mật khẩu kèm theo mỗi file zip

![image.png](Phreaky-htb-med%28pcap-smtp%28email%20exfiltration%29%29/image%201.png)

Bây giờ mình sẽ unzip từng file ra xem có j bên trong

```python
➜  extracted_output ls
phreaks_plan.pdf.part1   phreaks_plan.pdf.part13  phreaks_plan.pdf.part3  phreaks_plan.pdf.part7
phreaks_plan.pdf.part10  phreaks_plan.pdf.part14  phreaks_plan.pdf.part4  phreaks_plan.pdf.part8
phreaks_plan.pdf.part11  phreaks_plan.pdf.part15  phreaks_plan.pdf.part5  phreaks_plan.pdf.part9
phreaks_plan.pdf.part12  phreaks_plan.pdf.part2   phreaks_plan.pdf.part6
➜  extracted_output
```

Sau khi giải nén thì mình thấy có vẻ như có 1 file pdf bị chia thành nhiều phần tiếp mình sẽ nối và đọc thử

![image.png](Phreaky-htb-med%28pcap-smtp%28email%20exfiltration%29%29/image%202.png)

HTB{Th3Phr3aksReadyT0Att4ck}
