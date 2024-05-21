from flask import Flask, render_template, request
from models.models import Country


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("name")
    # 以下を変更
    all_country = Country.query.all()
    return render_template("index.html", name=name, all_country=all_country)
    # 変更終わり


if __name__ == "__main__":
    app.run(debug=True)
