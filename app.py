import os
from datetime import datetime
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

events = []

def analyze_security_input(security_input):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""
You are a cloud cybersecurity assistant for students and beginner security analysts.

Analyze the following security-related input:

{security_input}

Return a concise analysis using these headings:
Risk Level:
Analysis:
Recommended Action:

Identify suspicious indicators, security risks, or cloud configuration concerns.
Keep the response clear and practical.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


@app.route("/", methods=["GET", "POST"])
def dashboard():
    result = None

    if request.method == "POST":
        security_input = request.form.get("security_input", "").strip()

        if not security_input:
            result = "Please enter security information to analyze."
        else:
            try:
                result = analyze_security_input(security_input)

                events.insert(0, {
                    "input": security_input,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            except Exception as error:
                result = f"Analysis service error: {error}"

    return render_template(
        "index.html",
        result=result,
        events=events[:5]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
