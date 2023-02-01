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
