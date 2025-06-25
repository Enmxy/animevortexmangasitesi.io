# AnimeVortex Backend

## Özellikler
- Yorum sistemi (API üzerinden manga/bölüm yorumu ekle & listele)
- Basit admin paneli (yorum silme ve yönetim)
- SQLite veritabanı ile taşınabilirlik
- FastAPI ile hızlı, modern ve güvenli backend

## Kurulum
1. Gerekli paketleri yükleyin:

```
pip install -r requirements.txt
```

2. Sunucuyu başlatın:

```
uvicorn main:app --reload
```

3. Admin paneline erişim:
- [http://localhost:8000/admin](http://localhost:8000/admin)
- Kullanıcı adı: `admin`
- Şifre: `admin123`

## API Örnekleri
- Yorum ekle: `POST /api/comments/`
- Yorumları getir: `GET /api/comments/?manga_id=1&chapter_id=2`

## Klasör Yapısı
- `main.py`: FastAPI ana uygulama dosyası
- `models.py`: SQLAlchemy modelleri
- `schemas.py`: Pydantic şemaları
- `database.py`: Veritabanı bağlantısı
- `admin_panel.py`: Admin paneli router'ı
- `templates/`: Admin paneli için HTML şablonları
- `static/`: Statik dosyalar (varsa)
