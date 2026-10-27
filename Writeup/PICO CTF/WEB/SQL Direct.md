# SQL Direct

![image.png](SQL%20Direct/image.png)

Bài này có vẻ như là 1 bài tương tác với cơ sở dữ liệu 

Đầu tiên thì mình sẽ tải psql client về máy 

```python
sudo apt install postgresql-client
```

Sau khi tải thành công psql client thì mình bắt đầu chạy lệnh bài cấp để kết nói đến psql server

```python
➜  ~ psql -h chatelaine.cylabacademy.net -p 44495 -U postgres pico
Password for user postgres:
psql (18.6 (Debian 18.6-3))
Type "help" for help.

pico=#
```

Khi thấy pico=#  thì chúng ta đã kết nối thành công đến psql server rồi, đầu tiên khi kết nối đến psql server thì mình sẽ dùng lệnh `\dt` để liệt kê các bảng 

```python
pico=# \dt
          List of tables
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | flags | table | postgres
(1 row)
```

Chúng ta thấy chỉ có 1 bảng flags trong cơ sở dữ liệu này thôi, tiếp mình sẽ dùng truy vấn sql để trích xuất toàn bộ dữ liệu bảng này ra 

```python
pico=# SELECT * FROM flags;
 id | firstname | lastname  |                address
----+-----------+-----------+----------------------------------------
  1 | Luke      | Skywalker | academy{L3arN_S0m3_5qL_t0d4Y_d4538dde}
  2 | Leia      | Organa    | Alderaan
  3 | Han       | Solo      | Corellia
(3 rows)

pico=#
```

Ta đã lấy được flag chính là address của Luke 

academy{L3arN_S0m3_5qL_t0d4Y_d4538dde}