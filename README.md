
# AI Cloud Security Operations Dashboard

## Project Overview

This project is a web-based cybersecurity dashboard developed for the SDI-3213 Cloud Computing course.

Users can submit phishing emails, security logs, cloud configurations, and AWS security questions. Google Gemini analyzes the submitted information and provides security assessments and recommended actions.

## Features

- Web-based security dashboard
- Security information submission form
- AI-powered analysis using Google Gemini
- Risk assessments and recommended security actions
- Recent security event history with timestamps
- Flask backend with HTML and CSS frontend

## Architecture

The application uses Python and Flask to process user requests.

Application workflow:

1. A user enters security-related information.
2. Flask receives and validates the submission.
3. The backend sends the information to the Google Gemini API.
4. Gemini generates a security assessment.
5. Flask displays the result and records a recent security event.

AWS EC2 is the intended production hosting environment. The deployed application will integrate an additional AWS service using the EC2 LabInstanceProfile.

## Technologies

- Python
- Flask
- Google Gemini API
- HTML and CSS
- Git and GitHub
- Amazon EC2

## Installation

Clone the repository:

```bash
git clone https://github.com/adejayz/ai-cloud-security-dashboard.git
cd ai-cloud-security-dashboard
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure the Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Start the application:

```bash
python app.py
```

Open port 5000 in your local development environment to access the dashboard.

## Usage

1. Open the dashboard in your browser.
2. Enter a phishing email, security log, cloud configuration, or AWS security question.
3. Click Analyze.
4. Review the generated risk assessment and recommendations.
5. View recent submissions in the Recent Security Events section.

## Security

The Gemini API key is loaded from an environment variable rather than stored in the repository.

The planned AWS deployment uses LabInstanceProfile for AWS service access without hardcoded AWS credentials.

Only necessary application and administration ports should be permitted by the EC2 security group.

## Deployment

The application is being prepared for deployment to AWS EC2 through AWS Academy Learner Lab.

The production URL, additional AWS service integration, and deployment configuration will be documented after they have been implemented and verified.

## Project Management

Development is tracked using GitHub Issues, labels, a milestone, and a GitHub Project board.

## Author

Juwon Shomade
