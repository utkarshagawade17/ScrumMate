from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["scrum_slayer"]

# ✅ Add this if missing
breakdown_collection = db["breakdown"]
standups_collection = db["standups"]
