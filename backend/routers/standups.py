from fastapi import APIRouter, Request
from backend.db import standups_collection
import openai
import os
import traceback

router = APIRouter()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

@router.post("/standup-summary")
async def summarize_standup(req: Request):
    try:
        data = await req.json()
        entries = data.get("entries")
        if not entries:
            entries = [doc.get("text") for doc in standups_collection.find() if doc.get("text")]
    except Exception as e:
        print("❌ Error reading entries:", e)
        traceback.print_exc()
        entries = [doc.get("text") for doc in standups_collection.find() if doc.get("text")]

    if not entries:
        return {"summary": "⚠️ No valid standup entries."}

    prompt = "Summarize the following standup entries into a concise team update:\n\n" + "\n".join(f"- {e}" for e in entries)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message["content"].strip()
        return {"summary": summary}
    except Exception as e:
        print("❌ Summary generation failed:", e)
        traceback.print_exc()
        return {"summary": f"❌ Failed to generate summary: {e}"}

@router.get("/standup-summary")
async def summarize_standup_get():
    return await summarize_standup(Request(scope={"type": "http"}))

@router.get("/standup-entries")
def get_standup_entries():
    entries = list(standups_collection.find({}, {"_id": 0}))
    return {"entries": entries}

@router.post("/standup-entry")
async def add_standup_entry(request: Request):
    data = await request.json()
    text = data.get("text")
    user = data.get("user", "anonymous")

    if not text:
        return {"message": "No text provided."}

    standups_collection.insert_one({"user": user, "text": text})
    return {"message": "Entry added."}
