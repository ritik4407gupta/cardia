/**
 * Cardia — front-end interactions
 * Handles live range readouts, the demo monitor readout, client-side
 * validation, and the async call to the Flask /predict endpoint.
 */

(function () {
  "use strict";

  /* ---------------------------------------------------------------------
   * Live range slider readouts
   * ------------------------------------------------------------------- */
  const rangeBindings = [
    { input: "age", label: "ageVal" },
    { input: "max_hr", label: "maxHrVal" },
    { input: "oldpeak", label: "oldpeakVal" },
  ];

  rangeBindings.forEach(({ input, label }) => {
    const inputEl = document.getElementById(input);
    const labelEl = document.getElementById(label);
    if (!inputEl || !labelEl) return;
    const sync = () => {
      const val = input === "oldpeak" ? parseFloat(inputEl.value).toFixed(1) : inputEl.value;
      labelEl.textContent = val;
    };
    inputEl.addEventListener("input", sync);
    sync();
  });

  /* ---------------------------------------------------------------------
   * Hero demo monitor — a gentle idle animation, purely decorative
   * ------------------------------------------------------------------- */
  const demoHr = document.getElementById("demoHr");
  if (demoHr) {
    let base = 72;
    setInterval(() => {
      base = 70 + Math.round(Math.random() * 6);
      demoHr.textContent = base;
    }, 2600);
  }

  /* ---------------------------------------------------------------------
   * Form submission → /predict
   * ------------------------------------------------------------------- */
  const form = document.getElementById("predictForm");
  const btn = document.getElementById("predictBtn");
  const btnLabel = btn ? btn.querySelector(".btn-label") : null;
  const btnSpinner = btn ? btn.querySelector(".btn-spinner") : null;
  const errorBox = document.getElementById("formError");
  const errorText = document.getElementById("formErrorText");
  const resultWrap = document.getElementById("resultWrap");
  const resultCard = document.getElementById("resultCard");
  const resultIcon = document.getElementById("resultIcon");
  const resultTitle = document.getElementById("resultTitle");
  const resultText = document.getElementById("resultText");
  const probWrap = document.getElementById("resultProbWrap");
  const probFill = document.getElementById("resultProbFill");
  const probLabel = document.getElementById("resultProbLabel");

  function setLoading(isLoading) {
    if (!btn) return;
    btn.disabled = isLoading;
    btnLabel.classList.toggle("d-none", isLoading);
    btnSpinner.classList.toggle("d-none", !isLoading);
  }

  function showError(message) {
    errorText.textContent = message;
    errorBox.classList.remove("d-none");
  }

  function hideError() {
    errorBox.classList.add("d-none");
  }

  function renderResult(data) {
    resultWrap.classList.remove("d-none");
    resultCard.classList.remove("is-high", "is-low");

    if (data.risk === "high") {
      resultCard.classList.add("is-high");
      resultIcon.className = "bi bi-exclamation-triangle-fill";
      resultTitle.textContent = "High Risk of Heart Disease";
      resultText.textContent =
        "Your inputs align with patterns associated with elevated cardiac risk. " +
        "Please consult a healthcare professional for a full clinical evaluation.";
    } else {
      resultCard.classList.add("is-low");
      resultIcon.className = "bi bi-check-circle-fill";
      resultTitle.textContent = "Low Risk of Heart Disease";
      resultText.textContent =
        "Your inputs align with patterns associated with lower cardiac risk. " +
        "Keep up heart-healthy habits and continue regular checkups.";
    }

    if (typeof data.probability === "number") {
      probWrap.classList.remove("d-none");
      const pct = Math.round(data.probability * 100);
      probLabel.textContent = "Model confidence: " + pct + "%";
      requestAnimationFrame(() => {
        probFill.style.width = pct + "%";
      });
    } else {
      probWrap.classList.add("d-none");
    }

    resultWrap.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      hideError();

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      const payload = {
        age: document.getElementById("age").value,
        sex: document.getElementById("sex").value,
        chest_pain: document.getElementById("chest_pain").value,
        resting_bp: document.getElementById("resting_bp").value,
        cholesterol: document.getElementById("cholesterol").value,
        fasting_bs: document.getElementById("fasting_bs").value,
        resting_ecg: document.getElementById("resting_ecg").value,
        max_hr: document.getElementById("max_hr").value,
        exercise_angina: document.getElementById("exercise_angina").value,
        oldpeak: document.getElementById("oldpeak").value,
        st_slope: document.getElementById("st_slope").value,
      };

      setLoading(true);
      try {
        const response = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await response.json();

        if (!response.ok || !data.success) {
          const message =
            (data.errors && data.errors.join(" ")) ||
            "Something went wrong while analyzing your inputs. Please try again.";
          showError(message);
          return;
        }

        renderResult(data);
      } catch (err) {
        showError("Unable to reach the prediction service. Please check your connection and try again.");
      } finally {
        setLoading(false);
      }
    });
  }
})();
