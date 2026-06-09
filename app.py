"""WebCalc — веб-калькулятор на Flask (вся логика на Python)."""

from flask import Flask, redirect, render_template, request, session, url_for

from calculator_ui import CalculatorState

app = Flask(__name__)
app.secret_key = "webcalc-dev-key"


def _get_state() -> CalculatorState:
    return CalculatorState.from_dict(session.get("calc"))


def _save_state(state: CalculatorState) -> None:
    session["calc"] = state.to_dict()


@app.route("/", methods=["GET", "POST"])
def index():
    state = _get_state()

    if request.method == "POST":
        action = request.form.get("action", "")
        value = request.form.get("value")
        try:
            state.handle(action, value)
        except ValueError:
            state.error = "Некорректное действие"
        _save_state(state)
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        display=state.display(),
        error=state.error,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
