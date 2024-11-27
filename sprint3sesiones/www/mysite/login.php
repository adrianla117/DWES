<?php
$servername = '172.16.0.2';
$username = '';
$password = '';
$dbname = 'mysitedb.sql';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error){
    die("Conexión fallida: " . $conn->connect_error);
}

$email = trim($_POST['email']);
$password = trim($_POST['password']);

$stmt = $conn->prepare("SELECT password FROM usuarios WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows == 0) {
    die("El correo electrónico no está registrado.");
}

$stmt->bind_result($password_hash);
$stmt->fetch();

if (password_verify($password, $password_hash)) {
    session_start();
    $_SESSION['user'] = $email;
    header("Location: main.php");
    exit();
} else {
    echo "Contraseña incorrecta.";
}

$stmt->close();
$conn->close();
?>