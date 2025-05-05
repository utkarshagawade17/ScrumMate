from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from backend.routers import tasks, email, standups
from backend.routers import acceptance
from backend.routers import estimations
from backend.routers import standups
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your routers
app.include_router(tasks.router)
app.include_router(email.router)
app.include_router(standups.router)
app.include_router(acceptance.router)
app.include_router(estimations.router)

# ✅ Scheduler for daily email
scheduler = BackgroundScheduler()

def send_daily_standup_email():
    try:
        response = requests.post("http://localhost:8000/standup-summary", json={})
        summary = response.json().get("summary", "⚠️ No summary generated.")
        recipients = ["teammate1@example.com", "teammate2@example.com"]
        for to in recipients:
            requests.post("http://localhost:8000/send-email", json={
                "to": to,
                "subject": "📢 Daily Standup Summary",
                "content": summary
            })
        print("✅ Daily standup email sent")
    except Exception as e:
        print("❌ Failed to send summary email:", e)

scheduler.add_job(send_daily_standup_email, "cron", day_of_week="mon-fri", hour=9, minute=0)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
