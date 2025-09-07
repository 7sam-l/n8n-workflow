import json
import os

# Input files from each fetcher
FILES = [
    "youtube_workflows.json",
    "google_workflows.json",
    "forum_workflows.json"
]

OUTPUT_FILE = "all_workflows.json"

def merge_json():
    merged = []
    seen_urls = set()

    for file in FILES:
        if not os.path.exists(file):
            print(f"⚠️ Skipping missing file: {file}")
            continue

        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):  # normalize single dict
                    data = [data]
            except json.JSONDecodeError:
                print(f"❌ Error reading {file}")
                continue

        for wf in data:
            url = wf.get("source_url")
            if url and url in seen_urls:
                continue
            seen_urls.add(url)
            merged.append(wf)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"✅ Merged {len(merged)} workflows into {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_json()
