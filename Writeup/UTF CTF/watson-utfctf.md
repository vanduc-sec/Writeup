# watson-utfctf

![image.png](Last%20Byte%20Standing-utfctf/image.png)

Bài này cung cấp cho chúng ta khá nhiều file và 1 triage files 

Đề này là một bài **forensics / DFIR** dạng điều tra sự cố sau xâm nhập.

Ý của đề bài, tách từng câu ra thì là:

**“The threat actor was able to escalate privileges.”**

→ Kẻ tấn công **đã leo thang đặc quyền**.

Tức là ban đầu có thể chỉ chiếm được quyền user thường, nhưng sau đó đã lấy được quyền cao hơn như:

- local admin
- SYSTEM
- hoặc quyền domain cao hơn, tùy bối cảnh

Đây là điểm rất quan trọng, vì bài này sẽ xoay quanh việc tìm dấu vết cho thấy:

- chúng vào bằng cách nào,
- rồi **nâng quyền** bằng cách nào,
- sau khi nâng quyền thì làm gì tiếp.

**“We're in the process of containment”**

→ Đội IR đang trong giai đoạn **containment** = cô lập, chặn kẻ tấn công, ngăn lan rộng.

Tức là vụ việc đang được xử lý, và bạn được giao đi phân tích triage.

**“we want you to find a few things on the threat actor.”**

→ Bạn sẽ phải tìm một số thông tin về attacker.

Thông thường kiểu bài này sẽ hỏi các thứ như:

- attacker đã chạy lệnh gì
- dùng công cụ gì
- tải file gì
- tạo persistence thế nào
- privilege escalation diễn ra ra sao
- account nào bị dùng
- process / executable / path nào đáng ngờ
- thời gian xảy ra hành vi đó

**“The triage is the same as the one in ‘Landfall’.”**

→ Bộ dữ liệu dùng để phân tích **giống bài Landfall trước đó**.

Nghĩa là:

- cùng một bộ KAPE triage
- cùng host / cùng incident chain
- nhưng câu hỏi phần này tập trung vào giai đoạn **escalate privileges**

Nói dễ hiểu:

**Landfall** là phần trước của cùng vụ án.

**Watson** là phần tiếp theo, nơi attacker đã đi xa hơn và có quyền cao hơn.

**“Can you read the briefing and solve your part of the case?”**

→ Bạn phải:

1. đọc briefing / mô tả bối cảnh
2. mở bộ triage
3. phân tích artefact
4. trả lời flag / answer cho phần việc của mình

---

## Bản chất bài này là gì?

Đây không phải kiểu exploit trực tiếp, mà là kiểu:

- được cho **Triage Files**
- phải tự đi tìm dấu vết trong:
    - Event Logs
    - Registry artefacts
    - Prefetch
    - Amcache/Shimcache
    - LNK files
    - Scheduled Tasks
    - services
    - PowerShell history / console history
    - process execution evidence
    - file download traces
    - credential dumping traces
    - logon events
    - privilege assignment / special privileges

Vì đề nhấn mạnh **privilege escalation**, nên trọng tâm của bạn nên là các artefact cho thấy:

- ai đăng nhập
- tiến trình nào được chạy
- có dùng token/system/service/task/UAC bypass không
- có dump credential không
- có dùng công cụ như mimikatz, PsExec, rundll32, regsvr32, schtasks, sc.exe, powershell, cmd không
- có xuất hiện event chứng minh quyền đã tăng không

---

## “Triage Files” là gì?

Link này là file ZIP chứa bộ **KAPE triage**.

KAPE thường thu thập rất nhiều artefact điều tra nhanh từ Windows, ví dụ:

- Windows Event Logs (`.evtx`)
- Registry hives
- Prefetch
- browser / execution traces
- SRUM / BAM / RecentFiles
- Scheduled Tasks
- PowerShell logs / history
- file system metadata

Tức là bạn **không có full disk image**, mà có bộ dữ liệu rút gọn đủ để điều tra nhanh.

---

## Mục tiêu thật sự của bài

Từ lời đề, khả năng rất cao bài sẽ muốn bạn xác định các điểm như:

- privilege escalation xảy ra **khi nào**
- attacker dùng **kỹ thuật nào**
- attacker chạy **binary / command** nào để nâng quyền
- account nào bị lợi dụng
- tiến trình cha/con liên quan
- có dump credential hay enumerate quyền không
- attacker sau khi leo thang quyền thì làm gì tiếp

---

---

## Khi bắt đầu làm, bạn nên ưu tiên gì?

Nếu vào làm thật, thứ tự hợp lý là:

1. **Đọc briefing / câu hỏi cụ thể**
2. Xem trong triage có các thư mục như:
    - EventLogs
    - Registry
    - Prefetch
    - PowerShell
    - Users
3. Tìm timeline quanh lúc attacker hoạt động
4. Săn dấu vết:
    - `4624`, `4625`, `4672`, `4688`
    - PowerShell history
    - suspicious command lines
    - Prefetch của tool lạ
    - credential dumping / admin tools
5. Ghép chain:
    - initial access → execution → privilege escalation → post-exploitation

---

Sau khi phân tích 1 chút về đề bài mình sẽ tiến hành độc 2 fiel txt bài cho trước

```python
➜  utfctf cat briefing\ \(1\).txt
Welcome back agent. Please get us the following:

Checkpoint A: The threat actor deleted a word document containing secret
project information. Can you retrieve it and submit the name of the project?

Checkpoint B: The threat actor installed a suspicious looking program that
may or may not be benign. Retrieve the SHA1 Hash of the executable.

Hint:
- Checkpoint A's password is strictly uppercase
- Checkpoint B's password is the SHA1 Hash%                                                                             ➜  utfctf cat how-to-solve\ \(1\).txt
To obtain the flag, you must pass through all of the checkpoints. The
checkpoints have all been encrypted with a password. The password for each
checkpoint can be found by answering the problems in the Briefing. After
completing each checkpoint, you will be given a part of the flag. Combine the
checkpoint hashes along with hyphens to obtain the flag.

Example: utflag{DEAD-BEEF}%                                                                                             ➜  utfctf
```

