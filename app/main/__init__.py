from fastapi import APIRouter


main_router = APIRouter(
    tags=["weather"]
)



from app.main import routes