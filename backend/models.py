from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Integer, default=0)  # 1: admin, 0: normal user

class Manga(Base):
    __tablename__ = "mangas"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    # Genişletilebilir

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    manga_id = Column(Integer, ForeignKey("mangas.id"))
    title = Column(String, nullable=False)
    manga = relationship("Manga", backref="chapters")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    manga_id = Column(Integer, ForeignKey("mangas.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)
    user = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)  # Yıldız
    ip = Column(String, nullable=False)       # IP adresi
    created_at = Column(DateTime, default=datetime.utcnow)
    manga = relationship("Manga", backref="comments")
    chapter = relationship("Chapter", backref="comments")

class IPBan(Base):
    __tablename__ = "ipbans"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, nullable=False)
    reason = Column(String, nullable=True)
    banned_at = Column(DateTime, default=datetime.utcnow)
