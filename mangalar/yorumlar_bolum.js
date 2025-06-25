// AnimeVortex - Yorumlar Bölümü Scripti
// Her manga/chapter sayfasında kullanılabilir şekilde tasarlanmıştır

// DİKKAT: mangaId ve chapterId dinamik olarak backend'den veya sayfa datasından alınmalıdır!
let mangaId = window.mangaId;
let chapterId = window.chapterId;
console.log('DEBUG - mangaId:', mangaId, 'chapterId:', chapterId);

async function fetchComments() {
    const res = await fetch(`/api/comments/?manga_id=${mangaId}&chapter_id=${chapterId}`);
    const data = await res.json();
    let html = '';
    if (data.length === 0) html = '<p>Henüz yorum yok.</p>';
    else html = '<ul style="padding:0;list-style:none;">' + data.map(y => `<li style='margin-bottom:1.2rem;background:#181818;padding:1rem 1.5rem;border-radius:10px;'><b>${y.user}</b> <span style='color:#e50914;'>${y.rating} ⭐</span> <br>${y.content}<br><small>${new Date(y.created_at).toLocaleString()}</small></li>`).join('') + '</ul>';
    document.getElementById('yorumListesi').innerHTML = html;
}

async function checkBan() {
    const res = await fetch('/api/check_ban/');
    const data = await res.json();
    if (data.banned) {
        document.getElementById('yorumForm').style.display = 'none';
        document.getElementById('yorumListesi').innerHTML = '<span style="color:#e50914;font-weight:bold;">IP adresiniz banlandı, yorum yapamazsınız ve yorumları göremezsiniz.</span>';
    } else {
        document.getElementById('yorumForm').style.display = 'block';
        fetchComments();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    checkBan();
    document.getElementById('yorumForm').onsubmit = async e => {
        e.preventDefault();
        const user = document.getElementById('yorumKullanici').value.trim();
        const rating = parseInt(document.getElementById('yorumYildiz').value);
        const content = document.getElementById('yorumIcerik').value.trim();
        if (!user || !rating || !content) {
            document.getElementById('yorumHata').innerText = 'Tüm alanları doldurun ve yıldız seçin!';
            return;
        }
        if (
            mangaId === undefined ||
            mangaId === null ||
            mangaId === '' ||
            mangaId === 0 ||
            mangaId === 'null' ||
            mangaId === 'undefined'
        ) {
            document.getElementById('yorumHata').innerText = 'Sayfa için mangaId tanımlı değil!';
            return;
        }
        try {
            const res = await fetch('/api/comments/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user, rating, content, manga_id: window.mangaId, chapter_id: window.chapterId })
            });
            if (!res.ok) {
                const err = await res.json();
                document.getElementById('yorumHata').innerText = err.detail || 'Yorum gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.';
            } else {
                document.getElementById('yorumForm').reset();
                document.getElementById('yorumHata').innerText = '';
                fetchComments();
            }
        } catch {
            document.getElementById('yorumHata').innerText = 'Sunucu hatası!';
        }
    };
});
