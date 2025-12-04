from ..conexion.conexion import get_connection
import bcrypt
import re


def isValidEmail(email):
	regex = r'^[a-zA-Z0-9.%-]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,}$'

	if re.match(regex, email):
		return True
	return False

def create_email(json_data: dict):

	conexion = get_connection()

	if not conexion:
		return {
			"success": False,
			"error": "Error de conexión a la base de datos",
			"message": "No se pudo conectar a la base de datos"
		}

	""" Conexion to the database to check """
	cursorExistEmail = conexion.cursor(dictionary=True)
	query = "SELECT email, username FROM users WHERE email=%s OR username=%s"
	cursorExistEmail.execute(query, (json_data['email'], json_data['user']))
	result = cursorExistEmail.fetchone()

	if "email" in json_data and "Password" in json_data and not cursorExistEmail:
		if isValidEmail(json_data["email"]):
			cursor = conexion.cursor(dictionary=True)
			password_bytes = json_data['Password'].encode('utf-8')
			salt = bcrypt.gensalt()
			hashed_password = bcrypt.hashpw(password_bytes, salt)
			query = "INSERT INTO emails (email, username, password) VALUES (%s, %s)"
			cursor.execute(query, (json_data['email'], json_data['user'], hashed_password.decode('utf-8')))
			conexion.commit()
			conexion.close()

			return {
				"success": True,
				"message": "Usuario creado exitosamente",
				"emailname": json_data['email']
			}
		else:
			return {
			"success": False,
			"message": "Formato invalido"
			}
	elif cursorExistEmail:
		conexion.close()
		if (result['username'] == json_data['user'] and result['email'] == json_data['email']):
			return {
				"success": False,
				"message": "Usuario y correo ya registrado"
			}
		elif (result['username'] == json_data['user']):
			return {
				"success": False,
				"message": "Usuario ya registrado"
			}
		else:
			return {
				"success": False,
				"message": "Correo ya registrado"
			}
	return {
		"success": False,
		"message": "Usuario o contraseña incorrecta"
	}