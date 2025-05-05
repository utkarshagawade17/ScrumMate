from pymongo import MongoClient
import os

# MongoDB client connection
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["scrumslayer"]  # or whatever DB name you're using

# ✅ Define all collections used in routes
standups_collection = db["standups"]
acceptance_collection = db["acceptance"]
estimations_collection = db["estimations"]
tasks_collection = db["tasks"]
breakdown_collection = db["task_breakdown"]
