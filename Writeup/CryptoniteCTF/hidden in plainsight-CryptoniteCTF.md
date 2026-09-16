# hidden in plainsight-CryptoniteCTF

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image.png)

Bài này cung cấp cho mình một file ảnh jpeg và 1 file .txt đọc theo miêu tả của bài

## Ý nghĩa của đề bài

Tên bài: **Hidden in Plainsight**

Đây là kiểu chơi chữ của **“Hidden in plain sight”** = giấu ngay trước mắt nhưng khó thấy.

Phần mô tả:

> “The Tachyon team ... hidden the ultimate VIP access flag inside, but they buried it under a mountain of digital noise. We managed to intercept the Announcement file, but it looks perfectly normal to us.”
> 

Ý của nó là:

- Flag **nằm trong file Announcement**
- File nhìn **hoàn toàn bình thường**
- Nhưng bên trong có thứ gì đó **không hiện ra bằng mắt thường**
- “digital noise” ở đây thường là:
    - khoảng trắng thừa
    - tab
    - dòng trống
    - ký tự zero-width
    - unicode vô hình
    - metadata / object ẩn
    - dữ liệu nhúng trong phần hex

---

tiếp qua đó mình sẽ tác tab space ra và decode nó 

```python
python3 -c "from pathlib import Path; [print([len(x) for x in line.split('\t')]) for line in Path('Tachyon2.txt').read_text().splitlines()]"
```

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%201.png)

Mọi người sẽ nhìn vào bắt đàu từ số 6 dòng 1 số 9 đó cứ phần deal all ko phải phần dữ liệu ẩn nên mình sẽ đi từ 6 4 1 3 7 5 3 5 6 6 1 3 2 4 5 4 6 5 0

Vì mọi số đều nằm trong khoảng **0 đến 7**, nên nó rất giống dữ liệu được mã thành **3 bit**:

- 0 → 000
- 1 → 001
- ...
- 7 → 111

Lúc này mình thử ghép trực tiếp thì chưa ra chữ đẹp. Sau đó thử **đảo bit trong từng cụm 3 bit**:

- 6 = 110 → đảo thành 011
- 4 = 100 → đảo thành 001
- 1 = 001 → đảo thành 100

Sau khi nối lại và decode ra ascii mọi người sẽ nhận được foundit

Với việc nhận được 1 đoạn tn ngắn như này thi mình nghĩ nó sẽ là mk cho việc stegnography file jpeg nên mình sẽ dùng steghide để decode thử

```python
steghide extract -sf Tachyon2.jpeg -p foundit
```

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%202.png)

Sau khi extract mọi người sẽ nhận được vô số file flag giả và trong đó có file flag cuối cùng nó trông là mã hóa rot cipher 

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%203.png)

Mình sẽ mang nó lên cyberchef decode

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%204.png)

TACHYON{h1dd3n_1n_pl41ns1ght}
