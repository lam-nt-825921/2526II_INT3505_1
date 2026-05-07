from fastapi import FastAPI, Request
from .api.v1.endpoints import router as v1_router
from .db.session import engine, Base
from .models import payment # Import models to register them with Base
from fastapi.middleware.cors import CORSMiddleware
import traceback

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment API", version="1.0.0")

# ... (middleware and routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Versioning strategy: URL path
app.include_router(v1_router, prefix="/v1", tags=["v1"])

@app.middleware("http")
async def add_api_version_header(request: Request, call_next):
    try:
        response = await call_next(request)
        # Adding version header to responses
        if request.url.path.startswith("/v1"):
            response.headers["X-API-Version"] = "1.0"
        return response
    except Exception as e:
        print(f"Middleware Error: {e}")
        traceback.print_exc()
        raise e

@app.get("/")
def root():
    return {"message": "Welcome to Payment API. Use /v1 for version 1."}
