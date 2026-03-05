from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound, IntegrityError

def register_exception_handlers(app: FastAPI) -> None:
    
    @app.exception_handler(NoResultFound)
    def no_result_found_handler(request: Request, exc: NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail" : "Requested resource not found"}
        )
    
    
    @app.exception_handler(IntegrityError)
    def integrity_error_handler(request: Request, exc: IntegrityError):
        if "UNIQUE constraint failed: users.email" in str(exc.orig):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail" : "User with this email already exists"}
            )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database integrity error"}
        )