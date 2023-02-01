from miniWebServer import WebServer

app = WebServer(__name__)


@app.route("/")
def hello(request):
    return "Hello, World!"


app.run(host="127.0.0.1", port=8080)
