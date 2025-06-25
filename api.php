<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');
header('Access-Control-Allow-Methods: POST, OPTIONS');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$usersFile = __DIR__ . '/users.json';
if (!file_exists($usersFile)) file_put_contents($usersFile, '{}');
$users = json_decode(file_get_contents($usersFile), true);

$data = json_decode(file_get_contents('php://input'), true);
$action = $_GET['action'] ?? '';

if ($action === 'register') {
    $username = trim($data['username'] ?? '');
    $password = $data['password'] ?? '';
    if (!$username || !$password) {
        echo json_encode(['success' => false, 'message' => 'Eksik bilgi!']);
        exit();
    }
    if (isset($users[$username])) {
        echo json_encode(['success' => false, 'message' => 'Kullanıcı adı zaten var!']);
        exit();
    }
    $users[$username] = [ 'password' => password_hash($password, PASSWORD_DEFAULT) ];
    file_put_contents($usersFile, json_encode($users, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true, 'message' => 'Kayıt başarılı!']);
    exit();
}
if ($action === 'login') {
    $username = trim($data['username'] ?? '');
    $password = $data['password'] ?? '';
    if (!$username || !$password) {
        echo json_encode(['success' => false, 'message' => 'Eksik bilgi!']);
        exit();
    }
    if (!isset($users[$username]) || !password_verify($password, $users[$username]['password'])) {
        echo json_encode(['success' => false, 'message' => 'Kullanıcı adı veya şifre yanlış!']);
        exit();
    }
    echo json_encode(['success' => true, 'message' => 'Giriş başarılı!', 'username' => $username]);
    exit();
}
echo json_encode(['success' => false, 'message' => 'Geçersiz istek!']);
