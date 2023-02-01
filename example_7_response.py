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
