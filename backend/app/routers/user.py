from fastapi import APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2

router = APIRouter()


@router.get('/me', response_model=schemas.UserResponse)
def get_me(db: Session = Depends(get_db), username: str = Depends(oauth2.require_user)):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user
