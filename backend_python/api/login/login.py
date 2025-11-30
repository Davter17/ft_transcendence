# Equivalente a login.php
from ..conexion.conexion import get_connection

def validate_user(json_data: dict):
	"""
	Validate the user
	"""
	conexion = get_connection()
	if not conexion:
		return {
			"success": False,
			"error": "Error de conexión a la base de datos",
			"message": "No se pudo conectar a la base de datos"
		}
	
	if "User" in json_data and "Password" in json_data:
		cursor = conexion.cursor(dictionary=True)
		query = "SELECT id, username, password FROM users WHERE username = %s"
		cursor.execute(query, (json_data['User'],))
		user = cursor.fetchone()
		
		if user:
			if json_data['Password'] == user['password']:
				conexion.close()
				return {
					"success": True,
					"message": "Login exitoso",
					"user_id": user['id'],
					"username": user['username']
				}
		
		conexion.close()
		return {
			"success": False,
			"error": "Credenciales incorrectas",
			"message": "Usuario o contraseña inválidos"
		}
	
	return {
		"success": False,
		"error": "Credenciales incorrectas", 
		"message": "Usuario o contraseña inexistentes"
	}