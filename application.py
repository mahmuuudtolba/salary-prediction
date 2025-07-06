import joblib
import numpy as np
from config.path_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request

app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None

    if request.method == 'POST':
        # Numeric inputs
        fnlwgt = float(request.form["num__fnlwgt"])
        age = float(request.form["num__age"])
        education_num = float(request.form["num__education-num"])
        capital_gain = float(request.form["num__capital-gain"])
        capital_loss = float(request.form["num__capital-loss"])
        hours_per_week = float(request.form["num__hours-per-week"])

        # Binary categorical flags (as float 0.0 or 1.0)
        marital_married = float(request.form.get("cat__marital-status_ Married-civ-spouse", 0.0))
        marital_never = float(request.form.get("cat__marital-status_ Never-married", 0.0))
        rel_husband = float(request.form.get("cat__relationship_ Husband", 0.0))
        rel_wife = float(request.form.get("cat__relationship_ Wife", 0.0))
        occ_exec = float(request.form.get("cat__occupation_ Exec-managerial", 0.0))
        occ_prof = float(request.form.get("cat__occupation_ Prof-specialty", 0.0))

        features = np.array([[fnlwgt, age, education_num, capital_gain, hours_per_week,
                              marital_married, rel_husband, capital_loss,
                              marital_never, occ_exec, occ_prof, rel_wife]])

        prediction = loaded_model.predict(features)[0]

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
