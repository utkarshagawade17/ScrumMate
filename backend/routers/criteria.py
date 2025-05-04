# backend/routers/criteria.py
from fastapi import APIRouter, Request
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))

@router.post("/generate-criteria")
async def generate_criteria(req: Request):
    data = await req.json()
    task = data.get("task", "")

    prompt = (
        f"Generate 4-5 clear Agile acceptance criteria for the following task:\n\n"
        f"Task: {task}\n\n"
        f"Format as a bullet list using simple language. Respond only with the list."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content.strip()
        criteria = [line.strip("-• ") for line in content.splitlines() if line.strip()]
        return {"criteria": criteria}

    except Exception as e:
        print("❌ Error generating criteria:", e)
        return {"criteria": ["❌ Failed to generate acceptance criteria."]}
