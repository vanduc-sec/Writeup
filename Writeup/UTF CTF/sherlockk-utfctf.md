# sherlockk-utfctf

![image.png](Last%20Byte%20Standing-utfctf/image.png)

Bài này tiếp tục là 1 dạng IR với giống 2 bài trước mk sẽ phần tích đề bài 1 chút

Đề này là **một bài digital forensics / incident response kiểu “tiếp nối vụ án”**. Tức là bạn **không exploit**, không chạy malware để lấy flag ngay, mà phải **điều tra bộ triage Windows** rồi trả lời các câu hỏi mà briefing yêu cầu. đây là **challenge thứ 3** trong chuỗi **Landfall → Watson → Sherlockk**, và cả 3 đều dùng **cùng một bộ triage KAPE**. Ở Sherlockk, bạn phải tìm ra 3 manh mối/IOC rồi dùng chúng làm mật khẩu mở các checkpoint zip để ghép flag.

Giải thích từng phần của đề:

**“We’re almost done agent”**

Câu này cho biết bạn đang ở **giai đoạn cuối của một vụ điều tra đã diễn ra trước đó**. Nghĩa là các hoạt động của attacker đã bắt đầu từ các challenge trước, còn Sherlockk tập trung vào việc **đi nhặt dấu vết còn sót lại**.

**“identify some Indicators of Compromise (IOCs) left by the threat actor”**

IOC là **dấu hiệu xâm nhập**. Trong bài kiểu này, IOC có thể là:

- URL tải file
- tên file đáng ngờ
- hash MD5/SHA1
- script attacker để lại
- ghi chú, artifact trong browser, MFT, Recycle Bin, Downloads, registry, PowerShell history...

Tức là đề muốn bạn **lần ngược hành vi attacker qua dấu vết số** chứ không phải brute force.

**“The triage is the same as the one in ‘Landfall’ and ‘Watson’”**

Câu này cực quan trọng. Nó nghĩa là:

- Bạn được đưa **cùng bộ evidence** như 2 bài trước
- Những gì attacker làm ở Landfall/Watson **có liên quan trực tiếp** đến Sherlockk
- Bạn nên giữ tư duy “timeline”: attacker đã làm gì trước, dùng user nào, dùng browser nào, tải gì, xóa gì, để lại gì

**“Can you read the briefing and solve your part of the case?”**

Nghĩa là trong file triage sẽ có một hoặc nhiều file kiểu `briefing.txt`, `how-to-solve.txt`, `checkpointA.zip`, `checkpointB.zip`, `checkpointC.zip`.

Bạn phải:

1. Đọc briefing để biết **mỗi checkpoint đang hỏi cái gì**
2. Tìm đúng artifact trong triage
3. Biến kết quả tìm được thành **password**
4. Mở zip checkpoint
5. Lấy từng phần flag rồi ghép lại

Cụ thể, bản chất của Sherlockk là:

**Checkpoint A**

Đề bắt bạn tìm **một file tải từ “online text storage site”**.

Nghe mô tả thôi là đã nên nghĩ tới:

- paste site: pastes.io, pastebin, hastebin...
- artifact nằm trong **browser history / download history**
- thứ cần lấy có thể là **full URL tải xuống**

**Checkpoint B**

Đề bảo lấy **nội dung một ghi chú liên quan đến admin user**, trong đó có **nhiều item được liệt kê**, rồi ghép các item bằng dấu `-` để làm password.

Ý nghĩa forensic ở đây là:

- note có thể đã bị xóa
- có thể không còn nằm “bình thường” trong filesystem
- bạn cần kiểm tra artifact như **$MFT**, Recycle Bin, shortcut, recent files, Documents, carved text...

**Checkpoint C**

Đề yêu cầu tìm **file enumeration script mà attacker đã tải về**, rồi lấy **MD5** của nó làm password.

Đây là câu rất DFIR:

- “enumeration script” thường là script liệt kê file/quyền/hệ thống
- có thể nằm ở Downloads, Temp, browser download history, jump lists, Prefetch, shellbags...
- sau khi xác định đúng file, bạn phải hash nó bằng MD5

Nói ngắn gọn, **đề đang kiểm tra 4 kỹ năng chính**:

1. **Đọc briefing đúng cách**
    
    Không phải cứ lục bừa; phải hiểu câu hỏi đang ám chỉ artifact nào.
    
2. **Biết triage Windows nên xem đâu trước**
    
    Browser history, Downloads, Recycle Bin, `$MFT`, Documents, PowerShell history, registry, hash file.
    
3. **Biết biến artifact thành đáp án theo format đề yêu cầu**
    
    Ví dụ:
    
- full URL
- list ghép bằng
- hash MD5/SHA1
- có thể phân biệt hoa thường nếu đề nhạy format
1. **Biết ghép nhiều checkpoint để ra flag cuối**
    
    Flag không ở sẵn; mỗi checkpoint chỉ cho một phần.
    

Nếu nhìn theo tư duy điều tra, bài này gần như đang nói:

> “Attacker đã vào máy, tải một số thứ, xóa một số thứ, để lại một số IOC. Bạn hãy dùng bộ KAPE triage để dựng lại các hành động đó và lấy ra 3 bằng chứng quan trọng.”
> 

Về chiến lược làm bài, thứ tự hợp lý thường là:

- mở thư mục challenge, đọc `briefing.txt`
- xem có `checkpointA/B/C.zip` và `how-to-solve.txt` không
- ưu tiên artifact dễ ra đáp án trước:
    - browser history
    - Downloads
    - Recycle Bin
