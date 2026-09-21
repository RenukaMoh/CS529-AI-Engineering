# SMTP Notifications - I used this custom tool
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os

# Define the expected input schema for this tool
class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

# Define the tool class 
class PushNotificationTool(BaseTool):
    """
    A CrewAI custom tool that sends a push notification — implemented via email.
    This version uses Gmail's SMTP server to send an email with the message.
    The recipient and sender are controlled via environment variables.
    """
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user. "
        "It sends an email using Gmail SMTP."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        try:
            # Load email credentials and recipient from environment variables
            sender_email = os.getenv("GMAIL_SENDER")
            app_password = os.getenv("GMAIL_APP_PASSWORD")
            recipient_email = os.getenv("GMAIL_RECIPIENT")  # NEW: recipient via env var

            # Ensure all required environment variables are set
            if not sender_email or not app_password or not recipient_email:
                return "❌ Missing GMAIL_SENDER, GMAIL_APP_PASSWORD or GMAIL_RECIPIENT in environment."

            # Create the email content
            msg = MIMEMultipart() # Multipurpose Internet Mail Extensions(MIME)
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = "📈 Stock Notification from CrewAI"
            msg.attach(MIMEText(message, "plain")) # message is an method argument

            # Connect to Gmail SMTP and send the email
            server = smtplib.SMTP("smtp.gmail.com", 587) # Simple Mail Transfer Protocol
            #TLS the protocol that encrypts and protects your connection while sending emails via SMTP.
            server.starttls() # Transport Layer Security(TLS)
            server.login(sender_email, app_password)
            server.send_message(msg)
            server.quit()

            return f"✅ Email sent to {recipient_email}"
        except Exception as e:
            # Catch and return any errors that occur during the process
            return f"❌ Error sending email: {str(e)}"

# Optional testing code for your push notification
if __name__ == "__main__":
    tool = PushNotificationTool()
    print("Using Tool:", tool.name)
    result = tool.run(message="📈 CrewAI stock alert: Top pick is Nvidia (NVDA).")
    print(result)

