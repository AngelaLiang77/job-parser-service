import os
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def parse_job_email():
    """Parses email content to find company and job title."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    subject = data.get('subject', '')

    company = "Unknown"
    title = "Unknown"

    match = re.search(r"application for the (.*?) position at (.*?)$", subject, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        company = match.group(2).strip().replace('.', '')

    return jsonify({"company": company, "job_title": title})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))