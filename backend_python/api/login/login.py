from ..conexion.conexion import get_connection
import bcrypt
from typing import Union


class BaseResponse(BaseModel):
	success: bool
	message: str

class ResponseCorrect(BaseResponse):
	user_id: int
	username: str

class ResponseWrong(BaseResponse):
	error: str


class UserResponse(BaseModel):
	id: int
	username: str
	password: str


def validate_user(user_data: UserResponse) -> BaseResponse:
	"""
	Validate the user
	"""
	conexion = get_connection()
	if not conexion:
		return ResponseWrong(
			success=False,
			error="Error de conexión a la base de datos",
			message="No se pudo conectar a la base de datos"
		)
	
	try:
		if user_data.username and user_data.password:
			cursor = conexion.cursor(dictionary=True)
			query = "SELECT id, username, password FROM users WHERE username = %s"
			cursor.execute(query, (user_data.username,))
			db_user = cursor.fetchone()
			
			if db_user:
				if bcrypt.checkpw(user_data.password.encode('utf-8'), 
								db_user['password'].encode('utf-8')):
					return ResponseCorrect(
						success=True,
						message="Login exitoso",
						user_id=db_user['id'],
						username=db_user['username']
					)
			
			return ResponseWrong(
				success=False,
				error="Credenciales incorrectas",
				message="Usuario o contraseña inválidos"
			)
		
		return ResponseWrong(
			success=False,
			error="Credenciales faltantes", 
			message="Usuario o contraseña requeridos"
		)
		
	except Exception as e:
		return ResponseWrong(
			success=False,
			error="Error interno",
			message=str(e)
		)
	finally:
		conexion.close()