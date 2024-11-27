<?php
	session_start();

	$db = mysqli_connect('172.16.0.2', 'root', '1234', 'mysitedb') or die('Fail');

	$id_pelicula = $_POST['pelicula_id'];
	$comentario = $_POST['new_comment'];

	$usuario_id = 'NULL';

	if (isset($_SESSION['USER'])) {
		$email = $_SESSION['user'];

		$query_user = "SELECT id FROM usuarios WHERE email = '$email'";
		$result_user = mysqli_query($db, $query_user);

		if ($result_user && mysqli_num_rows($result_user) > 0) {
			$row = mysqli_fetch_assoc($result_user);
			$usuario_id = $row['id'];
		}
	}

	$query = "INSERT INTO tComentarios (comentario, usuario_id, pelicula_id) VALUES ('$comentario', $usuario_id, $id_pelicula)";
	mysqli_query($db, $query) or die('Error al insertar comentario');

	echo "<p>Nuevo comentario ";
	echo mysqli_insert_id($db);
	echo " añadido</p>";

	echo "<a href='/detail.php?pelicula_id=".$id_pelicula."'>Volver</a>";

	mysqli_close($db);
?>