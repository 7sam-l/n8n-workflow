import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # load .env file

API_KEY = os.getenv("YOUTUBE_API_KEY")


# Simulated forum data (replace this with actual scraping later)
def fetch_forum_workflows():
    return [
        {
            "workflow": "n8n Discord Bot",
            "platform": "Forum",
            "popularity_metrics": {
                "views": None,
                "likes": None,
                "comments": 30,
                "replies": 100,
                "contributors": 12,
                "search_interest": None,
                "like_to_view_ratio": None,
                "comment_to_view_ratio": None
            },
            "country": "IN",
            "source_url": "https://community.n8n.io/example-thread",
            "fetched_at": datetime.utcnow().isoformat()
        }
    ]

import os
import json

def save_to_json(new_data, filename="workflows.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, dict):  # 🔥 ensure dict structure
                    data = {"youtube": [], "google": [], "forum": []}
            except json.JSONDecodeError:
                data = {"youtube": [], "google": [], "forum": []}
    else:
        data = {"youtube": [], "google": [], "forum": []}

    if not isinstance(new_data, list):  # 🔥 wrap dict into list
        new_data = [new_data]

    # 🔥 Make sure "forum" key exists
    if "forum" not in data:
        data["forum"] = []

    data["forum"].extend(new_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(new_data)} forum workflows, total now {len(data['forum'])}")


if __name__ == "__main__":
    forum_data = fetch_forum_workflows()
    save_to_json(forum_data)
