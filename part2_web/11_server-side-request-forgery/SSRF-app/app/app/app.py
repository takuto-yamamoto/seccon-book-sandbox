#! python3

import os
from io import BytesIO

import pycurl
import redis as _redis
from flask import Flask, render_template, request

app = Flask(__name__)
redis = _redis.Redis(host="redis", port=6379, db=0)


@app.route("/", methods=["GET"])
def route_index():
    return render_template("index.html", data=None)


@app.route("/", methods=["POST"])
def route_index_post():
    url = request.form.get("url")

    redis.lpush("history", url)

    buf = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buf)
    c.perform()
    c.close()

    body = buf.getvalue().decode("UTF-8")
    return render_template("index.html", url=url, data=body)


@app.route("/redis", methods=["GET"])
def route_redis():

    if request.remote_addr != "127.0.0.1":
        return "Forbidden :(", 403

    key = request.args.get("key")
    if key == "" or key is None:
        return "key must be specified"

    if redis.exists(key) is False:
        return "key not found"

    t = redis.type(key)

    if t == b"string":
        value = redis.get(key)
    elif t == b"list":
        value = "\n".join([i.decode() for i in redis.lrange(key, 0, -1)])
    else:
        value = "the type of the value is neither string or list :("

    return value


def init_flag():

    flag = os.environ["FLAG"]
    redis.set("FLAG", flag)


init_flag()
app.run(host="0.0.0.0", port=5000, debug=False)
