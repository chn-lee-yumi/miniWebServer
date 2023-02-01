import _thread
from miniWebServer import WebServer

app = WebServer(__name__)


def http_server():
    """启动http服务器"""
    app.run(host="127.0.0.1", port=8080)


@app.route("/")
def hello(request):
    return "Hello, World!"


_thread.start_new_thread(http_server, ())

# If you run this in python (not Micropython), you need to sleep, or it will exit immediately.

import time

time.sleep(99999)
