import binascii
import os

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
MEMO_DIR = "/tmp/files/"


@app.route("/", methods=["GET"])
def route_index():
    files = [
        f for f in os.listdir(MEMO_DIR) if os.path.isfile(os.path.join(MEMO_DIR, f))
    ]
    memos = [
        {"title": binascii.unhexlify(f.split(".")[0]).decode(), "key": f} for f in files
    ]

    return render_template("index.html", memos=memos)


@app.route("/add", methods=["GET"])
def route_add_index():
    return render_template("add.html")


@app.route("/add", methods=["POST"])
def route_add_do():
    title = request.form.get("title")
    body = request.form.get("body")

    if title is None or title == "":
        return "title must be specified"

    filename = binascii.hexlify(title.encode()).decode() + ".txt"
    open(os.path.join(MEMO_DIR, filename), "w+").write(body)

    return redirect("/")


@app.route("/memo", methods=["GET"])
def route_memo():
    key = request.args.get("key")
    filepath = MEMO_DIR + key

    if not os.path.exists(filepath):
        return "file not found"
    if not os.path.isfile(filepath):
        return "not a file"

    try:
        memo_title = binascii.unhexlify(key.split(".")[0]).decode()
    except Exception:
        memo_title = ""

    memo_body = open(filepath, "r").read()
    return render_template("memo.html", title=memo_title, body=memo_body)


def init():
    app.config["FLAG"] = os.environ.get("FLAG")
    if not os.path.exists(MEMO_DIR):
        os.makedirs(MEMO_DIR)


init()
app.run(host="0.0.0.0", debug=False)
