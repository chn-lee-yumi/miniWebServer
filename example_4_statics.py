"""
I already put an index.html in this repo. If you want to access this file, you need to put the absolute path in the URL.

For example, if the path of this repo in your computer is `/Users/xxx/miniWebServer`, the path of `index.html` is `/Users/xxx/miniWebServer/index.html`,
then you should use the URL `http://127.0.0.1:8080/Users/xxx/miniWebServer/index.html`.
"""

from miniWebServer import WebServer

app = WebServer(__name__)

app.run(host="127.0.0.1", port=8080)
