# EZ-Des- dreamhack

![image.png](EZ-Des-%20dreamhack/image.png)

- Sau khi tải về mọi người sẽ nhận được 3 file

 

![image.png](EZ-Des-%20dreamhack/image%201.png)

- Bài sẽ cho chúng ta 1 web để tải file ciphertext.txt và keys.txt. Mỗi block 8 byte (DES) — tổng cộng **50 block** (400 bytes)
- Mã hóa mỗi block bằng **“Triple‑DES EDE” nhưng 3 lần dùng cùng một key** → thực chất chỉ còn **Single DES (ECB)** cho từng block
- Thứ tự key/khối bị xáo bằng random.shuffle(idxs) với seed = int(time.time()**)**, và seed bị lộ qua header X-Used-Seed (và mtime của file)
- Vì thế cách giải bài này là mình sẽ brute‑force 50 key/khối, chọn decrypt nào ra **ASCII có nghĩa** (unique) ⇒ ráp lại toàn văn/flag

Chia ciphertext thành 50 block 8B.

Với **mỗi block i**, thử giải bằng **50 key** trong keys.txt.

Chọn kết quả nào **in được/ASCII, có nghĩa** (mỗi block của đề này là **duy nhất**, không trùng key).

Sắp xếp theo **vị trí hiện tại** (vì ciphertext giữ thứ tự block, chỉ key bị xáo) ⇒ ráp toàn văn/flag.

mọi người sẽ chuyển file ciphertext.txt mình có thành dạng hex và lưu cipher1.txt nhé.

![image.png](EZ-Des-%20dreamhack/image%202.png)

```python
from Crypto.Cipher import DES
import binascii
import string

def is_printable(bs: bytes) -> bool:
    try:
        s = bs.decode('latin-1')
    except UnicodeDecodeError:
        return False
    allowed = set(string.printable)
    return all(ch in allowed for ch in s)

def des_decrypt_block(block: bytes, key: bytes) -> bytes:
    return DES.new(key, DES.MODE_ECB).decrypt(block)

def parse_hex_to_bytes(hex_with_spaces: str) -> bytes:
    hx = ''.join(hex_with_spaces.split())
    return binascii.unhexlify(hx)

def main(keys_path='keys.txt', cipher_hex_path='cipher1.txt'):
    keys = [bytes.fromhex(line.strip()) for line in open(keys_path) if line.strip()]
    assert len(keys) == 50 and all(len(k)==8 for k in keys)

    hex_str = open(cipher_hex_path, 'r', encoding='utf-8').read()
    c = parse_hex_to_bytes(hex_str)
    assert len(c) == 400 and len(c) % 8 == 0
    blocks = [c[i:i+8] for i in range(0, len(c), 8)]

    chosen = [None]*len(blocks)
    for i, cb in enumerate(blocks):
        hit = None
        for k in keys:
            pt = des_decrypt_block(cb, k)
            if is_printable(pt):
                hit = pt
                break
        if not hit:
            raise RuntimeError(f'No printable candidate for block {i}')
        chosen[i] = hit

    plaintext = b''.join(chosen)
    print(plaintext.decode('latin-1', 'replace'))

if __name__ == '__main__':
    main()
```

DH{Mistress_Sarah_Darling_inadvertently_bestowed_a_ring_of_considerable_value_upon_the_coin_cup_of_a_homeless_gentleman_known_as_Billy_Ray_Harris_However_Billy_displaying_admirable_integrity_sought_out_Sarah_to_return_the_precious_item_In_gratitude_Sarah_initiated_a_fundraising_campaign_which_has_since_enabled_Billy_to_acquire_both_a_residence_and_gainful_employment_UwUwUwUwUwUwUwUwUwUwUwUwUwUwU_}
