# BlueSky Ransomware Lab-cyberdefen

Knowing the source IP of the attack allows security teams to respond to potential threats quickly. Can you identify the source IP responsible for potential port scanning activity?

87.96.21.84

ở đây chúng ta thấy có rất nhiều gói tin được chạy bởi 2 ip và có rất nh gói tin từ .84 về .81 với nỗ luawj scanport

During the investigation, it's essential to determine the account targeted by the attacker. Can you identify the targeted account username?

sa

ở đây ta có thấy giao thức tds của mssql có thể thấy hacker dang dùng bruttce force mssql 

tìm gói tin login là có thẻ thấy user name và password

We need to determine if the attacker succeeded in gaining access. Can you provide the correct password discovered by the attacker?

cyb3rd3f3nd3r$

Attackers often change some settings to facilitate lateral movement within a network. What setting did the attacker enable to control the target host further and execute further commands?

xp_cmdshell

Đối với câu này thì việc thiết lập cài đặt sẽ là lúc bắt đầu có quyền điều khiên nên sẽ ưu tiên tìm các gói respne của các gói tin sau khi  đăng nhập đàu tiên

Process injection is often used by attackers to escalate privileges within a system. What process did the attacker inject the C2 into to gain administrative privileges?

winlogon.exe

![image.png](BlueSky%20Ransomware%20Lab-cyberdefen/image.png)

Following privilege escalation, the attacker attempted to download a file. Can you identify the URL of this file downloaded?

sau khi ngụy trang thành công có quyền truy cập cao hơn lúc này hacker sẽ dùng http tải file về 

[http://87.96.21.84/checking.ps1](http://87.96.21.84/checking.ps1)

Understanding which group Security Identifier (SID) the malicious script checks to verify the current user's privileges can provide insights into the attacker's intentions. Can you provide the specific Group SID that is being checked?

S-1-5-32-544

trong file tải xuống đầu tiên có bước đầu kiểm tra xem user người dùng thuộc nhóm nào giúp quá trình hacker làm việc dễ dàng hơn

Windows Defender plays a critical role in defending against cyber threats. If an attacker disables it, the system becomes more vulnerable to further attacks. What are the registry keys used by the attacker to disable Windows Defender functionalities? Provide them in the same order found.

DisableAntiSpyware,DisableRoutinelyTakingAction,DisableRealtimeMonitoring,SubmitSamplesConsent, SpynetReporting

tìm luôn trong file đầu tiên vì lúc nó tải lần đầu sẽ phải vô hiệu hóa luôn vì nêu ko sẽ ko thể tải file được

Can you determine the URL of the second file downloaded by the attacker?[http://87.96.21.84/del.ps11](http://87.96.21.84/del.ps1)

Identifying malicious tasks and understanding how they were used for persistence helps in fortifying defenses against future attacks. What's the full name of the task created by the attacker to maintain persistence?

\Microsoft\Windows\MUI\LPupdate

đối với các câu duy trì kêt snoois thì thường hacker sẽ thiết lập ngay khi tiari được file đầu tiên vì để duy trì và tiến hành các file khác

Based on your analysis of the second malicious file, What is the MITRE ID of the main tactic the second file tries to accomplish?

TA0005

What's the invoked PowerShell script used by the attacker for dumping credentials?

Invoke-PowerDump.ps1

đây là 1 mã nguồn mã vô cùng quan trọng trong bảo mật dùng để trích xuất hash mật khẩu trong cơ sở dữ liệu của hệ điều hành window

Understanding which credentials have been compromised is essential for assessing the extent of the data breach. What's the name of the saved text file containing the dumped credentials?

hashes.txt

Knowing the hosts targeted during the attacker's reconnaissance phase, the security team can prioritize their remediation efforts on these specific hosts. What's the name of the text file containing the discovered hosts?

extracted_hosts.txt

After hash dumping, the attacker attempted to deploy ransomware on the compromised host, spreading it to the rest of the network through previous lateral movement activities using SMB. You’re provided with the ransomware sample for further analysis. By performing behavioral analysis, what’s the name of the ransom note file?

After hash dumping, the attacker attempted to deploy ransomware on the compromised host, spreading it to the rest of the network through previous lateral movement activities using SMB. You’re provided with the ransomware sample for further analysis. By performing behavioral analysis, what’s the name of the ransom note file?

# DECRYPT FILES BLUESKY #

virustotal trong phần hành vi có các file bị drop với việc có comment mà file để lại và chèn theem extension vào cuois file

In some cases, decryption tools are available for specific ransomware families. Identifying the family name can lead to a potential decryption solution. What's the name of this ransomware family?

bluesky
