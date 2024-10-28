<?php
	$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
?>

<html>
	<body>
		<?php
			$id_pelicula = $_POST['pelicula_id'];
			$comentario = $_POST['new_comment'];

			$query = "INSERT INTO tComentarios(comentario, usuario_id, pelicula_id) VALUES ('".$comentario."',NULL,".$id_pelicula.")";

			mysqli_query($db, $query) or die('Error');

			echo "<p>Nuevo comentario ";
			echo mysqli_insert_id($db);
			echo " añadido</p>";

			echo "<a href='/detail.php?pelicula_id=".$id_pelicula."'>Volver</a>";
			mysqli_close($db);
		?>
	</body>
</html>