from fastapi import APIRouter, Request
from openai import ChatCompletion
import os
import openai

router = APIRouter()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

@router.post("/estimate-points")
async def estimate_story_points(request: Request):
    data = await request.json()
    story = data.get("story", "")

    if not story:
        return {"points": "❌ No story provided."}

    prompt = f"Estimate story points (1 to 13) for this task:\n\n{story}\n\nRespond with only a number."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        points = response.choices[0].message["content"].strip()
        return {"points": points}
    except Exception as e:
        return {"points": f"❌ Failed to estimate story points.\n\n{e}"}
