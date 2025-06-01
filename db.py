from pymongo import MongoClient, errors
import os
import logging

# Replace with your own URI from MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Trigger a server selection to check connection
    client.server_info()
    db = client["resume_screening"]
except errors.ServerSelectionTimeoutError as err:
    logging.error(f"Failed to connect to MongoDB: {err}")
    db = None

if db is not None:
    resumes_collection = db["resumes"]
    job_collection = db["job_descriptions"]
    results_collection = db["screening_results"]

    # Create indexes for performance
    resumes_collection.create_index("filename")
    job_collection.create_index("description")
    results_collection.create_index([("job_id", 1), ("resume_id", 1)])
else:
    resumes_collection = None
    job_collection = None
    results_collection = None
