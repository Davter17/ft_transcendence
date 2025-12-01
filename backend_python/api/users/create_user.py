from ..conexion.conexion import get_connection
import bcrypt
import re


def isValidUser(user):
	regex = r'^[a-zA-Z0-9.%-]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,}$'

	if re.match(regex, user):
		return True
	return False

def create_user(json_data: dict):

	conexion = get_connection()

	if not conexion:
		return {
			"success": False,
			"error": "Error de conexión a la base de datos",
			"message": "No se pudo conectar a la base de datos"
		}
	
	if "User" in json_data and "Password" in json_data:
		if isValidUser(json_data["User"]):
			cursor = conexion.cursor(dictionary=True)
			password_bytes = json_data['Password'].encode('utf-8')
			salt = bcrypt.gensalt()
			hashed_password = bcrypt.hashpw(password_bytes, salt)
			query = "INSERT INTO users (username, password) VALUES (%s, %s)"
			cursor.execute(query, (json_data['User'], hashed_password.decode('utf-8')))
			conexion.commit()
			conexion.close()

			return {
				"success": True,
				"message": "Usuario creado exitosamente",
				"username": json_data['User']
			}

	return {
		"success": False,
		"message": "Usuario o contraseña incorrecta"
	}