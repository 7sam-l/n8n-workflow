from fastapi import FastAPI, Query
from typing import Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

API_KEY = os.getenv("YOUTUBE_API_KEY")
app = FastAPI(title="SpeakGenie Workflow API")

OUTPUT_FILE = "workflows.json"

def load_workflows():
    if not os.path.exists(OUTPUT_FILE):
        return []
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

@app.get("/workflows")
def get_workflows(
    platform: Optional[str] = Query(None, description="Filter by platform (YouTube, Forum, Google)"),
    country: Optional[str] = Query(None, description="Filter by country (US, IN, etc.)"),
    sort_by: Optional[str] = Query(None, description="Sort by views, likes, comments, search_interest"),
    limit: Optional[int] = Query(10, description="Limit number of results")
):
    data = load_workflows()

    # Apply filters
    if platform:
        data = [d for d in data if d.get("platform", "").lower() == platform.lower()]
    if country:
        data = [d for d in data if d.get("country", "").lower() == country.lower()]

    # Apply sorting safely
    if sort_by:
        if sort_by in ["views", "likes", "comments", "search_interest"]:
            data = sorted(
                data,
                key=lambda x: (x.get("popularity_metrics") or {}).get(sort_by, 0) or 0,
                reverse=True
            )

    # Apply limit
    if limit:
        data = data[:limit]

    return data
