# models.py
from pydantic import BaseModel, Field
from typing import Dict, Union, Optional, Literal

class PopularityMetrics(BaseModel):
    """
    A flexible model for popularity metrics from different platforms.
    Fields are optional to accommodate various data sources.
    """
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    replies: Optional[int] = None
    contributors: Optional[int] = None
    search_interest: Optional[int] = None # For Google Trends (0-100 scale)
    
    # Ratios for engagement calculation
    like_to_view_ratio: Optional[float] = None
    comment_to_view_ratio: Optional[float] = None

class Workflow(BaseModel):
    """
    Defines the structure for a single workflow entry.
    """
    workflow: str = Field(..., description="The name or keyword of the workflow.")
    platform: Literal["YouTube", "Forum", "Google"] = Field(..., description="The source platform.")
    popularity_metrics: PopularityMetrics = Field(..., description="A dictionary of popularity metrics.")
    country: Literal["US", "IN"] = Field(..., description="The country for which the data is relevant.")
    source_url: Optional[str] = Field(None, description="Direct URL to the source video or post.")

class WorkflowDB(BaseModel):
    """
    Represents the structure of the entire database stored in the JSON file.
    """
    youtube: list[Workflow] = []
    forum: list[Workflow] = []
    google: list[Workflow] = []