- sau đó mới sang artifact sâu hơn:
    - `$MFT`
    - registry / Amcache / Shimcache / Prefetch nếu cần
- khi xác định được file đúng, tính hash đúng thuật toán đề yêu cầu

TIếp đến mình sẽ đọc file briefing.txt

```python
➜  utfctf cat briefing\ \(1\).txt how-to-solve\ \(1\).txt
Welcome back agent. Please get us the following:

Checkpoint A: The threat actor deleted a word document containing secret
project information. Can you retrieve it and submit the name of the project?

Checkpoint B: The threat actor installed a suspicious looking program that
may or may not be benign. Retrieve the SHA1 Hash of the executable.

Hint:
- Checkpoint A's password is strictly uppercase
- Checkpoint B's password is the SHA1 HashTo obtain the flag, you must pass through all of the checkpoints. The
checkpoints have all been encrypted with a password. The password for each
checkpoint can be found by answering the problems in the Briefing. After
completing each checkpoint, you will be given a part of the flag. Combine the
checkpoint hashes along with hyphens to obtain the flag.

Example: utflag{DEAD-BEEF}%            
```

## 5. Logic tổng thể của đề

Bài này đang tách thành 3 nhóm artifact:

### A — Dấu vết trên web / tải file

Cần tìm **URL đầy đủ**

### B — Dấu vết file note đã bị xóa

Cần khôi phục **nội dung note**

### C — Dấu vết file script attacker tải về

Cần xác định **file đúng** rồi tính **MD5**

Tức là đề kiểm tra bạn ở 3 kỹ năng:

- đọc artifact trình duyệt
- khôi phục file/nội dung đã xóa
- nhận diện file đáng ngờ và băm hash

Để làm bài này đầu tiên mình sẽ khái thác về dấu vế url trước đối với cái này thì mk sẽ ưu tiên tìm trong chorme history, brower history, …

![image.png](Last%20Byte%20Standing-utfctf/image%201.png)

Ở đây mọi người sẽ thấy có phần download đang tải 1 file nhy8LSzl.txt từ trang web pasters.ip trông rất là khả nghi nên là mình sẽ lấy luôn nó làm mật khẩu cho file zip A 

`http://pastes.io/download/nhy8LSzI`
  

```python
➜  utfctf unzip checkpointA.zip
Archive:  checkpointA.zip
   creating: Checkpoint A/
[checkpointA.zip] Checkpoint A/A.txt password:
 extracting: Checkpoint A/A.txt
➜  utfctf cd Checkpoint\ A
➜  Checkpoint A cat A.txt
b45k3rv1ll3
```

p1: b45k3rv1ll3

Tiếp đến là tìm md5 của file scrip, ở đây cũng trong user adminstrator các bạn vào phần downloads và thấy ngáy có file [script.sh.sh](http://script.sh.sh) là chính là đoạn scrip lạ

![image.png](Last%20Byte%20Standing-utfctf/image%202.png)

lấy md5 của nó

e86475121f231c02c4a63bd0915b9dff

Giai nén ra part 2 falg

```python
➜  utfctf unzip checkpointC.zip
Archive:  checkpointC.zip
   creating: Checkpoint C/
[checkpointC.zip] Checkpoint C/C.txt password:
 extracting: Checkpoint C/C.txt
➜  utfctf cd c
cd: no such file or directory: c
➜  utfctf cd Checkpoint\ C
➜  Checkpoint C cat C.txt
4r7hur_c0n4n_d0yl3%
```

4r7hur_c0n4n_d0yl3

Tiếp đến fiel note bị xóa thì chúng ta sẽ phải khai thác tiêp ở 

Tập `$MFT`tin (Master File Table) là một tập tin ẩn của Windows chứa thông tin về tất cả các tập tin trong hệ thống cùng với một số siêu dữ liệu và vị trí vật lý của chúng.

Đối với các tập tin nhỏ, nó thậm chí có thể chứa toàn bộ nội dung của tập tin đó.

Nó cũng chứa dữ liệu về một số tệp đã bị xóa, có nghĩa là nó có thể được sử dụng để khôi phục các tệp đã xóa.

Ghi chú mà chúng ta đang tìm kiếm có lẽ là một tập tin văn bản nhỏ, vì vậy có lý do chính đáng để tin rằng chúng ta sẽ tìm thấy nội dung của nó ở đó.

Để phân tích tập `$MFT`tin, chúng ta sẽ sử dụng MFTExplorer từ bộ công cụ của Eric Zimmerman

![image.png](Last%20Byte%20Standing-utfctf/image%203.png)

Ở đay mọi người sẽ có thể nhìn thấy trong file adminstrator note có grocery list với :Lettuce-Cabbage-Carrots

```python
 briefing.txt:Zone.Identifier   checkpointB.zip                   checkpointC.zip:Zone.Identifier
➜  utfctf unzip checkpointB.zip
Archive:  checkpointB.zip
   creating: Checkpoint B/
[checkpointB.zip] Checkpoint B/B.txt password:
password incorrect--reenter:
 extracting: Checkpoint B/B.txt
➜  utfctf cd Checkpoint\ B
➜  Checkpoint B cat B.txt
3l3m3n74ry%                                                                                                             ➜  Checkpoint B
```

flag:utflag{b45k3rv1ll3-3l3m3n74ry-4r7hur_c0n4n_d0yl3}
