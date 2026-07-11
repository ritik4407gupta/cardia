# ❤️ Cardia — Heart Stroke Risk Assessment

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-KNN-F7931E?logo=scikitlearn&logoColor=white)

A clinical-styled, single-page Flask web application that estimates heart
disease risk from eleven patient signals, using a trained **K-Nearest
Neighbours** model. This is a full redesign of an original Streamlit
prototype — the machine learning pipeline is untouched; only the delivery
layer has been rebuilt into a modern, responsive web experience.
---

## ✨ Features

- **Clinical-grade UI** — grouped patient-profile / vitals / diagnostic-signs
  form, styled after how a clinician reads a chart
- **Live EKG-style signature visual** in the hero section
- **Interactive range sliders** with live value readouts (Age, Max Heart
  Rate, Oldpeak)
- **Styled dropdowns & number inputs** for categorical and bounded fields
- **Async prediction** via `fetch()` — no page reload, with a loading
  spinner while the model runs
- **Color-coded result cards** (red/high-risk, green/low-risk) with
  confidence bar and micro-animations
- **Client- and server-side validation** matching the original input ranges
- **Fully responsive** — mobile, tablet, and desktop
- **Identical prediction logic** to the original Streamlit app

## 🛠 Technologies Used

| Layer      | Stack                                             |
|------------|----------------------------------------------------|
| Backend    | Flask, scikit-learn, pandas, joblib                 |
| Frontend   | Bootstrap 5, Bootstrap Icons, vanilla JS            |
| Fonts      | Fraunces (display), Public Sans (body), IBM Plex Mono (data) |
| Model      | K-Nearest Neighbours (`knn_heart_model.pkl`)        |


## 📁 Folder Structure

```
project/
│
├── app.py                  # Flask application & prediction endpoint
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html          # Single-page application markup
│
├── static/
│   ├── css/
│   │   └── style.css       # Design system & component styles
│   ├── js/
│   │   └── script.js       # Sliders, validation, async prediction
│   ├── images/
│   │   └── favicon.svg
│
├── models/
│   ├── knn_heart_model.pkl # Trained KNN classifier
│   ├── heart_scaler.pkl    # Fitted StandardScaler
│   └── heart_columns.pkl   # Expected feature column order
```

## ⚙️ Installation

1. **Clone or unzip the project**

   ```bash
   git clone https://github.com/ritik4407gupta/cardia.git
   cd flask
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Usage / How to Run

```bash
flask run
```

The app runs at **http://127.0.0.1:5000** by default. Open it in your
browser, fill out the Patient Profile, Cardiac Vitals, and Diagnostic Signs
sections, and click **Predict My Risk**.


## 🧠 Model Information

- **Algorithm:** K-Nearest Neighbours classifier (`sklearn.neighbors.KNeighborsClassifier`)
- **Preprocessing:** Features are one-hot encoded (matching the original
  training notebook), reindexed against `heart_columns.pkl`, then scaled
  with a fitted `StandardScaler` (`heart_scaler.pkl`) before inference.
- **Inputs:** Age, Sex, Chest Pain Type, Resting Blood Pressure, Cholesterol,
  Fasting Blood Sugar, Resting ECG, Max Heart Rate, Exercise-Induced Angina,
  Oldpeak, ST Slope.
- **Output:** Binary classification — `1` = High Risk, `0` = Low Risk —
  identical to the original Streamlit application's prediction logic.

## 🚀 Future Improvements

- Persist assessment history per session (with explicit user consent)
- Add downloadable PDF summary of results
- Expose a public JSON API with rate limiting for programmatic access
- Add model explainability (e.g. feature contribution) to the result card
- Internationalization / multi-language support


## 👤 Author

**Ritik** — Original model &amp; Streamlit prototype author.
Flask redesign and UI implementation as part of this project.

---

<p align="center"><sub>This tool is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.</sub></p>
