from fastapi import APIRouter, Request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/send-email")
async def send_email(request: Request):
    data = await request.json()
    to_email = data.get("to")
    subject = data.get("subject", "Daily Scrum Update")
    content = data.get("content", "")

    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return {"message": "Email sent successfully", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}
