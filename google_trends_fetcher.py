import os
import json
import time
from pytrends.request import TrendReq
from dotenv import load_dotenv

load_dotenv()  # load .env file

API_KEY = os.getenv("YOUTUBE_API_KEY")

OUTPUT_FILE = "google_trends_data.json"

def save_to_json(new_data):
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    if not isinstance(data, list):
        data = [data]

    data.extend(new_data)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def fetch_trends(keywords, geo="US", retries=3, delay=2):
    pytrends = TrendReq(hl="en-US", tz=360)
    for attempt in range(retries):
        try:
            pytrends.build_payload(keywords, cat=0, timeframe="today 12-m", geo=geo, gprop="")
            data = pytrends.interest_over_time()
            if not data.empty:
                return data
            else:
                return None
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Rate limited for {keywords} in {geo}, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2  # exponential backoff
            else:
                print(f"❌ Error fetching {keywords} for {geo}: {e}")
                return None
    print(f"❌ Failed after retries: {keywords} in {geo}")
    return None

if __name__ == "__main__":
    workflows = ["Google Sheets", "Slack", "Discord", "Airtable", "Notion"]
    countries = ["US", "IN"]
    all_data = []

    for wf in workflows:
        for country in countries:
            print(f"Fetching {wf} for {country}...")
            df = fetch_trends([f"n8n {wf}"], geo=country)
            if df is not None:
                record = {
                    "workflow": f"n8n {wf}",
                    "platform": "Google Trends",
                    "popularity_metrics": {"search_interest": df.iloc[:, 0].mean()},
                    "country": country,
                }
                all_data.append(record)
                print(f"✅ Saved trend for {wf} in {country}")
            else:
                print(f"❌ Skipped {wf} in {country}")

    save_to_json(all_data)
    print(f"🎯 Finished. Added {len(all_data)} records.")
