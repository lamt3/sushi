import logging
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any, Optional, List

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class UtmParams(BaseModel):
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    fbclid: Optional[str] = None
    gclid: Optional[str] = None
    ttclid: Optional[str] = None

class PixelEventData(BaseModel):
    event: str
    timestamp: str
    # shopDomain: str
    # utmParams: Optional[UtmParams] = None
    data: Dict[str, Any]

class PixelHandler:
     
    async def process_event(self, event_data: PixelEventData):
        try:
            print("PROCESSING EVENT...")
            print(event_data)
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Error processing pixel event: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing event data")