from flask import Flask, make_response

from lib.sample import hoge


app = Flask(__name__)


@app.route("/api", methods=["GET"])
def sample():
    """APIのサンプル"""

    result: str = hoge()
    response = make_response()
    response.data: str = result
    response.headers["Content-Type"] = "text/plain"
    return response
