
from fastapi import APIRouter


router = APIRouter(prefix='/contacts',
                   tags=['Contacts'])


@router.get("/")
async def root():
    return {"message": "Hello World"}
