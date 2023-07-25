import os

from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request
)
import pandas as pd

from lib.optimizers.car_student_assign_problem import CarGroupOpt
from lib.sample import hoge


app = Flask(__name__)


def check_request(request):
    """リクエストに学生データと車データが含まれているか確認する関数"""
    # 各ファイルを取得する
    students = request.files["students"]
    cars = request.files["cars"]

    # ファイルが選択されているか確認
    if students.filename == "":
        # 学生データが選ばれていません
        return False
    if cars.filename == "":
        # 車データが選ばれていません
        return False

    return True


def preprocess(request):
    """リクエストデータを受け取り、データフレームに変換する関数"""
    # 各ファイルを取得する
    students = request.files["students"]
    cars = request.files["cars"]
    # pandas で読み込む
    students_df = pd.read_csv(students)
    cars_df = pd.read_csv(cars)
    return students_df, cars_df


def postprocess(solution_df):
    """最適化結果をHTML形式に変換する関数"""
    solution_html = solution_df.to_html(header=True, index=False)
    return solution_html


@app.route("/api", methods=["GET"])
def sample():
    """APIのサンプル"""

    result: str = hoge()

    # NOTE: QueryStringParameters を取得
    query_string_content: str = request.args.get("content")

    if query_string_content is not None and query_string_content == "str":
        # strを返す
        response = make_response()
        response.data: str = result
        response.headers["Content-Type"] = "text/plain"
        return response
    else:
        # jsonを返す
        return jsonify({"message": result})


@app.route("/", methods=["GET", "POST"])
def solve():
    """最適化の実行と結果の表示を行う関数"""
    # トップページを表示する（GETリクエストがきた場合）
    if request.method == "GET":
        return render_template("index.html", solution_html=None)

    # POSTリクエストである「最適化を実行」ボタンが押された場合に実行
    # データがアップロードされているかチェックする。適切でなければ元のページ（トップページ）に戻る
    if not check_request(request):
        return redirect(request.url)

    # 前処理（データ読み込み）
    students_df, cars_df = preprocess(request)
    # 最適化実行
    result: dict = CarGroupOpt(students_df, cars_df).solve()
    if result["success"] is False:
        return render_template("index.html", solution_html=result["status"])

    # 後処理（最適化結果をHTMLに表示できる形式にする）
    solution_df: pd.DataFrame = result["result"]
    solution_html = postprocess(solution_df)
    return render_template("index.html", solution_html=solution_html)


@app.route("/download", methods=["POST"])
def download():
    """リクエストに含まれるHTMLの表形式データをcsv形式に変換してダウンロードする関数"""
    solution_html = request.form.get("solution_html")
    solution_df = pd.read_html(solution_html)[0]
    solution_csv = solution_df.to_csv(index=False)
    response = make_response()
    response.data = solution_csv
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = "attachment; filename=solution.csv"
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT','5000'))
