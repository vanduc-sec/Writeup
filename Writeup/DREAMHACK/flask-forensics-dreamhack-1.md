# flask-forensics-dreamhack-1

**Description
[[함께실습] flask-forensics](https://learn.dreamhack.io/657)에서 실습하는 문제입니다.
운영 중인 서버가 해킹 당한 것 같습니다.
해커가 서버의 전체 소스코드를 다운로드한 시간을 구해주세요.
Access Info
1st link
첫 번째 주소는 웹 사이트를 호스팅하고 있습니다. 브라우저 등을 이용해 접근하세요.
2nd link
두 번째 주소에는 ssh를 이용해 접근할 수 있습니다. 다음 정보를 사용하세요:
• id: `dream`
• pw: `hack1234`
Flag Info
• FLAG: `DH{downloadTime}`
    ◦ `downloadTime`: 해커가 서버의 전체 소스코드를 다운로드한 시각을 Unix Timestamp로 나타낸 것Translate**

- • id: `dream`
- • pw: `hack1234`
- • FLAG: `DH{downloadTime}`
    - ◦ `downloadTime`: 해커가 서버의 전체 소스코드를 다운로드한 시각을 Unix Timestamp로 나타낸 것
- Sau khi tải file về và giải nén chúng ta sẽ nhận 1 file log và thư mục app.

➜  dh ls
access.log                                ae63229b-6801-4046-a77c-91f6eb6d105b.zip:Zone.Identifier  README.txt
ae63229b-6801-4046-a77c-91f6eb6d105b.zip  app
➜  dh cd app
➜  app ls
api_keys.py  db_helper.py  _debug.py   LICENSE         [prod.py](http://prod.py/)    requirements.txt  [run.sh](http://run.sh/)    static     [util.py](http://util.py/)[app.py](http://app.py/)       db_models.py  Dockerfile  [middlewares.py](http://middlewares.py/)  [README.md](http://readme.md/)  [run.prod.sh](http://run.prod.sh/)       [setup.sh](http://setup.sh/)  templates  vulns
➜  app cd ..

- Bây giờ chúng ta sẽ đọc file log xem có gì không, file log  dài đọc khá lú

➜  dh cat access.log
INFO:app:2024-04-28T02:06:42 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7254
INFO:app:2024-04-28T02:06:42 | 200 | 3370 text/html
INFO:app:2024-04-28T02:06:42 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:06:42 | 304 | 206620 text/css
INFO:app:2024-04-28T02:06:42 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/temp.png.min.png](http://localhost:5000/static/uploads/temp.png.min.png) None
INFO:app:2024-04-28T02:06:42 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:06:42 | 200 | 2561 image/png
INFO:app:2024-04-28T02:06:42 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:06:42 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:06:42 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:06:44 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/login](http://localhost:5000/sql-injection/login) None
INFO:app:2024-04-28T02:06:44 | 200 | 4050 text/html
INFO:app:2024-04-28T02:06:44 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:06:44 | 304 | 206620 text/css
INFO:app:2024-04-28T02:06:44 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:06:44 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:06:44 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:06:44 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:06:49 | 172.17.0.1 | POST [http://localhost:5000/sql-injection/login](http://localhost:5000/sql-injection/login) 30
INFO:app:2024-04-28T02:06:49 | 200 | 4246 text/html
INFO:app:2024-04-28T02:06:49 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:06:49 | 304 | 206620 text/css
INFO:app:2024-04-28T02:06:49 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:06:49 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:06:49 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:06:49 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:06:53 | 172.17.0.1 | POST [http://localhost:5000/sql-injection/login](http://localhost:5000/sql-injection/login) 33
INFO:app:2024-04-28T02:06:53 | 200 | 4246 text/html
INFO:app:2024-04-28T02:06:53 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:06:53 | 304 | 206620 text/css
INFO:app:2024-04-28T02:06:53 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:06:53 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:06:53 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:06:53 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:06:59 | 172.17.0.1 | POST [http://localhost:5000/sql-injection/login](http://localhost:5000/sql-injection/login) 41
INFO:app:2024-04-28T02:06:59 | 200 | 4246 text/html
INFO:app:2024-04-28T02:06:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:06:59 | 304 | 206620 text/css
INFO:app:2024-04-28T02:06:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:06:59 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:06:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:06:59 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:07:08 | 172.17.0.1 | POST [http://localhost:5000/sql-injection/login](http://localhost:5000/sql-injection/login) 39
ERROR:waitress:Exception while serving /sql-injection/login
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 59, in sql_injection_login
return sql_injection_login_api(request, app)
File "/usr/src/app/vulns/sql_injection/sql_injection_login.py", line 22, in sql_injection_login_api
db_result = app.db_helper.execute_read(sql)
File "/usr/src/app/db_helper.py", line 33, in execute_read
cur.execute(sql, params)
sqlite3.OperationalError: near "' AND password='": syntax error
INFO:app:2024-04-28T02:07:30 | 172.17.0.1 | POST [http://localhost:5000/sql-injection/login](http://localhost:5000/sql-injection/login) 41
INFO:app:2024-04-28T02:07:30 | 200 | 4260 text/html
INFO:app:2024-04-28T02:07:30 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:07:30 | 304 | 206620 text/css
INFO:app:2024-04-28T02:07:30 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:07:30 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:07:30 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:07:30 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:07:35 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=](http://localhost:5000/sql-injection/search?q=) None
INFO:app:2024-04-28T02:07:35 | 200 | 4249 text/html
INFO:app:2024-04-28T02:07:35 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:07:35 | 304 | 206620 text/css
INFO:app:2024-04-28T02:07:35 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:07:35 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:07:35 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:07:35 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:07:38 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=123123](http://localhost:5000/sql-injection/search?q=123123) None
INFO:app:2024-04-28T02:07:38 | 200 | 4024 text/html
INFO:app:2024-04-28T02:07:38 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:07:38 | 304 | 206620 text/css
INFO:app:2024-04-28T02:07:38 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:07:38 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:07:38 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:07:38 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:07:50 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=](http://localhost:5000/sql-injection/search?q=) None
INFO:app:2024-04-28T02:07:50 | 200 | 4249 text/html
INFO:app:2024-04-28T02:07:50 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:07:50 | 304 | 206620 text/css
INFO:app:2024-04-28T02:07:50 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:07:50 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:07:50 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:07:50 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:08:28 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=123123'+UNION+SELECT+*+from+information_schema.tables+--](http://localhost:5000/sql-injection/search?q=123123%27+UNION+SELECT+*+from+information_schema.tables+--) None
ERROR:waitress:Exception while serving /sql-injection/search
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 64, in sql_injection_search
return sql_injection_search_page(request, app)
File "/usr/src/app/vulns/sql_injection/sql_injection_search.py", line 9, in sql_injection_search_page
db_result = app.db_helper.execute_read(sql)
File "/usr/src/app/db_helper.py", line 33, in execute_read
cur.execute(sql, params)
sqlite3.OperationalError: no such table: information_schema.tables
INFO:app:2024-04-28T02:08:41 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=123123'+UNION+SELECT+*+from+information_schema.table+--](http://localhost:5000/sql-injection/search?q=123123%27+UNION+SELECT+*+from+information_schema.table+--) None
ERROR:waitress:Exception while serving /sql-injection/search
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 64, in sql_injection_search
return sql_injection_search_page(request, app)
File "/usr/src/app/vulns/sql_injection/sql_injection_search.py", line 9, in sql_injection_search_page
db_result = app.db_helper.execute_read(sql)
File "/usr/src/app/db_helper.py", line 33, in execute_read
cur.execute(sql, params)
sqlite3.OperationalError: near "table": syntax error
INFO:app:2024-04-28T02:08:49 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=123123'+UNION+SELECT+1%2C2+--](http://localhost:5000/sql-injection/search?q=123123%27+UNION+SELECT+1%2C2+--) None
ERROR:waitress:Exception while serving /sql-injection/search
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 64, in sql_injection_search
return sql_injection_search_page(request, app)
File "/usr/src/app/vulns/sql_injection/sql_injection_search.py", line 9, in sql_injection_search_page
db_result = app.db_helper.execute_read(sql)
File "/usr/src/app/db_helper.py", line 33, in execute_read
cur.execute(sql, params)
sqlite3.OperationalError: SELECTs to the left and right of UNION do not have the same number of result columns
INFO:app:2024-04-28T02:09:03 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=123123'+](http://localhost:5000/sql-injection/search?q=123123%27+) None
ERROR:waitress:Exception while serving /sql-injection/search
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 64, in sql_injection_search
return sql_injection_search_page(request, app)
File "/usr/src/app/vulns/sql_injection/sql_injection_search.py", line 9, in sql_injection_search_page
db_result = app.db_helper.execute_read(sql)
File "/usr/src/app/db_helper.py", line 33, in execute_read
cur.execute(sql, params)
sqlite3.OperationalError: unrecognized token: "'"
INFO:app:2024-04-28T02:09:08 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=123123'+--](http://localhost:5000/sql-injection/search?q=123123%27+--) None
INFO:app:2024-04-28T02:09:08 | 200 | 4032 text/html
INFO:app:2024-04-28T02:09:08 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:08 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:08 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:08 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:08 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:08 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:32 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/search?q=123123'+union+select+1%2C2+--](http://localhost:5000/sql-injection/search?q=123123%27+union+select+1%2C2+--) None
ERROR:waitress:Exception while serving /sql-injection/search
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 64, in sql_injection_search
return sql_injection_search_page(request, app)
File "/usr/src/app/vulns/sql_injection/sql_injection_search.py", line 9, in sql_injection_search_page
db_result = app.db_helper.execute_read(sql)
File "/usr/src/app/db_helper.py", line 33, in execute_read
cur.execute(sql, params)
sqlite3.OperationalError: SELECTs to the left and right of UNION do not have the same number of result columns
INFO:app:2024-04-28T02:09:37 | 172.17.0.1 | GET [http://localhost:5000/xss/reflected?search=](http://localhost:5000/xss/reflected?search=) None
INFO:app:2024-04-28T02:09:37 | 200 | 4243 text/html
INFO:app:2024-04-28T02:09:37 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:37 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:37 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:37 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:37 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:37 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:38 | 172.17.0.1 | GET [http://localhost:5000/xss/reflected?search=](http://localhost:5000/xss/reflected?search=) None
INFO:app:2024-04-28T02:09:38 | 200 | 4243 text/html
INFO:app:2024-04-28T02:09:38 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:38 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:38 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:38 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:38 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:38 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:40 | 172.17.0.1 | GET [http://localhost:5000/xss/reflected?search=123123](http://localhost:5000/xss/reflected?search=123123) None
INFO:app:2024-04-28T02:09:40 | 200 | 4018 text/html
INFO:app:2024-04-28T02:09:40 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:40 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:40 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:40 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:40 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:40 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:42 | 172.17.0.1 | GET [http://localhost:5000/xss/reflected?search=123123](http://localhost:5000/xss/reflected?search=123123) None
INFO:app:2024-04-28T02:09:42 | 200 | 4018 text/html
INFO:app:2024-04-28T02:09:42 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:42 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:42 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:42 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:42 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:42 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:52 | 172.17.0.1 | GET [http://localhost:5000/xss/reflected?search=<script>alert(1)<%2Fscript>](http://localhost:5000/xss/reflected?search=%3Cscript%3Ealert%281%29%3C%2Fscript%3E) None
INFO:app:2024-04-28T02:09:52 | 200 | 4037 text/html
INFO:app:2024-04-28T02:09:52 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:52 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:52 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:52 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:52 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:52 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:55 | 172.17.0.1 | GET [http://localhost:5000/xss/stored](http://localhost:5000/xss/stored) None
INFO:app:2024-04-28T02:09:55 | 200 | 3990 text/html
INFO:app:2024-04-28T02:09:55 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:55 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:55 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:55 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:55 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:55 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:57 | 172.17.0.1 | POST [http://localhost:5000/xss/stored](http://localhost:5000/xss/stored) 47
INFO:app:2024-04-28T02:09:57 | 200 | 4164 text/html
INFO:app:2024-04-28T02:09:57 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:57 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:57 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:57 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:57 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:57 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:09:59 | 172.17.0.1 | GET [http://localhost:5000/file-upload](http://localhost:5000/file-upload) None
INFO:app:2024-04-28T02:09:59 | 200 | 3315 text/html
INFO:app:2024-04-28T02:09:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:09:59 | 304 | 206620 text/css
INFO:app:2024-04-28T02:09:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:09:59 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:09:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:09:59 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:10:11 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 180
convert-im6.q16: improper image header `/usr/src/app/temp/uploads/123.png' @ error/png.c/ReadPNGImage/4107. convert-im6.q16: no images defined` /usr/src/app/temp/uploads/123.png.min.png' @ error/convert.c/ConvertImageCommand/3229.
mv: cannot stat '/usr/src/app/temp/uploads/123.png.min.png': No such file or directory
INFO:app:2024-04-28T02:10:11 | 200 | 3369 text/html
INFO:app:2024-04-28T02:10:11 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:10:11 | 304 | 206620 text/css
INFO:app:2024-04-28T02:10:11 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/123.png.min.png](http://localhost:5000/static/uploads/123.png.min.png) None
INFO:app:2024-04-28T02:10:11 | 404 | 232 text/html
INFO:app:2024-04-28T02:10:11 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:10:11 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:10:11 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:10:11 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:10:27 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7255
INFO:app:2024-04-28T02:10:27 | 422 | 132 application/json
INFO:app:2024-04-28T02:10:40 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 180
convert-im6.q16: improper image header `/usr/src/app/temp/uploads/123.png' @ error/png.c/ReadPNGImage/4107. convert-im6.q16: no images defined` /usr/src/app/temp/uploads/123.png.min.png' @ error/convert.c/ConvertImageCommand/3229.
mv: cannot stat '/usr/src/app/temp/uploads/123.png.min.png': No such file or directory
INFO:app:2024-04-28T02:10:40 | 200 | 3369 text/html
INFO:app:2024-04-28T02:10:40 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:10:40 | 304 | 206620 text/css
INFO:app:2024-04-28T02:10:40 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/123.png.min.png](http://localhost:5000/static/uploads/123.png.min.png) None
INFO:app:2024-04-28T02:10:40 | 404 | 232 text/html
INFO:app:2024-04-28T02:10:40 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:10:40 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:10:40 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:10:40 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:10:57 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:10:57 | 304 | 206620 text/css
INFO:app:2024-04-28T02:10:57 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.map](http://localhost:5000/static/assets/axios.min.map) None
INFO:app:2024-04-28T02:10:57 | 404 | 232 text/html
INFO:app:2024-04-28T02:11:09 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/123.png.min.png](http://localhost:5000/static/uploads/123.png.min.png) None
INFO:app:2024-04-28T02:11:09 | 404 | 232 text/html
INFO:app:2024-04-28T02:11:17 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/temp.png.min.png](http://localhost:5000/static/uploads/temp.png.min.png) None
INFO:app:2024-04-28T02:11:17 | 304 | 2561 image/png
INFO:app:2024-04-28T02:11:59 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 188
INFO:app:2024-04-28T02:11:59 | 422 | 124 application/json
INFO:app:2024-04-28T02:12:00 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.map](http://localhost:5000/static/assets/axios.min.map) None
INFO:app:2024-04-28T02:12:00 | 404 | 232 text/html
INFO:app:2024-04-28T02:12:18 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7273
sh: 1: sh: 1: temp.png.min.png: not foundtemp.png.min.png: not found

mv: missing destination file operand after '/usr/src/app/temp/uploads/'
Try 'mv --help' for more information.
INFO:app:2024-04-28T02:12:18 | 200 | 3397 text/html
INFO:app:2024-04-28T02:12:18 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:12:18 | 304 | 206620 text/css
INFO:app:2024-04-28T02:12:18 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/%26 touch hack.txt %26 temp.png.min.png](http://localhost:5000/static/uploads/%26%20touch%20hack.txt%20%26%20temp.png.min.png) None
INFO:app:2024-04-28T02:12:18 | 404 | 232 text/html
INFO:app:2024-04-28T02:12:18 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:12:18 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:12:19 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:12:19 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:12:19 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.map](http://localhost:5000/static/assets/axios.min.map) None
INFO:app:2024-04-28T02:12:19 | 404 | 232 text/html
INFO:app:2024-04-28T02:12:45 | 172.17.0.1 | GET [http://localhost:5000/file-upload](http://localhost:5000/file-upload) None
INFO:app:2024-04-28T02:12:45 | 200 | 3315 text/html
INFO:app:2024-04-28T02:12:45 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:12:45 | 304 | 206620 text/css
INFO:app:2024-04-28T02:12:45 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:12:45 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:12:45 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:12:45 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:12:58 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/hack.min.png](http://localhost:5000/static/uploads/hack.min.png) None
INFO:app:2024-04-28T02:12:58 | 404 | 232 text/html
INFO:app:2024-04-28T02:13:07 | 172.17.0.1 | GET [http://localhost:5000/path-traversal](http://localhost:5000/path-traversal) None
INFO:app:2024-04-28T02:13:07 | 200 | 3226 text/html
INFO:app:2024-04-28T02:13:07 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:13:07 | 304 | 206620 text/css
INFO:app:2024-04-28T02:13:07 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:13:07 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:13:07 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:13:07 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:13:07 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:13:07 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:13:09 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:13:09 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:13:18 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=hack.txt](http://localhost:5000/path-traversal-img?img=hack.txt) None
ERROR:waitress:Exception while serving /path-traversal-img
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 103, in path_traversal_img
return path_traversal_image(request, app)
File "/usr/src/app/vulns/path_traversal/path_traversal.py", line 14, in path_traversal_image
return send_file(image_path)
File "/usr/local/lib/python3.7/site-packages/flask/helpers.py", line 625, in send_file
cache_timeout=cache_timeout,
File "/usr/local/lib/python3.7/site-packages/werkzeug/utils.py", line 697, in send_file
stat = os.stat(path)
FileNotFoundError: [Errno 2] No such file or directory: '/usr/src/app/static/img/hack.txt'
INFO:app:2024-04-28T02:13:23 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2Fhack.txt](http://localhost:5000/path-traversal-img?img=..%2Fhack.txt) None
ERROR:waitress:Exception while serving /path-traversal-img
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 103, in path_traversal_img
return path_traversal_image(request, app)
File "/usr/src/app/vulns/path_traversal/path_traversal.py", line 14, in path_traversal_image
return send_file(image_path)
File "/usr/local/lib/python3.7/site-packages/flask/helpers.py", line 625, in send_file
cache_timeout=cache_timeout,
File "/usr/local/lib/python3.7/site-packages/werkzeug/utils.py", line 697, in send_file
stat = os.stat(path)
FileNotFoundError: [Errno 2] No such file or directory: '/usr/src/app/static/img/../hack.txt'
INFO:app:2024-04-28T02:13:27 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack.txt](http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack.txt) None
INFO:app:2024-04-28T02:13:27 | 200 | 0 text/plain
INFO:app:2024-04-28T02:13:31 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2F..%2Fhack.txt](http://localhost:5000/path-traversal-img?img=..%2F..%2F..%2Fhack.txt) None
ERROR:waitress:Exception while serving /path-traversal-img
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 103, in path_traversal_img
return path_traversal_image(request, app)
File "/usr/src/app/vulns/path_traversal/path_traversal.py", line 14, in path_traversal_image
return send_file(image_path)
File "/usr/local/lib/python3.7/site-packages/flask/helpers.py", line 625, in send_file
cache_timeout=cache_timeout,
File "/usr/local/lib/python3.7/site-packages/werkzeug/utils.py", line 697, in send_file
stat = os.stat(path)
FileNotFoundError: [Errno 2] No such file or directory: '/usr/src/app/static/img/../../../hack.txt'
INFO:app:2024-04-28T02:13:33 | 172.17.0.1 | GET [http://localhost:5000/file-upload](http://localhost:5000/file-upload) None
INFO:app:2024-04-28T02:13:33 | 200 | 3315 text/html
INFO:app:2024-04-28T02:13:33 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:13:33 | 304 | 206620 text/css
INFO:app:2024-04-28T02:13:33 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:13:33 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:13:33 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:13:33 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:13:41 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7273
sh: 1: sh: 1: temp.png.min.png: not foundtemp.png.min.png: not found

mv: missing destination file operand after '/usr/src/app/temp/uploads/'
Try 'mv --help' for more information.
INFO:app:2024-04-28T02:13:41 | 200 | 3397 text/html
INFO:app:2024-04-28T02:13:41 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/%26 touch hack.txt %26 temp.png.min.png](http://localhost:5000/static/uploads/%26%20touch%20hack.txt%20%26%20temp.png.min.png) None
INFO:app:2024-04-28T02:13:41 | 404 | 232 text/html
INFO:app:2024-04-28T02:13:41 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:13:41 | 304 | 206620 text/css
INFO:app:2024-04-28T02:13:41 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:13:41 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:13:41 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:13:41 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:14:12 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2F..%2Fhack.txt](http://localhost:5000/path-traversal-img?img=..%2F..%2F..%2Fhack.txt) None
ERROR:waitress:Exception while serving /path-traversal-img
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 103, in path_traversal_img
return path_traversal_image(request, app)
File "/usr/src/app/vulns/path_traversal/path_traversal.py", line 14, in path_traversal_image
return send_file(image_path)
File "/usr/local/lib/python3.7/site-packages/flask/helpers.py", line 625, in send_file
cache_timeout=cache_timeout,
File "/usr/local/lib/python3.7/site-packages/werkzeug/utils.py", line 697, in send_file
stat = os.stat(path)
FileNotFoundError: [Errno 2] No such file or directory: '/usr/src/app/static/img/../../../hack.txt'
INFO:app:2024-04-28T02:14:16 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack.txt](http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack.txt) None
INFO:app:2024-04-28T02:14:16 | 200 | 0 text/plain
INFO:app:2024-04-28T02:15:07 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7274
sh: 1: temp.png.min.png: not found
mv: missing destination file operand after '/usr/src/app/temp/uploads/'
Try 'mv --help' for more information.
sh: 1: temp.png.min.png: not found
INFO:app:2024-04-28T02:15:07 | 200 | 3398 text/html
INFO:app:2024-04-28T02:15:07 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/%26 touch hack2.txt %26 temp.png.min.png](http://localhost:5000/static/uploads/%26%20touch%20hack2.txt%20%26%20temp.png.min.png) None
INFO:app:2024-04-28T02:15:07 | 404 | 232 text/html
INFO:app:2024-04-28T02:15:07 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:15:07 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:15:07 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:15:07 | 304 | 206620 text/css
INFO:app:2024-04-28T02:15:07 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:15:07 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:15:11 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack.txt](http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack.txt) None
INFO:app:2024-04-28T02:15:11 | 304 | 0 text/plain
INFO:app:2024-04-28T02:15:13 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack2.txt](http://localhost:5000/path-traversal-img?img=..%2F..%2Fhack2.txt) None
INFO:app:2024-04-28T02:15:13 | 200 | 0 text/plain
INFO:app:2024-04-28T02:16:29 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7280
ERROR:waitress:Exception while serving /file-upload
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 70, in file_upload
return file_upload_api(request, app)
File "/usr/src/app/vulns/file_upload/file_upload.py", line 15, in file_upload_api
file = request.files['file']
File "/usr/local/lib/python3.7/site-packages/werkzeug/datastructures.py", line 377, in **getitem**
raise exceptions.BadRequestKeyError(key)
werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.
KeyError: 'file'
INFO:app:2024-04-28T02:16:59 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7254
INFO:app:2024-04-28T02:16:59 | 200 | 3370 text/html
INFO:app:2024-04-28T02:16:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:16:59 | 304 | 206620 text/css
INFO:app:2024-04-28T02:16:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:16:59 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:16:59 | 172.17.0.1 | GET [http://localhost:5000/static/uploads/temp.png.min.png](http://localhost:5000/static/uploads/temp.png.min.png) None
INFO:app:2024-04-28T02:16:59 | 200 | 2561 image/png
INFO:app:2024-04-28T02:16:59 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:16:59 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:17:52 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7288
ERROR:waitress:Exception while serving /file-upload
Traceback (most recent call last):
File "/usr/local/lib/python3.7/site-packages/waitress/channel.py", line 426, in service
task.service()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 168, in service
self.execute()
File "/usr/local/lib/python3.7/site-packages/waitress/task.py", line 434, in execute
app_iter = self.channel.server.application(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2088, in **call**
return self.wsgi_app(environ, start_response)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2073, in wsgi_app
response = self.handle_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2070, in wsgi_app
response = self.full_dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1515, in full_dispatch_request
rv = self.handle_user_exception(e)
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1513, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1499, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
File "/usr/src/app/app.py", line 70, in file_upload
return file_upload_api(request, app)
File "/usr/src/app/vulns/file_upload/file_upload.py", line 15, in file_upload_api
file = request.files['file']
File "/usr/local/lib/python3.7/site-packages/werkzeug/datastructures.py", line 377, in **getitem**
raise exceptions.BadRequestKeyError(key)
werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.
KeyError: 'file'
INFO:app:2024-04-28T02:20:38 | 172.17.0.1 | POST [http://localhost:5000/file-upload](http://localhost:5000/file-upload) 7272
sh: 1: sh: 1: .png.min.png: not found.png.min.png: not found

mv: missing destination file operand after '/usr/src/app/temp/uploads/'
Try 'mv --help' for more information.
INFO:app:2024-04-28T02:20:38 | 200 | 3396 text/html
INFO:app:2024-04-28T02:20:53 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2Fsome.tar](http://localhost:5000/path-traversal-img?img=..%2F..%2Fsome.tar) None
INFO:app:2024-04-28T02:20:53 | 200 | 430080 application/x-tar
INFO:app:2024-04-28T02:21:00 | 172.17.0.1 | GET [http://localhost:5000/path-traversal](http://localhost:5000/path-traversal) None
INFO:app:2024-04-28T02:21:00 | 200 | 3226 text/html
INFO:app:2024-04-28T02:21:00 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:21:00 | 304 | 206620 text/css
INFO:app:2024-04-28T02:21:00 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:21:00 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:21:00 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:21:00 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:21:00 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:21:00 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:21:01 | 172.17.0.1 | GET [http://localhost:5000/idor/login](http://localhost:5000/idor/login) None
INFO:app:2024-04-28T02:21:01 | 200 | 3984 text/html
INFO:app:2024-04-28T02:21:01 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:21:01 | 304 | 206620 text/css
INFO:app:2024-04-28T02:21:01 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:21:01 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:21:01 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:21:01 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:21:03 | 172.17.0.1 | GET [http://localhost:5000/iframe-injection?page=%2Fstatic%2Fpages%2Fabout.html](http://localhost:5000/iframe-injection?page=%2Fstatic%2Fpages%2Fabout.html) None
INFO:app:2024-04-28T02:21:03 | 200 | 3170 text/html
INFO:app:2024-04-28T02:21:03 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:21:03 | 304 | 206620 text/css
INFO:app:2024-04-28T02:21:03 | 172.17.0.1 | GET [http://localhost:5000/static/pages/about.html](http://localhost:5000/static/pages/about.html) None
INFO:app:2024-04-28T02:21:03 | 304 | 341 text/html
INFO:app:2024-04-28T02:21:03 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:21:03 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:21:03 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:21:03 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:21:11 | 172.17.0.1 | GET [http://localhost:5000/iframe-injection?page=..%2F..%2F..%2F..%2Fetc%2Fpasswd](http://localhost:5000/iframe-injection?page=..%2F..%2F..%2F..%2Fetc%2Fpasswd) None
INFO:app:2024-04-28T02:21:11 | 200 | 3168 text/html
INFO:app:2024-04-28T02:21:11 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:21:11 | 304 | 206620 text/css
INFO:app:2024-04-28T02:21:11 | 172.17.0.1 | GET [http://localhost:5000/etc/passwd](http://localhost:5000/etc/passwd) None
INFO:app:2024-04-28T02:21:11 | 404 | 232 text/html
INFO:app:2024-04-28T02:21:11 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:21:11 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:21:11 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:21:11 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:21:13 | 172.17.0.1 | GET [http://localhost:5000/path-traversal](http://localhost:5000/path-traversal) None
INFO:app:2024-04-28T02:21:13 | 200 | 3226 text/html
INFO:app:2024-04-28T02:21:13 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:21:13 | 304 | 206620 text/css
INFO:app:2024-04-28T02:21:13 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:21:13 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:21:13 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:21:13 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:21:13 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:21:13 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:21:14 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:21:14 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:21:23 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd](http://localhost:5000/path-traversal-img?img=..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd) None
INFO:app:2024-04-28T02:21:23 | 200 | 839 application/octet-stream
INFO:app:2024-04-28T02:21:34 | 172.17.0.1 | GET [http://localhost:5000/path-traversal](http://localhost:5000/path-traversal) None
INFO:app:2024-04-28T02:21:34 | 200 | 3226 text/html
INFO:app:2024-04-28T02:21:34 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:21:34 | 304 | 206620 text/css
INFO:app:2024-04-28T02:21:34 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:21:34 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:21:34 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:21:34 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:21:34 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:21:34 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:21:35 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:21:35 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:21:43 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2Fapp.py](http://localhost:5000/path-traversal-img?img=..%2F..%2Fapp.py) None
INFO:app:2024-04-28T02:21:43 | 200 | 3651 text/x-python
INFO:app:2024-04-28T02:22:25 | 172.17.0.1 | GET [http://localhost:5000/file-upload](http://localhost:5000/file-upload) None
INFO:app:2024-04-28T02:22:25 | 200 | 3315 text/html
INFO:app:2024-04-28T02:22:25 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:22:25 | 304 | 206620 text/css
INFO:app:2024-04-28T02:22:25 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:22:25 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:22:25 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:22:25 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/ssrf](http://localhost:5000/ssrf) None
INFO:app:2024-04-28T02:22:26 | 200 | 3793 text/html
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:22:26 | 304 | 206620 text/css
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:22:26 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:22:26 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/path-traversal](http://localhost:5000/path-traversal) None
INFO:app:2024-04-28T02:22:26 | 200 | 3226 text/html
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:22:26 | 304 | 206620 text/css
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg](http://localhost:5000/path-traversal-img?img=84721189311536093217.jpg) None
INFO:app:2024-04-28T02:22:26 | 304 | 24409 image/jpeg
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:22:26 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:22:26 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/idor/login](http://localhost:5000/idor/login) None
INFO:app:2024-04-28T02:22:26 | 200 | 3984 text/html
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:22:26 | 304 | 206620 text/css
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:22:26 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:22:26 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:22:26 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:22:27 | 172.17.0.1 | GET [http://localhost:5000/iframe-injection?page=%2Fstatic%2Fpages%2Fabout.html](http://localhost:5000/iframe-injection?page=%2Fstatic%2Fpages%2Fabout.html) None
INFO:app:2024-04-28T02:22:27 | 200 | 3170 text/html
INFO:app:2024-04-28T02:22:27 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:22:27 | 304 | 206620 text/css
INFO:app:2024-04-28T02:22:27 | 172.17.0.1 | GET [http://localhost:5000/static/pages/about.html](http://localhost:5000/static/pages/about.html) None
INFO:app:2024-04-28T02:22:27 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:22:27 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:22:27 | 304 | 341 text/html
INFO:app:2024-04-28T02:22:27 | 304 | 648 text/javascript
INFO:app:2024-04-28T02:22:27 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:25:05 | 172.17.0.1 | GET [http://localhost:5000/sql-injection/login](http://localhost:5000/sql-injection/login) None
INFO:app:2024-04-28T02:25:05 | 200 | 4050 text/html
INFO:app:2024-04-28T02:25:05 | 172.17.0.1 | GET [http://localhost:5000/static/assets/bulma.min.css](http://localhost:5000/static/assets/bulma.min.css) None
INFO:app:2024-04-28T02:25:05 | 304 | 206620 text/css
INFO:app:2024-04-28T02:25:05 | 172.17.0.1 | GET [http://localhost:5000/static/assets/axios.min.js](http://localhost:5000/static/assets/axios.min.js) None
INFO:app:2024-04-28T02:25:05 | 304 | 17753 text/javascript
INFO:app:2024-04-28T02:25:05 | 172.17.0.1 | GET [http://localhost:5000/static/assets/global.js](http://localhost:5000/static/assets/global.js) None
INFO:app:2024-04-28T02:25:05 | 304 | 648 text/javascript
➜  dh

- Đọc file log thì mọi người chỉ cần tìm những file nén thôi vì bài đã bảo hacker tải toàn bộ mã nguồn thì nó phải được nén vào 1 file chứ ko thể nòa là nhiều file được
- Khi đó chúng ta sẽ thấy có 1 file tar được cho

INFO:app:2024-04-28T02:20:53 | 172.17.0.1 | GET [http://localhost:5000/path-traversal-img?img=..%2F..%2Fsome.tar](http://localhost:5000/path-traversal-img?img=..%2F..%2Fsome.tar) None

- Đến đây thì việc của chúng ta đơn giản là chuyển thời gian ngày giờ sang Unix timestamp là được và chúng ta chỉ cần lấy cụm  2024-04-28T02:20:53 và lên web [https://www.epochconverter.com/](https://www.epochconverter.com/) để tiến hành chuyển đổi hoặc mọi người có thể dùng lệnh:

date -ud "2024-04-28 02:20:53" +%s

![image.png](Gyul%20Box-dreamhack-1/Binary%20Badresources-htb-med/image.png)

- Vậy flag sẽ là: DH{1714270853}
