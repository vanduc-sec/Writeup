# rogue-htb-med(sharefolder-smb2,3 encrypt-decrypt-session id+session key)

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image.png)

Bài này cho chúng ta 1 file pcap sau khi vào mình có thấy cuộc trò truyền qua giao thức ftb và có tải 1 file zip

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image%201.png)

giờ mình sẽ export ra và xem nó đây là 1 file LSASS minidump nên mình dùng 

```python
pypykatz lsa minidump 3858793632.dmp
```

để xem cáo những credential bị lộ ròi

```python
  rougue pypykatz lsa minidump 3858793632.dmp
INFO:pypykatz:Parsing file 3858793632.dmp
FILE: ======== 3858793632.dmp =======
== LogonSession ==
authentication_id 6361112 (611018)
session_id 3
username rpaker
domainname WS02
logon_server WS02
logon_time 2022-07-04T11:37:24.798200+00:00
sid S-1-5-21-900241500-1566882183-2274020907-1001
luid 6361112
        == MSV ==
                Username: rpaker
                Domain: WS02
                LM: NA
                NT: a9fdfa038c4b75ebc76dc855dd74f0da
                SHA1: 9400ae28448e1364174dde269b2cce1bca9d7ee8
                DPAPI: 0000000000000000000000000000000000000000
        == WDIGEST [611018]==
                username rpaker
                domainname WS02
                password None
                password (hex)
        == Kerberos ==
                Username: rpaker
                Domain: WS02
        == WDIGEST [611018]==
                username rpaker
                domainname WS02
                password None
                password (hex)

```

Ở đây có 1 số hash md4 cái này có thể được dùng để xem smp3 bị encrypt

tiếp thì để có thẻ tính session key thì mọi người phải lấy 

- **username**
 `athomson`
- **domain**
 `CORP`
- **NT hash**
Lấy từ `pypykatz lsa minidump`
`88d84bad705f61fcdea0d771301c3a7d`
- **NTProofStr**
Lấy trong packet `NTLMSSP_AUTH`
 `d047ccdffaeafb22f222e15e719a34d4`
- **Encrypted Random Session Key**
Cũng trong packet `NTLMSSP_AUTH`, dòng `Session Key`
`032c9ca4f6908be613b240062936e2d2`
- **Session ID**

Session Id: 0x0000a00000000015 → 1500000000a00000

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image%202.png)

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image%203.png)

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image%204.png)

```python
import hmac
import hashlib

username = "athomson"
domain = "CORP"
nt_hash_hex = "88d84bad705f61fcdea0d771301c3a7d"
ntproof_hex = "d047ccdffaeafb22f222e15e719a34d4"
enc_random_session_key_hex = "032c9ca4f6908be613b240062936e2d2"
def rc4(key, data):
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    i = j = 0
    out = bytearray()
    for b in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        out.append(b ^ s[(s[i] + s[j]) % 256])
    return bytes(out)

user = username.upper().encode("utf-16le")
dom = domain.upper().encode("utf-16le")
nt_hash = bytes.fromhex(nt_hash_hex)
ntproof = bytes.fromhex(ntproof_hex)
enc_key = bytes.fromhex(enc_random_session_key_hex)

resp_nt_key = hmac.new(nt_hash, user + dom, hashlib.md5).digest()
session_base_key = hmac.new(resp_nt_key, ntproof, hashlib.md5).digest()
exported_session_key = rc4(session_base_key, enc_key)
print("Session Key:", exported_session_key.hex())
```

tiếp mình sẽ dùng code này để giải mã 

```python
➜  rougue python3 1.py
Session Key: 9ae0af5c19ba0de2ddbe70881d4263ac
➜  rougue

```

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image%205.png)

sau khi decrypt sẽ thấy có file pdf thông tin khác hàngmọi nu export ra đọc và có được flag

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image%206.png)

![image.png](rogue-htb-med%28sharefolder-smb2%2C3%20encrypt-decrypt-s/image%207.png)

mọi người export ra và có được flag

HTB{n0th1ng_c4n_st4y_un3ncrypt3d_f0r3v3r}
