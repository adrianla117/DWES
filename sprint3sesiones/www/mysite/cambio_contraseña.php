<?php
session_start();
require_once 'main.php'

if (!isset($_SESSION['user'])) {
    echo "Debes estar logueado para cambiar tu contraseña";
    exit;
}

$user_id = $_SESSION['user'];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $current_password = $_POST['password'];
    $new_password = $_POST['new_password'];
    $confirm_new_password = $_POST['confirm_new_password'];

    if (empty($password) || empty($new_password) || empty($confirm_new_password)) {
        echo "Todos los campos son requeridos";
        exit;
    }

    if ($new_password !== $confirm_new_password) {
        echo "Las contraseñas no coinciden";
        exit;
    }

    $query = "SELECT * FROM usuarios WHERE id = ?";
    $stmt = $db->prepare($query);
    $stmt->execute([$user_id]);

    $user = $stmt->fetch();

    if (!$user) {
        echo "Usuario no encontrado";
        exit;
    }

    if (!password_verify($current_password, $user['password'])) {
        echo "La contraseña actual es incorrecta";
        exit;
    }

    $hashed_new_password = password_hash($new_password, PASSWORD_DEFAULT);

    $query = "UPADTE usuarios SET password = ? WHERE id = ?";
    $stmt = $db->prepare($query);
    $stmt->execute([$hashed_new_password, $user_id]);

    echo "Contraseña cambiada correctamente";
}
?>