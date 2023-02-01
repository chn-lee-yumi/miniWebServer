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
    request.print()  # this will print request information on the console
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
