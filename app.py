
from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    attendance = float(request.form["attendance"])
    study_hours = float(request.form["study_hours"])
    internal_marks = float(request.form["internal_marks"])
    previous_marks = float(request.form["previous_marks"])
    assignments = float(request.form["assignments"])

    data = pd.DataFrame([{
        "attendance": attendance,
        "study_hours": study_hours,
        "internal_marks": internal_marks,
        "previous_marks": previous_marks,
        "assignments": assignments
    }])

    prediction = float(model.predict(data)[0])

    bonus = 0

    if attendance >= 90:
        bonus += 5

    if study_hours >= 4:
        bonus += 5

    if assignments >= 8:
        bonus += 5

    if previous_marks >= 80:
        bonus += 5

    final_score = min(100, prediction + bonus)

    if final_score >= 90:
        grade = "A+"
        status = "Outstanding"

    elif final_score >= 80:
        grade = "A"
        status = "Excellent"

    elif final_score >= 70:
        grade = "B"
        status = "Good"

    elif final_score >= 60:
        grade = "C"
        status = "Average"

    elif final_score >= 40:
        grade = "D"
        status = "Pass"

    else:
        grade = "F"
        status = "Fail"

    recommendations = []

    if attendance < 75:
        recommendations.append("Improve attendance above 75%")

    if study_hours < 3:
        recommendations.append("Study at least 3-4 hours daily")

    if assignments < 7:
        recommendations.append("Complete assignments regularly")

    if internal_marks < 20:
        recommendations.append("Improve internal assessment marks")

    if previous_marks < 60:
        recommendations.append("Revise previous concepts")

    if len(recommendations) == 0:
        recommendations.append(
            "Excellent performance. Keep maintaining your current study habits."
        )

    return render_template(
        "result.html",
        score=round(final_score, 2),
        grade=grade,
        status=status,
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )
#flask
#pandas
#numpy
#scikit-learn
#joblib
