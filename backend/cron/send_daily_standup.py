import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 🔐 Setup
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
mongo = MongoClient(os.getenv("MONGO_URI"))
db = mongo["scrum"]
standups_collection = db["standups"]

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAILS = os.getenv("TO_EMAILS").split(",")

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=8)  # ⏰ Every day at 8 AM
def send_standup_summary():
    try:
        entries = list(standups_collection.find({}))
        if not entries:
            print("No standup entries found.")
            return

        combined = "\n".join([f"{e['name']}: {e['update']}" for e in entries])
        prompt = f"Summarize the following team standups:\n\n{combined}\n\nBe concise and highlight blockers."

        summary = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content

        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAILS,
            subject="🧠 Daily Standup Summary",
            html_content=f"<p>{summary.replace('\n', '<br>')}</p>"
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print("✅ Standup email sent!")

    except Exception as e:
        print(f"❌ Error sending standup summary: {e}")

if __name__ == "__main__":
    scheduler.start()
