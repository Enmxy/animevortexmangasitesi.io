const express = require('express');
const fs = require('fs');
const path = require('path');
const bcrypt = require('bcryptjs');
const cors = require('cors');

const app = express();
const PORT = 3001;
const USERS_FILE = path.join(__dirname, 'users.json');

app.use(cors());
app.use(express.json());

// Yardımcı: Kullanıcıları oku/yaz
function readUsers() {
    if (!fs.existsSync(USERS_FILE)) return {};
    return JSON.parse(fs.readFileSync(USERS_FILE, 'utf8'));
}
function writeUsers(users) {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
}

// Kayıt
app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) return res.status(400).json({ success: false, message: 'Eksik bilgi!' });
    let users = readUsers();
    if (users[username]) return res.status(409).json({ success: false, message: 'Kullanıcı adı zaten var!' });
    const hash = await bcrypt.hash(password, 10);
    users[username] = { password: hash };
    writeUsers(users);
    res.json({ success: true, message: 'Kayıt başarılı!' });
});

// Giriş
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) return res.status(400).json({ success: false, message: 'Eksik bilgi!' });
    let users = readUsers();
    if (!users[username]) return res.status(401).json({ success: false, message: 'Kullanıcı bulunamadı!' });
    const valid = await bcrypt.compare(password, users[username].password);
    if (!valid) return res.status(401).json({ success: false, message: 'Şifre yanlış!' });
    res.json({ success: true, message: 'Giriş başarılı!', username });
});

app.get('/', (req, res) => {
    res.send('Anime Vortex Backend API çalışıyor!');
});

app.listen(PORT, () => {
    console.log(`Backend API çalışıyor: http://localhost:${PORT}`);
});
