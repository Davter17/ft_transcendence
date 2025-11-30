# Equivalente a conexion.php
import mysql.connector

# Configuración de la base de datos
DB_CONFIG = {
	"host": "localhost",
	"user": "root",
	"password": "",
	"database": "test"
}

def get_connection():
	"""
	Crear la conexion esta en mySQL y no en SQLite por lo que cuidao
	"""
	try:
		conexion = mysql.connector.connect(**DB_CONFIG)
		return conexion
	except mysql.connector.Error as err:
		print(f"Failure conexion: {err.errno}")
		return None