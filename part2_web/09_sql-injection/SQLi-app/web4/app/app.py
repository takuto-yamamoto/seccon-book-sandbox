#! python3


import pymysql
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

app.config["MYSQL_DATABASE_HOST"] = "db"
app.config["MYSQL_DATABASE_DB"] = "db"
app.config["MYSQL_DATABASE_USER"] = "user"
app.config["MYSQL_DATABASE_PASSWORD"] = "password"

# we have two tables in database:
# kv(id, k, v) and secrets(id, data)

_db = pymysql.connect(host="db", db="db", user="user", password="password")


def get_db():
    _db.ping(reconnect=True)
    return _db


@app.route("/", methods=["GET"])
def route_index():

    db = get_db()

    sql = "select k,v from kv;"

    try:
        cur = db.cursor()
        cur.execute(sql)
    except Exception:
        return "Error", 500

    data = cur.fetchall()
    cur.close()

    return render_template("index.html", data=data, ndata=len(data))


@app.route("/search", methods=["GET"])
def route_search_index():

    key = request.args.get("key")
    if key is None:
        key = ""

    sql = "select k,v from kv where k like %s;"

    db = get_db()
    try:
        cur = db.cursor()
        cur.execute(sql, ("%{}%".format(key)))

    except Exception:
        cur.close()
        return "Error", 500

    data = cur.fetchall()
    cur.close()

    return render_template("index.html", data=data, ndata=len(data))


@app.route("/add", methods=["GET"])
def route_add_index():
    return render_template("add.html", msg=None)


@app.route("/add", methods=["POST"])
def route_add_do():

    key = request.form.get("key")
    value = request.form.get("value")

    if key is None or value is None or key == "" or value == "":
        msg = "both key and value cannot be null"
        return render_template("add.html", msg=msg)

    sql = "insert into kv (k, v) values('" + key + "', '" + value + "');"

    db = get_db()
    try:
        cur = db.cursor()
        cur.execute(sql)

    except pymysql.err.IntegrityError:
        cur.close()
        msg = "key is already used"
        return render_template("add.html", msg=msg)

    except Exception as e:
        cur.close()
        return str(e), 500

    db.commit()
    cur.close()

    return redirect("/")


app.run(host="0.0.0.0", debug=False)
