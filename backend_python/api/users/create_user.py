from ..conexion.conexion import get_connection
import bcrypt
import re
from pydantic import BaseModel, field_validator
from typing import Optional

class UserCreate(BaseModel):
	email: str
	username: str
	password: str

	@field_validator('email')
	def validate_email(cls, v):
		regex = r'^[a-zA-Z0-9.%-]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,}$'
		if not re.match(regex, v):
			raise ValueError('Formato de email inválido')
		return v
	
	# Validador de contraseña
	@field_validator('password')
	def validate_password(cls, v):
		if len(v) < 6:
			raise ValueError('La contraseña debe tener al menos 6 caracteres')
		return v

class UserResponse(BaseModel):
	success: bool
	message: str
	username: Optional[str] = None
	error: Optional[str] = None

def create_user(user_data: UserCreate) -> UserResponse:
	"""
	Crea un usuario usando el modelo UserCreate
	"""
	conexion = get_connection()
	
	if not conexion:
		return UserResponse(
			success=False,
			error="Error de conexión a la base de datos",
			message="No se pudo conectar a la base de datos"
		)
	
	try:
		cursor = conexion.cursor(dictionary=True)
		query = "SELECT email, username FROM users WHERE email=%s OR username=%s"
		cursor.execute(query, (user_data.email, user_data.username))
		existing_user = cursor.fetchone()
		
		if existing_user:
			if existing_user['email'] == user_data.email and existing_user['username'] == user_data.username:
				message = "Usuario y correo ya registrados"
			elif existing_user['username'] == user_data.username:
				message = "Usuario ya registrado"
			else:
				message = "Correo ya registrado"
				
			return UserResponse(success=False, message=message)
		
		password_bytes = user_data.password.encode('utf-8')
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw(password_bytes, salt)
		
		insert_query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
		cursor.execute(insert_query, (
			user_data.email, 
			user_data.username, 
			hashed_password.decode('utf-8')
		))
		conexion.commit()
		
		return UserResponse(
			success=True,
			message="Usuario creado exitosamente",
			username=user_data.username
		)
		
	except Exception as e:
		return UserResponse(
			success=False,
			error="Error interno",
			message=str(e)
		)
	finally:
		conexion.close()