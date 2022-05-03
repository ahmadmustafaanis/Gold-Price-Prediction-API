import flask
from cfg import models as model_list
from flask import jsonify, render_template, request
from utils import Predictions

models = model_list.models  # list of all models from which to select

app = flask.Flask(__name__)
app.config["debug"] = True


@app.route("/")
def home():
    return render_template("index.html", models=models)


@app.route("/predict", methods=["POST"])
def predict_gold():
    """
    Given the date, predict the gold price for next date
    """
    # print(request.form.get)
    try:
        model = Predictions(request.form.get("model_name"))
        pred = model.predict(request.form.get("date"))
    except FileNotFoundError:  # get value from curl header
        try:
            model = Predictions(request.headers.get("model_name"))
            pred = model.predict(request.headers.get("date"))
        except FileNotFoundError:
            print("Wrong path")
            exit(-1)

    return jsonify(
        {
            "given_date": request.form.get("date"),
            "next_date": model.get_next_date(),
            "price": pred,
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
