import flask
from cfg import models as model_list
from flask import jsonify, render_template, request

models = model_list.models  # list of all models from which to select

app = flask.Flask(__name__)
app.config["debug"] = True


@app.route("/")
def home():
    return render_template("index.html", models=list(models.keys()))


@app.route("/predict", methods=["POST"])
def predict_gold():
    """
    Given the date, predict the gold price for next date
    """
    # print(request.form.get)
    try:
        model_name = request.form.get("model_name")
        date_given = request.form.get("date")
        model = models[model_name]()
        pred = model.predict(date_given)
    except KeyError:  # get value from curl header
        try:
            model_name = request.headers.get("model_name")
            date_given = request.headers.get("date")
            model = models[model_name]()
            pred = model.predict(date_given)
        except FileNotFoundError:
            print("Wrong path")
            exit(-1)

    return jsonify(
        {
            "given_date": date_given,
            "next_date": model.get_next_date(date_given),
            "price": pred,
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
