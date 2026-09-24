from flask import Flask, render_template, request

app = Flask(__name__)

events = []

@app.route("/", methods=["GET", "POST"])
def dashboard():
    result = None

    if request.method == "POST":
        security_input = request.form.get("security_input", "").strip()

        if not security_input:
            result = "Please enter security information to analyze."
        else:
            result = (
                "Security analysis received. AI-powered analysis will be "
                "connected in the next development step."
            )
            events.insert(0, security_input)

    return render_template(
        "index.html",
        result=result,
        events=events[:5]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
