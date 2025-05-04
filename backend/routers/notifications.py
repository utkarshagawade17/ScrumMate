from fastapi import APIRouter, Request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

router = APIRouter()

@router.post("/send-email")
async def send_email(request: Request):
    data = await request.json()
    to_email = data.get("email")
    summary = data.get("summary", "")

    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=to_email,
        subject="📢 Sprint Summary - ScrumMate",
        html_content=f"<p>Hello Team,</p><p>Here is your latest Sprint Summary:</p><p>{summary}</p><p>Regards,<br>ScrumMate Bot</p>",
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return {"status": "Email sent successfully", "code": response.status_code}
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return {"error": "Failed to send email"}
