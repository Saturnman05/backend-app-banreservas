from fastapi import FastAPI

from accounts.routes import router as accounts_router
from auth.routes import router as auth_router
from cards.routes import router as cards_router
from claims.routes import router as claims_router
from users.routes import router as users_router

from core.config import ENV, DEV

import os
import uvicorn

app = FastAPI()

app.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(cards_router, prefix="/cards", tags=["Cards"])
app.include_router(claims_router, prefix="/claims", tags=["Claims"])
app.include_router(users_router, prefix="/user", tags=["User"])
