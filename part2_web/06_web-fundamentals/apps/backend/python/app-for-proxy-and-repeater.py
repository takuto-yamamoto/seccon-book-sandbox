from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return """<!DOCTYPE html>
    <html>
        <head></head>
        <body>
            <form action="/api" method="POST">
                <input type="hidden" name="passcode" value="wrong_passcode">
                <input type="submit" value="Get FLAG">
            </form>
        </body>
    </html>"""


@app.route("/api", methods=["POST"])
def api():
    if request.form["passcode"] == "correct_passcode":
        return "Correct!"
    else:
        return "Wrong..."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
