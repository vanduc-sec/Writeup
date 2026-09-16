# Reminiscent-htb-easy

### Challenge Scenario

Suspicious traffic was detected from a recruiter&#039;s virtual PC. A memory dump of the offending VM was captured before it was removed from the network for imaging and analysis. Our recruiter mentioned he received an email from someone regarding their resume. A copy of the email was recovered and is provided for reference. Find and decode the source of the malware to find the flag.

- Chúng ta tải xuống tệp zip và giải nén, sau đó ta nhận đươc 3 tệp: flounder-pc-memdump.elf, imageinfo.txt, Resume.
- Ta đọc file imageinfo.txt thì thấy thông tin về cấu hình:

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image.png)

- Đọc file txt chúng ta có thể thấy đây như là cấu hình máy àm người ta dùng để dump memory kết hợp với đề bài có nhắc đến bản sao lưu bộ nhớ nên bài này chúng ta sẽ dùng volality 3
- Đầu tiên thì khi mà dùng vol3 thì mình sẽ dùng window.pslist , lênh này sẽ liệt kê cho chúng ta tất cả các tiến trình đang hoạt đùng vào thời điểm mà chúng ta dump memory.

vol3 -f  flounder-pc-memdump.elf window.pslist

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%201.png)

- Tìm một hồi thì mình thấy bài này chỉ đặc biệt ở chỗ nó có 1  chương trình powershell.exe ở cuối.
- Sau khi tìm hiểu thì mình thấy có lệnh dùng để liệt kê các lệnh đã được dùng trên máy khi dump
- vol3 -f flounder-pc-memdump.elf windows.cmdline
- 

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%202.png)

- Sau khi chạy lệnh chúng ta thấy ở cuối có đoạn mã base64
- decode bằng lệnh: ehco ‘mã base64’ | base64 -d

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%203.png)

- Chúng ta có được flag: flag='HTB{$*j0G_y0uR_M3m0rY*$}'.
