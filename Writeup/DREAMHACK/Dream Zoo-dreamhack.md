# Dream Zoo-dreamhack

![image.png](Dream%20Zoo-dreamhack/image.png)

![image.png](Dream%20Zoo-dreamhack/image%201.png)

Sau khi mở file thì mk thấy có vẻ như có liên quan j đến openstego gì đó

![image.png](Dream%20Zoo-dreamhack/image%202.png)

Này trông có vẻ giống mã dec nên mình sẽ cắt thử xem thế nào

```python
tshark -r zoo.pcap -Y "dns.flags.response==0 && dns.qry.type==TXT" \
  -T fields -e frame.number -e dns.qry.name \
| sort -n -k1,1 \
| awk -F'\t' '{print $2}' \
| awk -F'.' '{
  for(i=1;i<=NF;i++){
    if($i ~ /^[0-9A-Fa-f]+$/ && (length($i)%2)==0) printf "%s",$i
  }
} END{print ""}' > dns_hex.txt
```

![image.png](Dream%20Zoo-dreamhack/image%203.png)

Sau khi có file thì mình phát hiện ra nó là zip nên mình sẽ giải nén nó ra xem sao

![image.png](Dream%20Zoo-dreamhack/image%204.png)

![image.png](Dream%20Zoo-dreamhack/image%205.png)

Sau khi đọc hint thì mình sẽ bắt đầu khiai thác các ảnh hình trái tim 

![image.png](Dream%20Zoo-dreamhack/image%206.png)

![image.png](Dream%20Zoo-dreamhack/image%207.png)

![image.png](Dream%20Zoo-dreamhack/image%208.png)

![image.png](Dream%20Zoo-dreamhack/image%209.png)

![image.png](Dream%20Zoo-dreamhack/image%2010.png)

Sau khi etract tất cả dữ liệu thì hcungs ta sẽ biết được có vẻ flag đã bị xor với số động vật trong file zip nên mk sẽ decode

![image.png](Dream%20Zoo-dreamhack/image%2011.png)

DH{4bn0rm4l_dns_p4ck3t_l34ks_d4t4}
