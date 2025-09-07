# config.py

# --- API Keys ---
# IMPORTANT: Fill these in with your actual API keys.
# To get a YouTube API key, visit the Google Cloud Console: https://console.cloud.google.com/
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

# --- Service URLs ---
# The base URL for the n8n community forum (which runs on Discourse)
N8N_DISCOURSE_URL = "https://community.n8n.io"

# --- Data Fetching Parameters ---

# General search keywords to find n8n content.
# These are used across YouTube and Discourse.
BASE_SEARCH_KEYWORDS = [
    "n8n workflow",
    "n8n automation",
    "n8n tutorial",
    "n8n guide",
]

# Keywords for specific integrations/use-cases.
# This list is used by the Google Trends fetcher and to broaden other searches.
# A more comprehensive list will yield more results.
INTEGRATION_KEYWORDS = [
    "n8n Google Sheets", "n8n Slack", "n8n Discord", "n8n Airtable",
    "n8n Notion", "n8n OpenAI", "n8n Gmail", "n8n HubSpot", "n8n Telegram",
    "n8n Typeform", "n8n Webhook", "n8n RSS", "n8n Cron", "n8n Shopify",
    "n8n Stripe", "n8n MySQL", "n8n Postgres", "n8n Microsoft Teams",
    "n8n Google Drive", "n8n Trello"
]

# Countries to analyze. Using ISO 3166-1 alpha-2 codes.
# US = United States, IN = India
TARGET_COUNTRIES = ["US", "IN"]

# The maximum number of results to fetch from each platform's search.
# Higher numbers will take longer to process.
MAX_RESULTS_PER_QUERY = 50

# --- File Paths ---
# The name of the file used as a simple database to store workflow data.
DB_FILE_PATH = "workflows.json"