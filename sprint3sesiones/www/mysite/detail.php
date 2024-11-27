<?php
	session_start();
	if (isset($_SESSION['user'])) {
		echo "<a href='logout.php'>Cerrar sesión</a>";
	}

	$db = mysqli_connect('172.16.0.2', 'root', '1234', 'mysitedb') or die('Fail');
?>
<html>
<body>
	<?php
		if (!isset($_GET['pelicula_id'])) {
			die('No se ha especificado una película');
		}
		$id_pelicula = $_GET['pelicula_id'];
		$query = 'SELECT * FROM tPeliculas WHERE id='.$id_pelicula;
		$result = mysqli_query($db, $query) or die('Query error');
		$only_row = mysqli_fetch_array($result);
		echo '<h1>'.$only_row['nombre'].'</h1>';
		echo '<h2>'.$only_row['url_imagen'].'</h2>';
		echo '<h3>'.$only_row['genero'].'</h3>';
		echo '<h4>'.$only_row['nota'].'</h4>';
		echo '<h5>'.$only_row['fecha'].'</h5>';
	?>
	<h3>Comentarios:</h3>
	<ul>
		<?php
			$query2 = 'SELECT * FROM tComentarios WHERE pelicula_id='.$id_pelicula;
			$result2 = mysqli_query($db, $query2) or die('Query error');
			while ($row = mysqli_fetch_array($result2)) {
				echo '<li>'.$row['comentario'].'</li>';
				echo '<li>'.$row['fecha'].'</li>';
			}
			mysqli_close($db);
		?>
	</ul>

	<p>Deja un nuevo comentario:</p>
	<form action="/comment.php" method="post">
		<textarea rows="4" cols="50" name="new_comment"></textarea><br>
		<input type="hidden" name="pelicula_id" value="<?php echo $id_pelicula; ?>">
		<input type="submit" value="Comentar">
	</form>
</body>
</html>
