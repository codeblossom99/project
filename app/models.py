from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime, timedelta
from typing import Optional

class URLBase(BaseModel):
    original_url: str
    
    @validator('original_url')
    def validate_url(cls, v):
        # 去驗證 URL 
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        if len(v) > 2048:
            raise ValueError('URL is too long (max 2048 characters)')
        return v

class URLResponse(BaseModel):
    short_url: str
    expiration_date: datetime
    success: bool
    reason: Optional[str] = None
    
    class Config:
        orm_mode = True