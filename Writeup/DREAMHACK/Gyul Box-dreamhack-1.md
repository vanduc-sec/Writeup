# Gyul Box-dreamhack-1

**Description
Rootsquare has been arrested by 0xB1nary COMMUNITY agents for hiding confidential documents, slush funds, and golden tangerines in a tangerine box!
But when I opened the box, it was really just tangerines! Where did they hide the secret?
Above all... I don't think this is a single box! I think there's another box inside the box...?Undo (Translated by amazon)**

- Sau khi tải file về chúng ta unzip thì sẽ nhận được 2 file ảnh.
- Khi chúng ta dùng hxd mở file thì ở cuối chúng ta sẽ thấy có final key: 7e1cbabc03360aa6a25d7c85ece471beb2d9517c23f38a1ccec4d0206c0e00f8

![image.png](Gyul%20Box-dreamhack-1/image.png)

- Cái khóa này mình nghĩ chắc sẽ dùng vào việc gì đó chúng  ta sẽ lưu lại dùng sau
- Tiếp theo mình phân tích tiếp đề bài và dòng chữ có trên ảnh thì mình nghĩ file này có thể được ẩn file nào đó bên trong nên mình sẽ dùng:  binwalk -e big_box.jpg, binwalk -e filethu2
- Mọi người sẽ thấy file 4D8AE
- Dùng lệnh:  file 4D8AE thì biết nó file tar, chúng ta sẽ extract nó ra bằng lệnh: tar -xf 4D8AE

![image.png](Gyul%20Box-dreamhack-1/image%201.png)

- Mở ảnh và đọc file txt chúng ta sẽ thấy đây là một dạng mã hóa cộng x với 1 số và chia dư cho 256 và x là 1 byte nên x sẽ chạy từ 0-255 chúng ta sẽ dùng brute force cho x :

```
def decrypt_file():
try:
with open('small_box.enc', 'rb') as f:
enc_data = f.read()
except FileNotFoundError:
print("[-] Không tìm thấy file 'small_box.enc'.")
return
print("[*] Đang dò tìm Key (x)...")
# Thử tất cả key từ 0 đến 255
for x in range(256):
    # Giải mã thử 4 byte đầu tiên: Gốc = (Mã_hóa - x) % 256
    header = bytes([(b - x) % 256 for b in enc_data[:4]])

    # Kiểm tra Magic Bytes của các định dạng phổ biến
    file_type = ""
    if header.startswith(b'\\x89PNG'):
        file_type = "PNG Image"
    elif header.startswith(b'\\x50\\x4B\\x03\\x04'):
        file_type = "ZIP Archive"
    elif header.startswith(b'\\xFF\\xD8\\xFF'):
        file_type = "JPG Image"

    # Nếu tìm thấy Header hợp lệ
    if file_type:
        print(f"[!] TÌM THẤY KEY: x = {x}")
        print(f"[+] Định dạng file gốc: {file_type}")

        # Giải mã toàn bộ file
        dec_data = bytes([(b - x) % 256 for b in enc_data])

        # Lưu file kết quả
        output_name = f"flag_decrypted.{file_type.split()[0].lower()}" # flag_decrypted.png hoặc .zip
        with open(output_name, 'wb') as out:
            out.write(dec_data)

        print(f"[+] Đã lưu file giải mã thành công: {output_name}")
        print(">>> Hãy mở file đó ra để lấy Flag!")
        return

print("[-] Không tìm thấy key phù hợp (hoặc file gốc là định dạng lạ).")
if **name** == "**main**":
decrypt_file()

```

- Sau khi chạy code chúng ta sẽ có file tiếp theo mọi người giải nén ra chúng ta sẽ nhận được 1 file txt và file gyul.png.enc
- Khi mà chúng ta đọc file txt thì mọi người sẽ nhận ra ngay nó đang đề cập đến key mà chúng ta tìm được lúc đầu: Final key : 7e1cbabc03360aa6a25d7c85ece471beb2d9517c23f38a1ccec4d0206c0e00f8
- Vì key này 32 byte nên mk đoán thử nó sẽ là key của mã hóa aes vì key aes hay là 16 hoặc 32 byte
- Mình lên cyberchef decode

![image.png](Gyul%20Box-dreamhack-1/image%202.png)

- và nhận được file png mới mở ra và nhận được flag
    
    ![flag_final.png](Gyul%20Box-dreamhack-1/flag_final.png)
    

[**Binary Badresources-htb-med**](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med.md)
