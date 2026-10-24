import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
LOCAL_FILE = ROOT / "data" / "local_store.json"

def _read_local():
    if not LOCAL_FILE.exists():
        return {"profiles": {}, "recommendations": {}}
    try:
        return json.loads(LOCAL_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"profiles": {}, "recommendations": {}}

def _write_local(data):
    LOCAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def _mongo_collection(name):
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return None
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=1500)
        client.admin.command("ping")
        db = client[os.getenv("MONGODB_DB", "careerguide_ai")]
        return db[name]
    except Exception:
        return None

def save_profile(profile):
    profile = dict(profile)
    profile["updated_at"] = datetime.now(timezone.utc).isoformat()
    collection = _mongo_collection("profiles")
    if collection is not None:
        collection.update_one({"student_id": profile["student_id"]}, {"$set": profile}, upsert=True)
        return profile
    data = _read_local()
    data["profiles"][profile["student_id"]] = profile
    _write_local(data)
    return profile

def get_profile(student_id):
    collection = _mongo_collection("profiles")
    if collection is not None:
        result = collection.find_one({"student_id": student_id}, {"_id": 0})
        return result
    return _read_local().get("profiles", {}).get(student_id)

def save_recommendations(student_id, recommendations):
    collection = _mongo_collection("recommendations")
    record = {
        "student_id": student_id,
        "recommendations": recommendations,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    if collection is not None:
        collection.update_one({"student_id": student_id}, {"$set": record}, upsert=True)
        return
    data = _read_local()
    data["recommendations"][student_id] = record
    _write_local(data)
