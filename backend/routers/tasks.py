from fastapi import APIRouter, Request
from backend.db import breakdown_collection

router = APIRouter()

@router.post("/breakdown")
async def add_task(req: Request):
    data = await req.json()
    task = data.get("task")
    user = data.get("user")
    if task and user:
        breakdown_collection.insert_one({"task": task, "user": user})
        return {"message": "Task added successfully"}
    return {"error": "Missing task or user"}

@router.get("/breakdown")
async def get_all_tasks():
    return [{"task": doc["task"], "user": doc["user"]} for doc in breakdown_collection.find()]
