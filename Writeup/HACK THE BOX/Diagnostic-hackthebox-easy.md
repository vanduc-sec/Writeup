# Diagnostic-hackthebox-easy

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image.png)

- Chúng ta sẽ bắt đầu tải về bằng lệnh: wget [http://83.136.250.108:39124/layoffs.doc](http://83.136.250.108:39124/layoffs.doc) , dựa vào host đề bài cho và ở phần miêu tả.
- Đối với những bài liên quan đến file office như này thì ae nên dùng oletools, lúc đầu mình có làm theo cách giải nén ra nhưng mà lú quá nó khá nhiều file á nên thôi chúng ta sẽ dùng oletools để làm bài này.
- Đầu tiên là chúng ta sẽ xem tổng quát file bằng lệnh:  oleid layoffs.doc

➜  hackthebox oleid layoffs.doc
oleid 0.60.1 - [http://decalage.info/oletools](http://decalage.info/oletools)
THIS IS WORK IN PROGRESS - Check updates regularly!
Please report any issue at [https://github.com/decalage2/oletools/issues](https://github.com/decalage2/oletools/issues)

Filename: layoffs.doc
--------------------+--------------------+----------+--------------------------
Indicator           |Value               |Risk      |Description
--------------------+--------------------+----------+--------------------------
File format         |MS Word 2007+       |info      |
|Document (.docx)    |          |
--------------------+--------------------+----------+--------------------------
Container format    |OpenXML             |info      |Container type
--------------------+--------------------+----------+--------------------------
Encrypted           |False               |none      |The file is not encrypted
--------------------+--------------------+----------+--------------------------
VBA Macros          |No                  |none      |This file does not contain
|                    |          |VBA macros.
--------------------+--------------------+----------+--------------------------
XLM Macros          |No                  |none      |This file does not contain
|                    |          |Excel 4/XLM macros.
--------------------+--------------------+----------+--------------------------
External            |1                   |HIGH      |External relationships
Relationships       |                    |          |found: oleObject - use
|                    |          |oleobj for details
--------------------+--------------------+----------+--------------------------

- Sau khi dùng oleid thì mọi người thấy phần External Relationships được đánh giá là mức high và kém theo dòng chúng ta nên dùng oleobj nên chúng ta sẽ dùng nó xem sao.

➜  hackthebox oleobj layoffs.doc
oleobj 0.60.1 - [http://decalage.info/oletools](http://decalage.info/oletools)
THIS IS WORK IN PROGRESS - Check updates regularly!
Please report any issue at [https://github.com/decalage2/oletools/issues](https://github.com/decalage2/oletools/issues)

---

File: 'layoffs.doc'
Found relationship 'oleObject' with external link [http://diagnostic.htb:39124/223_index_style_fancy.html](http://diagnostic.htb:39124/223_index_style_fancy.html)!

- Mọi người có thể thấy nó có một mối liên hệ với 1 link lạ nên chúng ta sẽ xem link này là gì

[http://83.136.250.108:39124/223_index_style_fancy.html](http://83.136.250.108:39124/223_index_style_fancy.html) 

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%201.png)

- Ko thấy gì nên mình sẽ xem thử view page source bằng cách nhấp chuột phải và chọn hoặc ctrl+u

|  | <script>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           </script> |
|  |  |
- Chúng ta sẽ nhận được đoạn mã base64 mọi người hãy thử decode ra, mọi người có thể lên cyberchef để decode nhé

![image.png](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox/image%202.png)

- Ở đây mình sẽ chỉ decode đoạn đầu vì đoạn sau mình decode ra thì nó cũng không có j hết, ở đây chúng ta sẽ thấy là mình chỉ cần ghép mảng các chữ cái  theo file.

HTB{msDt_4s_A_pr0toC0l_h4nDl3r...sE3Ms_b4D}

[An unusual sighting-ctftryout-hackthebox](Diagnostic-hackthebox-easy/An%20unusual%20sighting-ctftryout-hackthebox.md)
