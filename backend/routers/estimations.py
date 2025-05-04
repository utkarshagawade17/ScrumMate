from fastapi import APIRouter, Request
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@router.post("/estimate-points")
async def estimate_points(req: Request):
    data = await req.json()
    story = data.get("story", "")
    if not story:
        return {"points": 0}

    prompt = f"Estimate the story points (in Fibonacci series like 1, 2, 3, 5, 8) for the following story:\n\n{story}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content.strip()
        points = int(''.join(filter(str.isdigit, text)))
        return {"points": points}
    except Exception as e:
        print("❌ Estimation error:", e)
        return {"points": 0}
