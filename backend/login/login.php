<?php
header('Content-Type: application/json; charset=utf-8');
require_once '../conexion/conexion.php';

function validateUser($json)
{
	global $conexion;

	if ($_SERVER['REQUEST_METHOD'] !== 'POST')
	{
		http_response_code(405);
		return json_encode([
			"success" => false,
			"error" => "Método no permitido, usa GET"
		]);
	}
	$data = json_decode($json, true);
	if (isset($data['User']) && isset($data['Password']))
	{
		$stmt = $conexion->prepare("SELECT id, username, password FROM users WHERE username = ?");
		$stmt->bind_param("s", $data['User']);
		$stmt->execute();
		$result = $stmt->get_result();
		$user = $result->fetch_assoc();
		if ($user && password_verify($data['Password'], $user['password']))
		{
			return json_encode([
				"success" => true,
				"message" => "Login exitoso",
				"user_id" => $user['id'],
				"username" => $user['username']
			]);
		}
		else
		{
			http_response_code(401);
			return json_encode([
				"success" => false,
				"error" => "Credenciales incorrectas",
				"message" => "Usuario o contraseña inválidos"
			]);
		}
	}
	return json_encode([
		"success" => false,
		"error" => "Credenciales incorrectas",
		"message" => "Usuario o contraseña inexistentes"
	]);
}

// Código principal - llamar la función
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$jsonInput = file_get_contents('php://input');
	$response = validateUser($jsonInput);
	echo $response;
} else {
	http_response_code(405);
	echo json_encode(["error" => "Solo se permiten peticiones POST"]);
}

?>