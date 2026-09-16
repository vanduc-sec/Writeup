# Spongebob Squarepants-CryptoniteCTF

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image.png)

Bài này cung cấp cho chúng ta 2 file 1 file .bmp và 1 file là .jpeg theo đề bài thì có vẻ như có file đã bị hỏng gì đó, trước tiên mình sẽ mở 2 file bằng hxd thì phát hiện với file .bmp ở cuối file có dòng chữ

mp3stego_with_plankton@2026

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%201.png)

Còn đối với file .jpeg thì có vẻ như header của nó đã gặp 1 số vấn đề bình thường file jpeg sẽ bắt đầu bằng ffd8 nhưng mà ở bài này thì nó lại là 0000 có vẻ như đã bị thay đổi nên minhf se sửa lại file này 

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%202.png)

![spongebob.jpeg](Spongebob%20Squarepants-CryptoniteCTF/spongebob.jpeg)

Sửa lại mở lên mình nhận được dòng chữ krabby-patties có vẻ như là mật khẩu để làm gì đó, tiếp tục khai thác một số công cụ khác mình phát hiện được  1 file âm thanh trong file .bmp bằng mật khẩu mình vừa tìm được

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%203.png)

Đến đây mình sử dụng gợi ý lúc đầu có trong file .bmp có vẻ như là file âm thành đã bị ẩn thông tin nên mình sẽ dùng công cụ dược gọi ý là mp3stego 

![Screenshot 2026-03-10 090908.png](Spongebob%20Squarepants-CryptoniteCTF/Screenshot_2026-03-10_090908.png)

Sau khi dùng mình thu được 1 file .txt đọc nó và có được flag

![image.png](Spongebob%20Squarepants-CryptoniteCTF/image%204.png)

TACHYON{killing_1t_$p0ng3b0b!}
