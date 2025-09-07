# youtube_fetcher.py
import requests
import config
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()  # load .env file

API_KEY = os.getenv("YOUTUBE_API_KEY")

OUTPUT_FILE = "workflows.json"

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
WORKFLOWS_FILE = "workflows.json"


def fetch_youtube_workflows(query: str, max_results: int = 10, country: str = "US"):
    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "regionCode": country,
        "key": config.YOUTUBE_API_KEY,
    }

    search_resp = requests.get(YOUTUBE_API_URL, params=search_params)
    search_data = search_resp.json()

    video_ids = [item["id"]["videoId"] for item in search_data.get("items", [])]

    if not video_ids:
        return []

    stats_params = {
        "part": "statistics,snippet",
        "id": ",".join(video_ids),
        "key": config.YOUTUBE_API_KEY,
    }

    stats_resp = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
    stats_data = stats_resp.json()

    workflows = []
    for item in stats_data.get("items", []):
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})

        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0)) if "likeCount" in stats else None
        comments = int(stats.get("commentCount", 0)) if "commentCount" in stats else None

        workflow_entry = {
            "workflow": snippet.get("title"),
            "platform": "YouTube",
            "popularity_metrics": {
                "views": views,
                "likes": likes,
                "comments": comments,
                "like_to_view_ratio": (likes / views) if views and likes else None,
                "comment_to_view_ratio": (comments / views) if views and comments else None,
            },
            "country": country,
            "source_url": f"https://www.youtube.com/watch?v={item['id']}",
        }

        workflows.append(workflow_entry)

    return workflows


def save_to_json(new_data):
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Ensure the youtube key exists
    if "youtube" not in data:
        data["youtube"] = []

    # Avoid duplicates by source_url
    existing_urls = {wf.get("source_url") for wf in data["youtube"]}
    fresh_data = [wf for wf in new_data if wf.get("source_url") not in existing_urls]

    data["youtube"].extend(fresh_data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(fresh_data)} YouTube workflows, total now {len(data['youtube'])}")


if __name__ == "__main__":
    data = fetch_youtube_workflows("n8n Google Sheets", max_results=5, country="US")
    save_to_json(data)
