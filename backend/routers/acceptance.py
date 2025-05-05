from fastapi import APIRouter, Request
from backend.db import acceptance_collection
import openai
import os
import traceback

router = APIRouter()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

@router.post("/acceptance-criteria")
async def generate_acceptance_criteria(request: Request):
    data = await request.json()
    story = data.get("story")
    if not story:
        return {"criteria": "⚠️ No user story provided."}

    prompt = f"Generate acceptance criteria for the following user story:\n\n{story}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        criteria = response.choices[0].message["content"].strip()
        acceptance_collection.insert_one({"story": story, "criteria": criteria})
        return {"criteria": criteria}
    except Exception as e:
        print("❌ Error generating acceptance criteria:", e)
        traceback.print_exc()
        return {"criteria": f"❌ Failed to generate: {e}"}
