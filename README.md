# miniWebServer

A mini web framework like Flask, but can run in MicroPython.

一个类似Flask的可以运行在MicroPython上的迷你web框架。

The reason why I started this project was that when I want to run an HTTP server on my ESP32-C3 development board with MicroPython, I couldn't find a
suitable package, so I decided to write one.

我开始这个项目的原因是当我想用MicroPython在我的ESP32-C3开发板上运行一个HTTP服务器时，我找不到合适的包，所以我决定写一个。

This project only has one python file, which is easy to use.

本项目只有一个python文件，简单易用。

Notice: ESP8266 can't run this because it doesn't support multithread.

注意：ESP8266 不支持多线程，因此无法运行。

## Usage

You only need to copy `miniWebServer.py` to your source code directory.

你只需要将 `miniWebServer.py` 复制到你的源代码目录。

See `example_*.py` for more usage.

有关更多用法，请参见 `example_*.py`。

### A Minimal Application

```python
from miniWebServer import WebServer

app = WebServer(__name__)

@app.route("/")
def hello(request):
    return "Hello, World!"

app.run(host="127.0.0.1", port=8080)
```

It's some like Flask, but notice that the route functions must have one argument `request`.

它有点像 Flask，但请注意路由函数必须有一个参数 `request`。

### Run in Background

`app.run()` will block the terminal. If you want to use WebREPL of MicroPython in the same time, you need to use a thread to put the HTTP server into
the background.

`app.run()` 会阻塞终端。如果想同时使用MicroPython的WebREPL，需要用一个线程将HTTP服务器放到后台。

```python
import _thread
from miniWebServer import WebServer

app = WebServer(__name__)

def http_server():
    app.run(host="127.0.0.1", port=8080)
    
@app.route("/")
def hello(request):
    return "Hello, World!"
    
_thread.start_new_thread(http_server, ())
```

### Routing

```python
from miniWebServer import WebServer

app = WebServer(__name__)

@app.route('/')
def index(request):
    return 'Index Page'

@app.route('/hello')
def hello(request):
    return 'Hello, World'

@app.route('/hello/')
def hello2(request):
    return 'Hello, World 2'
    
@app.route('/login', methods=['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        return "You POST /login"
    else:
        return "You GET /login"

app.run(host="127.0.0.1", port=8080)
```

The routing is very simple, and it doesn't support [variable rules](https://flask.palletsprojects.com/en/2.2.x/quickstart/#variable-rules) (get
arguments from URL).

路由很简单，不支持从URL获取参数。

Remember, there is always a param `request` in the function.

请记住，函数中始终有一个参数“request”。

The route supports `GET` by default. If you want to handle other methods, you need to add `methods` arg in `app.route`. It
supports `GET`, `POST`, `PUT`, `PATCH` and `DELETE`.

该路由默认支持`GET`。 如果你想处理其他方法，你需要在 `app.route` 中添加 `methods` 参数。它支持 `GET`, `POST`, `PUT`, `PATCH` 和 `DELETE`。

### Static Files

Considering of the lightness of running in MicroPython, I didn't add extra function for handling static files. Actually, if you try to access an URL,
and if it doesn't match the routes, it will try to read the file on the filesystem. So if you want to access static files, just put the path in the
URL.

考虑到在MicroPython中运行的轻便性，我没有额外添加处理静态文件的函数。 实际上，如果您尝试访问一个 URL，如果它与路由不匹配，它将尝试读取文件系统上的文件。
所以如果要访问静态文件，只要把路径放在URL中即可。

```
from miniWebServer import WebServer

app = WebServer(__name__)

app.run(host="127.0.0.1", port=8080)
```

I already put an `index.html` in this repo. If you want to access this file, you need to put the absolute path in the URL.

我已经在这个仓库中放了一个 `index.html`。 如果你想访问这个文件，你需要把绝对路径放在URL中。

For example, if the path of this repo in your computer is `/Users/xxx/miniWebServer`, the path of `index.html`
is `/Users/xxx/miniWebServer/index.html`, then you should use the URL `http://127.0.0.1:8080/Users/xxx/miniWebServer/index.html`.

比如这个仓库在你电脑中的路径是`/Users/xxx/miniWebServer`，`index.html`的路径是`/Users/xxx/miniWebServer/index.html`
，那么你应该使用URL `http://127.0.0.1:8080/Users/xxx/miniWebServer/index.html` 。

In MicroPython, I use to put the files and code in the root directory.

在 MicroPython 中，我习惯将文件和代码放在根目录中。

### Accessing Request Data

```python
from miniWebServer import WebServer

app = WebServer(__name__)

LOGIN_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Login Page</title>
</head>
<body>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password">
        <input type="submit" value="Login">
    </form>
</body>
</html>"""

def valid_login(username, password):
    return username == "admin" and password == "admin"

@app.route('/login', methods=['POST', 'GET'])
def login(request):
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return "Login success!"
        else:
            return "Invalid username/password"
    return LOGIN_HTML

@app.route('/full', methods=['POST', 'GET', 'DELETE', 'PUT', 'PATCH'])
def full(request):
    text = "Your method is %s\n" % request.method
    text += "Your path is %s\n" % request.path
    text += "HTTP Headers: %r\n" % request.headers
    text += "args: %r\n" % request.args  # url args
    text += "form: %r\n" % request.form  # application/x-www-form-urlencoded
    text += "values: %r\n" % request.values  # values = args + form, if has same key, args will override form
    text += "data: %r\n" % request.data  # request body
    text += "json: %r\n" % request.json  # application/json
    return text

app.run(host="127.0.0.1", port=8080)
```

The `request` object in Flask needs to be imported if you want to use it, but in here, it is a param in route functions.

Flask中的`request`对象如果要使用是需要导入的，但是在这里，它是路由函数中的一个参数。

### Redirects and Errors

```python
from miniWebServer import WebServer, redirect

app = WebServer(__name__)

@app.route('/index')
def index(request):
    return "Index Page"

@app.route('/')
def root(request):
    # code supports 301 and 302
    return redirect("/index", code=302)

@app.route('/500')
def error(request):
    # If code throws exceptions, it will return 500.
    raise Exception("Example Error")
    return "You won't see this return."
    
app.run(host="127.0.0.1", port=8080)
```

Use `redirect(path, code)` to redirect to another page. `code` supports `301` and `302`.

使用 `redirect(path, code)` 重定向到另一个页面。 `code` 支持 `301` 和 `302`。

If there is an exception in the code, the server will return 500 automatically, and you will see something like this in the
console: `Exception in handle_request: Exception('Example Error')`.

如果代码中出现异常，服务器会自动返回 500，你会在控制台中看到类似这样的信息：`Exception in handle_request: Exception('Example Error')`。

### Responses

```python
from miniWebServer import WebServer, jsonify

app = WebServer(__name__)

@app.route('/index')
def index(request):
    # If you return one value, it will be used as body.
    return "Index Page"

@app.route('/403')
def forbidden(request):
    # If you return two values, it will be used as body and status code.
    return "Forbidden", 403
    
@app.route('/301')
def redirect(request):
    # In fact, redirect() return this.
    # If you return three values, it will be used as body, status code, and headers.
    return "", 302, {"Location": "/index"}

@app.route('/json')
def json(request):
    # return json
    return jsonify({"key": "value"})
    
app.run(host="127.0.0.1", port=8080)
```

The route function supports one, two or three return values, which are body, status code, headers respectively.

路由函数支持一个、两个或三个返回值，分别是body、status code、headers。

If you want to return a dict, you can use `jsonify`.

如果你想返回一个字典，你可以使用 `jsonify` 。
