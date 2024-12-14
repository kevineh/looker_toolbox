from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api import auth, dashboards, migration
from middleware.auth_middleware import verify_token_middleware

app = FastAPI(title="Looker Dashboard Migration Tool")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(
    dashboards.router,
    prefix="/api/dashboards",
    tags=["dashboards"],
    dependencies=[Depends(verify_token_middleware)],
)
app.include_router(
    migration.router,
    prefix="/api/migration",
    tags=["migration"],
    dependencies=[Depends(verify_token_middleware)],
)
