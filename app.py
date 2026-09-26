
import os
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# Uses the EC2 instance's LabInstanceProfile automatically.
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("SecurityAnalysisEvents")


def analyze_security_input(security_input):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""
You are a cloud cybersecurity assistant for students and beginner
security analysts.

Analyze the following security-related input:

{security_input}

Return a concise analysis using these headings:
Risk Level:
Analysis:
Recommended Action:

Identify suspicious indicators, security risks, or cloud
configuration concerns. Keep the response clear and practical.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text


def save_event(security_input, result):
    event = {
        "event_id": str(uuid.uuid4()),
        "input": security_input,
        "analysis": result,
        "time": datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),
    }
    table.put_item(Item=event)


def get_recent_events():
    response = table.scan()
    items = response.get("Items", [])

    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    items.sort(key=lambda event: event.get("time", ""), reverse=True)
    return items[:5]


@app.route("/", methods=["GET", "POST"])
def dashboard():
    result = None
    notice = None

    if request.method == "POST":
        security_input = request.form.get(
            "security_input", ""
        ).strip()

        if not security_input:
            result = "Please enter security information to analyze."
        else:
            try:
                result = analyze_security_input(security_input)
                try:
                    save_event(security_input, result)
                except (BotoCoreError, ClientError) as error:
                    app.logger.exception("DynamoDB event save failed")
                    notice = "Analysis completed, but saving the event failed."
            except Exception:
                app.logger.exception("Gemini analysis failed")
                result = "Analysis service is temporarily unavailable."

    try:
        events = get_recent_events()
    except (BotoCoreError, ClientError):
        app.logger.exception("DynamoDB event retrieval failed")
        events = []
        notice = "Recent security events are temporarily unavailable."

    return render_template(
        "index.html",
        result=result,
        events=events,
        notice=notice
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

