from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
from api.login.login import validate_user
from api.users.create_user import create_email

app = FastAPI(title="Transcendence API", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
	return {"message": "Transcendence API - Migrado de PHP", "endpoints": ["/login"]}

@app.post("/login")
async def login(request: Request):
	"""
	To login the user
	"""
	try:
		json_input = await request.body()
		json_data = json.loads(json_input.decode('utf-8'))
		
		response = validate_user(json_data)
		
		if not response["success"]:
			return JSONResponse(
				status_code=401 if "Credenciales incorrectas" in response.get("error", "") else 400,
				content=response
			)
		
		return response
		
	except json.JSONDecodeError:
		return JSONResponse(
			status_code=400,
			content={
				"success": False,
				"error": "JSON inválido",
				"message": "El formato del JSON no es válido"
			}
		)
	except Exception as e:
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": "Error interno del servidor",
				"message": str(e)
			}
		)

@app.post("/register")
async def register(request: Request):
	"""
	To create de user in the app
	"""
	try:
		json_input = await request.body()
		json_data = json.loads(json_input.decode('utf-8'))
		
		response = create_email(json_data)
		
		if not response["success"]:
			return JSONResponse(
				status_code=400,
				content=response
			)
		
		return response
		
	except json.JSONDecodeError:
		return JSONResponse(
			status_code=400,
			content={
				"success": False,
				"error": "JSON inválido",
				"message": "El formato del JSON no es válido"
			}
		)
	except Exception as e:
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": "Error interno del servidor",
				"message": str(e)
			}
		)

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="127.0.0.1", port=8000)