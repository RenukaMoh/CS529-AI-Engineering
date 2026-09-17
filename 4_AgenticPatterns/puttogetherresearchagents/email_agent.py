# SMTP Email Notifications

import os
import smtplib
from typing import Dict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an HTML email using Gmail SMTP instead of SendGrid."""

    try:
        # Load credentials from environment
        sender_email = os.getenv("GMAIL_SENDER")            # e.g., your@gmail.com
        app_password = os.getenv("GMAIL_APP_PASSWORD")      # 16-char App Password
        recipient_email = os.getenv("GMAIL_RECIPIENT")      # e.g., someone@example.com

        # Validate environment setup
        if not sender_email or not app_password or not recipient_email:
            return {
                "status": "error",
                "message": "Missing GMAIL_SENDER, GMAIL_APP_PASSWORD, or GMAIL_RECIPIENT env variables."
            }

        # Compose the email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        # Attach HTML content
        msg.attach(MIMEText(html_body, "html"))

        # Send via Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        return {"status": "success", "message": f"Email sent to {recipient_email}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)

