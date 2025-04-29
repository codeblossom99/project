from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import datetime

from .database import get_db, URL, create_tables
from .models import URLBase, URLResponse
from .utils import generate_short_code, get_expiration_date, is_valid_url

app = FastAPI(title="URL Shortener API")

@app.on_event("startup")
async def startup():
    create_tables()

@app.post("/api/shorten", response_model=URLResponse)
async def create_short_url(url_data: URLBase, db: Session = Depends(get_db)):
    if not is_valid_url(url_data.original_url):
        return URLResponse(
            short_url="",
            expiration_date=datetime.datetime.utcnow(),
            success=False,
            reason="Invalid URL format or URL too long"
        )
    
    short_code = generate_short_code()
    expiration_date = get_expiration_date()
    
    db_url = URL(
        original_url=url_data.original_url,
        short_code=short_code,
        expiration_date=expiration_date
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    # 組合短網址
    short_url = f"{request.base_url}r/{short_code}"
    
    return URLResponse(
        short_url=short_url,
        expiration_date=expiration_date,
        success=True
    )

@app.get("/r/{short_code}")
async def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if db_url.expiration_date < datetime.datetime.utcnow():
        raise HTTPException(status_code=410, detail="URL has expired")
    
    return RedirectResponse(url=db_url.original_url)

@app.get("/")
async def root():
    return {"message": "Hello World"}