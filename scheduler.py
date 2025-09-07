# scheduler.py
import schedule
import time
import subprocess
from datetime import datetime

def run_fetchers():
    print(f"🚀 Running fetchers at {datetime.now().isoformat()}")
    subprocess.run(["python", "forum_fetcher.py"])
    subprocess.run(["python", "google_trends_fetcher.py"])
    subprocess.run(["python", "youtube_fetcher.py"])
    print(f"✅ Completed at {datetime.now().isoformat()}\n")

# Run every 6 hours
schedule.every(6).hours.do(run_fetchers)

print("📅 Scheduler started, running fetchers every 6 hours...")
run_fetchers()  # Run once at start

while True:
    schedule.run_pending()
    time.sleep(60)
