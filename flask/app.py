import os

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODEL_DIR, "knn_heart_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "heart_scaler.pkl"))
expected_columns = joblib.load(os.path.join(MODEL_DIR, "heart_columns.pkl"))

SEX_OPTIONS = ["M", "F"]
CHEST_PAIN_OPTIONS = ["ATA", "NAP", "TA", "ASY"]
FASTING_BS_OPTIONS = [0, 1]
RESTING_ECG_OPTIONS = ["Normal", "ST", "LVH"]
EXERCISE_ANGINA_OPTIONS = ["Y", "N"]
ST_SLOPE_OPTIONS = ["Up", "Flat", "Down"]

FIELD_RANGES = {
    "age": (18, 100, 40),
    "resting_bp": (80, 200, 120),
    "cholesterol": (100, 600, 200),
    "max_hr": (60, 220, 150),
    "oldpeak": (0.0, 6.0, 1.0),
}


@app.route("/")
def index():
    """Render the single-page application."""
    return render_template(
        "index.html",
        sex_options=SEX_OPTIONS,
        chest_pain_options=CHEST_PAIN_OPTIONS,
        fasting_bs_options=FASTING_BS_OPTIONS,
        resting_ecg_options=RESTING_ECG_OPTIONS,
        exercise_angina_options=EXERCISE_ANGINA_OPTIONS,
        st_slope_options=ST_SLOPE_OPTIONS,
        field_ranges=FIELD_RANGES,
    )


def _validate_payload(data):
    """Validate incoming form data against the same ranges/options the
    original Streamlit widgets enforced. Returns (cleaned_dict, errors)."""
    errors = []
    cleaned = {}

    def _get_number(key, low, high, cast):
        raw = data.get(key)
        try:
            value = cast(raw)
        except (TypeError, ValueError):
            errors.append(f"'{key}' must be a valid number.")
            return None
        if not (low <= value <= high):
            errors.append(f"'{key}' must be between {low} and {high}.")
            return None
        return value

    cleaned["age"] = _get_number("age", 18, 100, int)
    cleaned["resting_bp"] = _get_number("resting_bp", 80, 200, int)
    cleaned["cholesterol"] = _get_number("cholesterol", 100, 600, int)
    cleaned["max_hr"] = _get_number("max_hr", 60, 220, int)
    cleaned["oldpeak"] = _get_number("oldpeak", 0.0, 6.0, float)

    sex = data.get("sex")
    if sex not in SEX_OPTIONS:
        errors.append("'sex' must be one of M, F.")
    cleaned["sex"] = sex

    chest_pain = data.get("chest_pain")
    if chest_pain not in CHEST_PAIN_OPTIONS:
        errors.append("'chest_pain' must be one of ATA, NAP, TA, ASY.")
    cleaned["chest_pain"] = chest_pain

    try:
        fasting_bs = int(data.get("fasting_bs"))
    except (TypeError, ValueError):
        fasting_bs = None
    if fasting_bs not in FASTING_BS_OPTIONS:
        errors.append("'fasting_bs' must be 0 or 1.")
    cleaned["fasting_bs"] = fasting_bs

    resting_ecg = data.get("resting_ecg")
    if resting_ecg not in RESTING_ECG_OPTIONS:
        errors.append("'resting_ecg' must be one of Normal, ST, LVH.")
    cleaned["resting_ecg"] = resting_ecg

    exercise_angina = data.get("exercise_angina")
    if exercise_angina not in EXERCISE_ANGINA_OPTIONS:
        errors.append("'exercise_angina' must be Y or N.")
    cleaned["exercise_angina"] = exercise_angina

    st_slope = data.get("st_slope")
    if st_slope not in ST_SLOPE_OPTIONS:
        errors.append("'st_slope' must be one of Up, Flat, Down.")
    cleaned["st_slope"] = st_slope

    return cleaned, errors


@app.route("/predict", methods=["POST"])
def predict():
    """Run the exact same feature-engineering + prediction pipeline as the
    original Streamlit app and return a JSON result for the front end."""
    data = request.get_json(silent=True) or request.form

    cleaned, errors = _validate_payload(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    # --- Identical feature engineering to the original Streamlit app -----
    raw_input = {
        "Age": cleaned["age"],
        "RestingBP": cleaned["resting_bp"],
        "Cholesterol": cleaned["cholesterol"],
        "FastingBS": cleaned["fasting_bs"],
        "MaxHR": cleaned["max_hr"],
        "Oldpeak": cleaned["oldpeak"],
        "Sex_" + cleaned["sex"]: 1,
        "ChestPainType_" + cleaned["chest_pain"]: 1,
        "RestingECG_" + cleaned["resting_ecg"]: 1,
        "ExerciseAngina_" + cleaned["exercise_angina"]: 1,
        "ST_Slope_" + cleaned["st_slope"]: 1,
    }

    input_df = pd.DataFrame([raw_input])

    # Fill in missing columns with 0s
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder columns
    input_df = input_df[expected_columns]

    # Scale the input
    scaled_input = scaler.transform(input_df)

    # Make prediction
    prediction = int(model.predict(scaled_input)[0])

    probability = None
    if hasattr(model, "predict_proba"):
        try:
            probability = float(model.predict_proba(scaled_input)[0][prediction])
        except Exception:
            probability = None

    return jsonify(
        {
            "success": True,
            "prediction": prediction,
            "risk": "high" if prediction == 1 else "low",
            "probability": probability,
        }
    )


@app.errorhandler(404)
def not_found(_e):
    return render_template("index.html", not_found=True), 404


if __name__ == "__main__":
    app.run(debug=True)