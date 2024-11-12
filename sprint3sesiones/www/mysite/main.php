<?php
session_start();
if (isset($_SESSION['user'])) {
    echo "<a href='logout.php'>Cerrar sesión</a>";
}

$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb');
if (!$db) {
    error_log('Connection error: ' . mysqli_connect_error());
    echo "Error en la conexión a la base de datos.";
    exit;
}

$query = 'SELECT * FROM tPeliculas';
$result = mysqli_query($db, $query) or die('Error en la consulta');
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Listado de Películas</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        img {
            max-width: 150px;
            height: auto;
        }
    </style>
</head>
<body>
<h1>Listado de Películas</h1>
<table>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Imagen</th>
            <th>Género</th>
            <th>Nota</th>
        </tr>
    </thead>
    <tbody>
        <?php
        // Compruebo si hay resultados
        if (mysqli_num_rows($result) > 0) {
            // Recorro los resultados
            while ($row = mysqli_fetch_array($result)) {
                $id = $row['id'];
                $nombre = $row['nombre'];
                $url_imagen = $row['url_imagen'];
                $genero = $row['genero'];
                $nota = $row['nota'];
                ?>
                <tr>
                    <td><a href="/detail.php?id=<?php echo $id; ?>"><?php echo $id; ?></a></td>
                    <td><?php echo $nombre; ?></td>
                    <td><img src="<?php echo $url_imagen; ?>" alt="Imagen de <?php echo $nombre; ?>"></td>
                    <td><?php echo $genero; ?></td>
                    <td><?php echo $nota; ?></td>
                </tr>
                <?php
            }
        } else {
            echo "<tr><td colspan='5'>No se encontraron resultados.</td></tr>";
        }
        ?>
    </tbody>
</table>
</body>
</html>
<?php
	mysqli_close($db);
?>