import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from app.oauth2 import require_user

router = APIRouter()


@router.get('/', response_model=schemas.ListPostResponse)
def get_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit

    posts = db.query(models.Post).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(posts), 'posts': posts}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePostSchema, db: Session = Depends(get_db), owner_id: str = Depends(require_user)):
    post.user_id = uuid.UUID(owner_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: str, post: schemas.UpdatePostSchema, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No post with this id: {id} found')
    if updated_post.user_id != uuid.UUID(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    post.user_id = user_id
    post_query.update(post.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_post


@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with this id: {id} found")
    return post


@router.delete('/{id}')
def delete_post(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')

    if str(post.user_id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
