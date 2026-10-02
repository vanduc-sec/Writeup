# crackmepy-rev-picoCTF

### 1. Phân tích luồng Code (Execution Flow)

Nếu bạn đọc từ trên xuống dưới, chương trình sẽ hoạt động theo thứ tự sau:

1. **Khai báo biến:** Khởi tạo biến `bezos_cc_secret` (chứa đoạn mã bí mật / flag đã bị mã hóa) và biến `alphabet` (bảng chứa 94 ký tự chuẩn).
2. **Định nghĩa hàm `decode_secret(secret)`:** Khai báo một hàm có chức năng giải mã đoạn text bí mật. Tuy nhiên, lúc này chương trình *chưa hề* chạy hàm này, nó mới chỉ "ghi nhớ" là hàm này tồn tại.
3. **Định nghĩa hàm `choose_greatest()`:** Khai báo một hàm yêu cầu người dùng nhập 2 số và in ra số lớn hơn.
4. **Thực thi lệnh `choose_greatest()`:** Ở dòng cuối cùng của script, chương trình gọi hàm `choose_greatest()`.

**Cái bẫy ở đây là gì?**
Nếu bạn chạy file Python này, nó sẽ chỉ hỏi bạn nhập vào 2 con số, in ra số lớn hơn, và sau đó kết thúc chương trình. Đoạn flag bị mã hóa và hàm `decode_secret` **hoàn toàn bị bỏ qua**. Mã nguồn của hàm `choose_greatest` thực chất chỉ là một "mồi nhử" (red herring) để đánh lạc hướng những người mới chơi.

### 2. Giải thích chi tiết hàm `decode_secret` và thuật toán ROT47

Để lấy được cờ (flag), mục tiêu thực sự của bạn là phải đọc hiểu và sử dụng được hàm `decode_secret()`. Hàm này sử dụng một thuật toán mã hóa cổ điển có tên là **ROT47** (thuộc họ mật mã dịch chuyển Caesar).

Đây là cách từng dòng code trong hàm hoạt động:

- **`rotate_const = 47`**: Đây là "chìa khóa" (key). Thuật toán sẽ dịch chuyển mỗi ký tự đi 47 bước trong bảng chữ cái.
- **`decoded = ""`**: Tạo một chuỗi rỗng để từ từ ghép các ký tự sau khi đã giải mã xong vào đây.
- **Vòng lặp `for c in secret:`**: Bắt đầu duyệt qua từng ký tự một trong đoạn mã bí mật (`bezos_cc_secret`). Giả sử ký tự đầu tiên là chữ `A`.
    - **`index = alphabet.find(c)`**: Tìm xem chữ `A` nằm ở vị trí số mấy trong chuỗi `alphabet`. Theo bảng `alphabet` được cung cấp, chữ `A` nằm ở vị trí số 32 (index bắt đầu từ 0).
    - **`original_index = (index + rotate_const) % len(alphabet)`**: Đây là công thức toán học cốt lõi của mật mã dịch chuyển.
        - Nó lấy vị trí hiện tại (32) cộng thêm độ dịch chuyển (47) = 79.
        - Phép `% len(alphabet)` (chia lấy phần dư cho 94 - tổng số ký tự của bảng `alphabet`). Bước này cực kỳ quan trọng vì nếu `index + 47` vượt quá con số 94, phép chia lấy dư sẽ giúp vị trí "vòng ngược" lại từ đầu bảng chữ cái, tránh việc chương trình bị lỗi (out of bounds).
        - Trong trường hợp này, 79 chia 94 dư 79.
    - **`decoded = decoded + alphabet[original_index]`**: Lấy ký tự ở vị trí số 79 trong bảng `alphabet` (đó là chữ `p`) và ghép nó vào chuỗi `decoded`.

Chương trình tiếp tục lặp lại quá trình này với các ký tự tiếp theo:

- Ký tự `:` -> Dịch 47 bước -> Giải mã thành `i`
- Ký tự `4` -> Dịch 47 bước -> Giải mã thành `c`
- Ký tự `@` -> Dịch 47 bước -> Giải mã thành `o`

```python
secret1 = "A:4@r%uL`>0c0Abc?FE0g`_47fgaagg6ffN"

# Reference alphabet
alphabet = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"+ \
            "[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

def decode_secret(secret):
    """ROT47 decode

    NOTE: encode and decode are the same operation in the ROT cipher family.
    """

    # Encryption key
    rotate_const = 47

    # Storage for decoded secret
    decoded = ""

    # decode loop
    for c in secret:
        index = alphabet.find(c)
        original_index = (index + rotate_const) % len(alphabet)
        decoded = decoded + alphabet[original_index]

    print(decoded)
decode_secret(secret1)

```
