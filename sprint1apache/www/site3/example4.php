<html>
<body>
<h1>Jubilación</h1>
<?php
	$v_edadx = $_GET["edad_en_x"];
        if ($_GET["edad"]+$v_edadx > 65) {
                echo "En ".$v_edadx." años tendras edad de jubilación";
        } else {
                echo "¡Disfruta de tu tiempo!";
        }
?>
</body>
</html>
