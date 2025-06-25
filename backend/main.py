from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
import admin_panel
from database import engine, SessionLocal
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AnimeVortex API & Admin Panel")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Yorum ekle
from fastapi import Request

@app.post("/api/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, request: Request, db: Session = Depends(get_db)):
    # IP ban kontrolü
    client_ip = request.client.host
    if db.query(models.IPBan).filter(models.IPBan.ip == client_ip).first():
        raise HTTPException(status_code=403, detail="IP adresiniz banlandı.")
    # Yıldız zorunlu kontrolü
    if not (1 <= comment.rating <= 5):
        raise HTTPException(status_code=400, detail="Yıldız (rating) 1-5 arası olmalı.")
    db_comment = models.Comment(
        manga_id=comment.manga_id,
        chapter_id=comment.chapter_id,
        user=comment.user,
        content=comment.content,
        rating=comment.rating,
        ip=client_ip
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Manga veya bölüme ait yorumları getir
@app.get("/api/comments/", response_model=List[schemas.Comment])
def get_comments(manga_id: int, chapter_id: int = None, db: Session = Depends(get_db)):
    q = db.query(models.Comment).filter(models.Comment.manga_id == manga_id)
    if chapter_id:
        q = q.filter(models.Comment.chapter_id == chapter_id)
    return q.order_by(models.Comment.created_at.desc()).all()

@app.get("/api/check_ban/")
def check_ban(request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host
    if db.query(models.IPBan).filter(models.IPBan.ip == client_ip).first():
        return {"banned": True}
    return {"banned": False}

# Admin panel router
app.include_router(admin_panel.router)

@app.get("/", response_class=HTMLResponse)
def root():
    return "<h2>AnimeVortex Backend Çalışıyor!</h2>"
