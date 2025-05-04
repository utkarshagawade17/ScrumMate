from fastapi import APIRouter, Request
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@router.post("/acceptance-criteria")
async def generate_acceptance_criteria(req: Request):
    data = await req.json()
    story = data.get("story", "")

    if not story:
        return {"criteria": "No story provided."}

    prompt = f"Write clear and testable acceptance criteria for the following user story:\n\n{story}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        criteria = response.choices[0].message.content.strip()
        return {"criteria": criteria}
    except Exception as e:
        print("❌ Criteria generation error:", e)
        return {"criteria": "Failed to generate criteria."}
