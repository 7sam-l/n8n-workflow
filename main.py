# main.py
import json
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, Literal
import os

import config
from models import Workflow

print(">>> Running this main.py")

app = FastAPI(
    title="n8n Workflow Popularity API",
    description="Provides data on popular n8n workflows from YouTube, Discourse, and Google Trends.",
    version="1.0.0"
)


# =====================
# Database Loader
# =====================
def load_db() -> list[Workflow]:
    try:
        with open(config.DB_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_workflows = []

            if isinstance(data, dict):  # structured db
                for platform_list in data.values():
                    all_workflows.extend([Workflow(**wf) for wf in platform_list])
            elif isinstance(data, list):  # plain list
                all_workflows = [Workflow(**wf) for wf in data]

            return all_workflows
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading database: {e}")
        return []



# =====================
# API Routes
# =====================
@app.get("/workflows", response_model=list[Workflow])
def get_workflows(
    platform: Optional[Literal["YouTube", "Forum", "Google"]] = Query(None, description="Filter by source platform."),
    country: Optional[Literal["US", "IN"]] = Query(None, description="Filter by country (US or IN)."),
    skip: int = Query(0, ge=0, description="Number of results to skip for pagination."),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return (1–100).")
):
    """
    Retrieve a list of popular n8n workflows.
    
    You can filter by `platform`, `country`, and paginate results.
    """
    workflows = load_db()
    
    if not workflows:
        raise HTTPException(
            status_code=503, 
            detail="Workflow database is not yet available. Please run the scheduler first."
        )

    filtered_workflows = workflows
    
    if platform:
        filtered_workflows = [wf for wf in filtered_workflows if wf.platform == platform]
        
    if country:
        filtered_workflows = [wf for wf in filtered_workflows if wf.country == country]

    # Sort: workflows with more non-null metrics come first
    filtered_workflows.sort(
        key=lambda wf: sum(1 for v in wf.popularity_metrics.dict().values() if v is not None),
        reverse=True
    )

    return filtered_workflows[skip: skip + limit]


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify API and database status.
    """
    db_exists = os.path.exists(config.DB_FILE_PATH)
    workflows = load_db() if db_exists else []
    return {
        "status": "ok",
        "database_file": config.DB_FILE_PATH,
        "database_exists": db_exists,
        "workflows_loaded": len(workflows),
    }


@app.get("/")
def read_root():
    """
    Root endpoint with a welcome message and link to the documentation.
    """
    return {
        "message": "Welcome to the n8n Workflow Popularity API.",
        "docs_url": "/docs"
    }
