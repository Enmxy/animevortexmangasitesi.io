from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Comment, User
from schemas import Comment as CommentSchema
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

# Basit admin kontrolü (geliştirilebilir)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = pwd_context.hash("admin123")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or not pwd_context.verify(credentials.password, ADMIN_PASSWORD):
        return HTMLResponse("<h2>Yetkisiz</h2>", status_code=401)
    return templates.TemplateResponse("admin_panel.html", {"request": request})

# Yorumları listele
@router.get("/admin/comments", response_class=HTMLResponse)
def admin_comments(request: Request, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or not pwd_context.verify(credentials.password, ADMIN_PASSWORD):
        return HTMLResponse("<h2>Yetkisiz</h2>", status_code=401)
    comments = db.query(Comment).order_by(Comment.created_at.desc()).all()
    return templates.TemplateResponse("admin_comments.html", {"request": request, "comments": comments})

@router.post("/admin/comments/ban_ip/{ip}")
def ban_ip(ip: str, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or not pwd_context.verify(credentials.password, ADMIN_PASSWORD):
        return HTMLResponse("<h2>Yetkisiz</h2>", status_code=401)
    from models import IPBan
    if not db.query(IPBan).filter(IPBan.ip == ip).first():
        db.add(IPBan(ip=ip))
        db.commit()
    return RedirectResponse(url="/admin/comments", status_code=HTTP_303_SEE_OTHER)

@router.post("/admin/comments/unban_ip/{ip}")
def unban_ip(ip: str, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or not pwd_context.verify(credentials.password, ADMIN_PASSWORD):
        return HTMLResponse("<h2>Yetkisiz</h2>", status_code=401)
    from models import IPBan
    ban = db.query(IPBan).filter(IPBan.ip == ip).first()
    if ban:
        db.delete(ban)
        db.commit()
    return RedirectResponse(url="/admin/comments", status_code=HTTP_303_SEE_OTHER)

# Yorum sil
@router.post("/admin/comments/delete/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or not pwd_context.verify(credentials.password, ADMIN_PASSWORD):
        return HTMLResponse("<h2>Yetkisiz</h2>", status_code=401)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return RedirectResponse(url="/admin/comments", status_code=HTTP_303_SEE_OTHER)
