import flask
from cfg import models as model_list
from flask import jsonify, render_template, request
from predict import Predictions

models = model_list.models

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
    model = Predictions(request.form.get("model_name"))
    pred = model.predict(request.form.get("date"))
    return jsonify(
        {
            "given_date": request.form.get("date"),
            "next_date": model.get_next_date(),
            "price": list(pred["yhat"]),
        },
    )


if __name__ == "__main__":
    app.run()
