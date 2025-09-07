# SpeakGenie Assignment – Workflow Popularity Tracker

## Features
- Fetches most popular n8n workflows from YouTube, Google Trends, and Forums
- Stores results in JSON
- Serves API with FastAPI
- Automated with cron/scheduler

## Setup
1. Install deps:
   pip install -r requirements.txt

2. Run API:
   uvicorn app:app --reload

3. Run scheduler (auto-refresh data):
   python scheduler.py

## API Endpoint
GET http://127.0.0.1:8000/workflows
