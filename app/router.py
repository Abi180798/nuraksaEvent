from app.Users.router import user_router
from app.TahuraEvent.router import eventRouter
from app import app

# app.include_router(user_router, prefix="/users")
app.include_router(eventRouter, prefix="/event")