from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.db.database import Database
from app.router.auth_router import auth_router
from app.router.user_routes import user_routes
from app.router.admin_router import admin_router
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.auth_middleware import JWTAuthMiddleware
from app.utils.api_response import error_response

async def lifespan(app:FastAPI):
    await Database.connect()
    yield
    await Database.disconnect()

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="School Management System API",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Middleware
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:8000",  # your frontend dev URL
    # Add your prod frontend URL here,
    "http://127.0.0.1:8000"
]

app.add_middleware(JWTAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "School Management System API"}


app.include_router(auth_router)
app.include_router(user_routes)
app.include_router(admin_router)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request : Request, exc : HTTPException):
    return error_response(
        message=exc.detail,
        status_code=exc.status_code
    )



@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return error_response(message="Internal server error",error=str(exc), status_code=500)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"][1:])  # skip "body"
        errors.append({
            "field": field,
            "message": err["msg"]
        })

    return error_response(
        message="Validation Error",
        error=errors,
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )
