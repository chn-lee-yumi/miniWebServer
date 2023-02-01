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
