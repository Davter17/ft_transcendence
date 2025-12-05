from fastapi import status, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import datetime
import traceback

requestCount = {}

class ErrorResponse(BaseModel):
	success: bool
	ip: str
	port: int
	error: str
	message: str
	details: str
	timestamp: str

class TooManyRequestsException(Exception):
	pass


async def httpErrorHandler(request: Request, call_next) -> Response | JSONResponse:
	try:
		ip = request.client.host
		requestCount[ip] = requestCount.get(ip, 0) + 1
		if requestCount[ip] >= 500:
			raise TooManyRequestsException("Demasiadas solicitudes desde esta IP")
		return await call_next(request)
	except HTTPException as exc:
		error = ErrorResponse(
			success=False,
			ip=request.client.host,
			port=request.client.port,
			error=str(exc.status_code),
			message=exc.detail if exc.detail else "HTTP error",
			details="",
			timestamp=datetime.datetime.utcnow().isoformat(),
		)
		return JSONResponse(status_code=exc.status_code, content=error.model_dump())
	except ValueError as exc:
		error = ErrorResponse(
			success=False,
			ip=request.client.host,
			port=request.client.port,
			error="ValueError",
			message=str(exc),
			details="",
			timestamp=datetime.datetime.utcnow().isoformat(),
		)
		return JSONResponse(status_code=400, content=error.model_dump())
	except PermissionError as exc:
		error = ErrorResponse(
			success=False,
			ip=request.client.host,
			port=request.client.port,
			error="PermissionError",
			message=str(exc),
			details="",
			timestamp=datetime.datetime.utcnow().isoformat(),
		)
		return JSONResponse(status_code=403, content=error.model_dump())
	except TooManyRequestsException as exc:
		error = ErrorResponse(
			success=False,
			ip=request.client.host,
			port=request.client.port,
			error="TooManyRequests",
			message=str(exc),
			details="",
			timestamp=datetime.datetime.utcnow().isoformat(),
		)
		return JSONResponse(status_code=429, content=error.model_dump())
	except Exception as exc:
		error = ErrorResponse(
			success=False,
			ip=request.client.host,
			port=request.client.port,
			error="InternalServerError",
			message=str(exc),
			details=traceback.format_exc(),
			timestamp=datetime.datetime.utcnow().isoformat(),
		)
		return JSONResponse(status_code=500, content=error.model_dump())