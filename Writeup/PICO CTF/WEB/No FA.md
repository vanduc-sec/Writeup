# No FA

Bản chất & Ví dụ: - 2FA/MFA: Yêu cầu thêm yếu tố ngoài password.- Session transition: Sau password đúng, user thường ở trạng thái “chưa hoàn tất 2FA”.- Broken flow: Nếu endpoint sau 2FA không kiểm trạng thái, có thể bypass.
Hệ sinh thái kiến thức: - 2FA/MFA logic- Authentication factor- Session transition- Backup/step-up auth- Broken auth flow
Trạng thái: Chưa bắt đầu
Trạng thái 1: Chưa bắt đầu

![image.png](No%20FA/image.png)

Bài web này cấp cho ta khá nhiều dữ liệu 

![image.png](No%20FA/image%201.png)

Đầu tiên thì trang web sẽ bắt mình đăng nhập và nó cũng không cho đăng ý

![image.png](No%20FA/image%202.png)

Thứ 2 thì mình xem phần dữ liệu bị leak là 1 file db mở bằng db browser thì mình có được tài khoản và hash của admin và riêng tài khoản này cần xác thực 2fa 

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
from dotenv import load_dotenv

import db
import os
import hashlib
import random
import time

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.before_request
def initialize():
    app.before_request_funcs[None].remove(initialize)
    db.init_db()

@app.route("/")
def home():
    if 'username' not in session or session['logged'] == 'false':
        flash('Please login to access this page', 'red')
        return redirect(url_for('login'))
    
    flag = "No flag for you!!"
    if session.get('username') == 'admin':
        flag = os.getenv('FLAG')
    
    return render_template("index.html", flag=flag)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user_by_username(username)
        if user and hashlib.sha256(password.encode()).hexdigest() == user['password']:
            if user['two_fa']:
                # Generate OTP
                otp = str(random.randint(1000, 9999))
                session['otp_secret'] = otp
                session['otp_timestamp'] = time.time()
                session['username'] = username
                session['logged'] = 'false'
                # send OTP to mail ---
                return redirect(url_for('two_fa'))
            else:
                session['username'] = username
                session['logged'] = 'true'
                flash('Login successful!', 'green')
                return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'red')
    return render_template('login.html')

@app.route('/two_fa', methods=['GET', 'POST'])
def two_fa():
    if request.method == 'POST':
        otp = request.form['otp']
        stored_otp = session['otp_secret']
        timestamp = session.get('otp_timestamp')
        if stored_otp and otp == stored_otp and (time.time() - timestamp) < 120:
            session['logged'] = 'true'
            flash('Login successful!', 'green')
            return redirect(url_for('home'))
        else:
            flash('Invalid OTP or OTP expired', 'red')
            return render_template('2fa.html')
    else:
        return render_template('2fa.html')

@app.route('/logout')
def logout():
    flash('You have been logged out.', 'green')
    session.pop('username', None)
    session['logged'] = 'false'
    return redirect(url_for('login'))
```

Cuối cùng là mã nguồn có nhiều thứ cần chú ý

```
from flask import Flask, ..., session
...
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
```

Việc import thẳng object `session` từ thư viện `flask` và thiết lập `app.secret_key` chứng tỏ ứng dụng này đang sử dụng cơ chế quản lý phiên làm việc nguyên bản (mặc định) của framework Flask.

Trong route /login, thì ta thấy password sẽ được mã hóa bằng sha256

```python
if user and hashlib.sha256(password.encode()).hexdigest() == user['password']:
```

Trong route `/login`, khi kiểm tra đúng mật khẩu của user có bật 2FA, code thực hiện gán trực tiếp mã OTP vào session:

```
otp = str(random.randint(1000, 9999))
session['otp_secret'] = otp
```

Khác với nhiều ngôn ngữ/framework khác (như PHP hay Java thường lưu session trên server và chỉ cấp cho client một chuỗi Session ID vô nghĩa), Flask mặc định sử dụng **Client-side Session**. Cụ thể quá trình diễn ra như sau:

- Flask gom tất cả các key/value bạn gán vào `session` (bao gồm `username`, `logged`, `otp_secret`, `otp_timestamp`) thành một cấu trúc từ điển (tương đương định dạng JSON).
- Toàn bộ cục JSON này được mã hóa bằng thuật toán Base64URL.
- Flask dùng `SECRET_KEY` để tạo ra một chữ ký và gắn vào cuối chuỗi Base64.
- Cuối cùng, toàn bộ chuỗi này được gửi về trình duyệt của bạn dưới dạng một Cookie có tên là `session`.

Đầu tiên giờ mình sẽ thử brutece force băm xem có lấy được mật khẩu của admin không 

![image.png](No%20FA/image%203.png)

Sau khi dùng hashcat thì mình lấy được pass là : apple@123

Giờ mình sẽ đăng nhập bằng tài khoản và mật khẩu

![image.png](No%20FA/image%204.png)

Sau khi đăng nhập thì mình sẽ cần phải có OTP, đến đây mọi người hãy nhớ lại OTP sẽ được gán vào trong session và trả về cho user session['otp_secret'] = otp nên mình sẽ giả mã session và lấy OTP

```python
➜  ~ flask-unsign --decode --cookie ".eJwty0sKgCAQANC7zFoCP2V6mRhyEsEfaqvo7rlo--A9EIv35MDChbETMCijHp3ORmOiEtz8NkKiPjBVsFwbsWmpV7kobsyuGdydWsZE86BLIcP7AS2lHDs.atoH2Q.RKG4JE6-3PxyPkDsMaEPBbRtybk"
{'logged': 'false', 'otp_secret': '4219', 'otp_timestamp': 1792673753.419987, 'username': 'admin'}
➜  ~
```

OTP: 4219

![image.png](No%20FA/image%205.png)

Nhập OTP vào để verify

![image.png](No%20FA/image%206.png)

Sau khi đăng nhập chúng ta sẽ lấy được flag

academy{n0_r4t3_n0_4uth_b8c7ed63}