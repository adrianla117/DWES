<html>
        <body>
                <h1>Calculadora</h1>
                <p>
                <?php
                        if (isset($_POST["calcular"])) {
                                $num1 = $_POST['num1'];
				$num2 = $_POST['num2'];
				$op = $_POST['op'];
				if (empty($num1) || empty($num2) || !is_numeric($num1) || !is_numeric($num2)) {
					echo "Introduce un número válido por favor";
				} else {
					switch($op) {
						case "+":
							$resultado = $num1 + $num2;
							break;
						case "-":
							$resultado = $num1 + $num2;
							break;
						case "*":
							$resultado = $num1 * $num2;
							break;
						case "/":
							$resultado = $num1 / $num2;
							break;
						default:
							echo "Operación imposible";
					}
				}
				echo "El resultado final de ".$num1." ".$op." ".$num2." es ".$resultado;
                        }
                ?>
                </p>
                <p>Realiza una nueva operación:</p>

                <form action="calculadora.php" method="post">
			<label for="num1">Introduce el primer número: </label>
			<input type="number" id="num1" name="num1" required><br>
			<label for="num2">Introduce el segundo número: </label>
			<input type="number" id="num2" name="num2" required><br>
			<label for="op">Escoge un operación: </label>
			
			<select id="op" name="op">
				<option value="+">+</option>
				<option value="-">-</option>
				<option value="*">*</option>
				<option value="/">/</option>
			</select><br>
                        <input type="submit" value="calcular">
                </form>
        </body>
</html>