Bạn có 2 file mô tả:

### `briefing (1).txt`

Nó nói bạn phải giải **2 câu hỏi điều tra**:

### Checkpoint A

> The threat actor deleted a word document containing secret project information. Can you retrieve it and submit the name of the project?
> 

Ý là:

- attacker đã **xóa một file Word**
- file đó chứa thông tin bí mật về một **project**
- nhiệm vụ của bạn là:
    1. tìm lại file Word đã bị xóa
    2. đọc nội dung hoặc metadata của nó
    3. lấy ra **tên project**
- tên project đó sẽ là **mật khẩu mở checkpoint A**

Hint:

> Checkpoint A's password is strictly uppercase
> 

Tức là mật khẩu phải nhập **toàn bộ chữ in hoa**.

Ví dụ nếu project là `Watson` thì password phải nhập là `WATSON`.

---

### Checkpoint B

> The threat actor installed a suspicious looking program that may or may not be benign. Retrieve the SHA1 Hash of the executable.
> 

Ý là:

- attacker đã cài một chương trình đáng ngờ
- bạn phải tìm ra **file executable** của chương trình đó
- rồi tính hoặc lấy **SHA1 hash** của file `.exe`
- chính giá trị SHA1 này sẽ là **mật khẩu mở checkpoint B**

Hint:

> Checkpoint B's password is the SHA1 Hash
> 

Tức là password của checkpoint B **chính là chuỗi SHA1**, ví dụ kiểu:

`a94a8fe5ccb19ba61c4c0873d391e987982fbbd3`

---

## 2. `how-to-solve (1).txt` đang nói gì?

Nó bảo cơ chế lấy flag như sau:

> To obtain the flag, you must pass through all of the checkpoints.
> 

Tức là:

- muốn ra flag cuối cùng
- phải mở được **tất cả checkpoint**

> The checkpoints have all been encrypted with a password.
> 

Tức là:

- `checkpointA (1).zip`
- `checkpointB.zip`
    
    đều là file zip có password
    

> The password for each checkpoint can be found by answering the problems in the Briefing.
> 

Tức là:

- password không cho sẵn
- bạn phải **phân tích forensic** để tìm ra đáp án câu hỏi trong briefing
- đáp án đó chính là password

> After completing each checkpoint, you will be given a part of the flag.
> 

Tức là:

- sau khi giải đúng và mở được từng checkpoint
- bên trong sẽ có một **mảnh flag**
- thường là một đoạn hash / chuỗi ngắn

> Combine the checkpoint hashes along with hyphens to obtain the flag.
> 

Tức là:

- mỗi checkpoint sẽ cho ra 1 đoạn
- ghép chúng lại bằng dấu

Ví dụ:

`utflag{DEAD-BEEF}`

nghĩa là:

- checkpoint A cho `DEAD`
- checkpoint B cho `BEEF`
- flag cuối là `utflag{DEAD-BEEF}`

Đầu tiên mình sẽ tiến hành khai thác checkpoint A trước vì có vẻ là dễ hơn

Mình sẽ vào recycle nơi lưu những file đã xóa để tìm file word

![image.png](Last%20Byte%20Standing-utfctf/image%201.png)

Ở đây mọi người sẽ thấy có file word R07YGFU bên trong có file dự án HOOKEM khá là khớp với miêu tả của pass checkpoint A rồi

pass:HOOKEM

Mình sẽ giải nén fiel check a xem được không

```python
➜  utfctf unzip checkpointA\ \(1\).zip
Archive:  checkpointA (1).zip
   creating: Checkpoint A/
[checkpointA (1).zip] Checkpoint A/A.txt password:
password incorrect--reenter:
 extracting: Checkpoint A/A.txt
➜  utfctf cd Checkpoint\ A
➜  Checkpoint A cat A.txt
pr1v473_3y3%                                                                                                            ➜  Checkpoint A
```

Ở đây mk đã có được phần đầu flag rồi tiếp theo là checkpoint B bài này nó là yêu cầu tìm fiel .exe và sha1 của file này

Đầu tiên thì vì đẻ tìm file exe thì mình vào prefetch 

![image.png](Last%20Byte%20Standing-utfctf/image%202.png)

Ở đây mk có thấy fiel calc.exe khá đang nghi nó như là giải dạng fiel caculater.exe của máy tính nạn nhân nhưng mà vì pf thì thường không có sha1 nên mình nghĩ đến amcache.hve vì nó sẽ lưu khá nh thứ của file

![image.png](Last%20Byte%20Standing-utfctf/image%203.png)

Vào inventrory file mọi người sẽ thấy ngay đường dẫn của fiel này chắc chắc có vấn đề tiếp đó là có sha1 luôn 

67198a3ca72c49fb263f4a9749b4b79c50510155

Giải nén file zip thứ 2

```python
➜  utfctf unzip checkpointB.zip
Archive:  checkpointB.zip
   creating: Checkpoint B/
[checkpointB.zip] Checkpoint B/B.txt password:
 extracting: Checkpoint B/B.txt
➜  utfctf cd Checkpoint\ B
➜  Checkpoint B cat B.txt
m1551n6_l1nk%                                                                                                           ➜  Checkpoint B

```

flag:utflag{pr1v473_3y3-m1551n6_l1nk}
