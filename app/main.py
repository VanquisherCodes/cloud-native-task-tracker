import os
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId

# =========================
# MongoDB configuration
# =========================

# For now:
# - When running locally without Docker, it will try localhost.
# - When we use Docker Compose, it will get MONGO_URL from environment.
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "tasktracker")

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
tasks_collection = db["tasks"]


# =========================
# Helper functions
# =========================

def bson_to_str(doc: dict) -> dict:
    """
    Convert MongoDB's ObjectId to str so FastAPI/Pydantic can serialize it.
    """
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc


# =========================
# Pydantic models
# =========================

class TaskBase(BaseModel):
    title: str = Field(..., example="Finish DevOps project")
    description: Optional[str] = Field(
        default=None,
        example="Implement CI pipeline with GitHub Actions",
    )
    status: str = Field(
        default="pending",
        example="pending",  # could be: pending, in_progress, done
    )


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: str = Field(..., example="66f1d51ab9a0b3421a5c1234")


# =========================
# FastAPI app
# =========================

app = FastAPI(
    title="Cloud-Native Task Tracker API",
    description="A simple task tracker API built with FastAPI and MongoDB.",
    version="1.0.0",
)


@app.get("/", tags=["health"])
def read_root():
    return {"message": "Task Tracker API is running"}


@app.post("/tasks", response_model=Task, tags=["tasks"])
def create_task(task: TaskCreate):
    """
    Create a new task and store it in MongoDB.
    """
    doc = task.dict()
    result = tasks_collection.insert_one(doc)
    created = tasks_collection.find_one({"_id": result.inserted_id})
    created = bson_to_str(created)

    return Task(
        id=created["_id"],
        title=created["title"],
        description=created.get("description"),
        status=created["status"],
    )


@app.get("/tasks", response_model=List[Task], tags=["tasks"])
def list_tasks():
    """
    List all tasks.
    """
    tasks = []
    for t in tasks_collection.find():
        t = bson_to_str(t)
        tasks.append(
            Task(
                id=t["_id"],
                title=t["title"],
                description=t.get("description"),
                status=t["status"],
            )
        )
    return tasks


@app.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def get_task(task_id: str):
    """
    Get a single task by its ID.
    """
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task id format")

    doc = tasks_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Task not found")

    doc = bson_to_str(doc)
    return Task(
        id=doc["_id"],
        title=doc["title"],
        description=doc.get("description"),
        status=doc["status"],
    )


@app.delete("/tasks/{task_id}", tags=["tasks"])
def delete_task(task_id: str):
    """
    Delete a task by its ID.
    """
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task id format")

    result = tasks_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
