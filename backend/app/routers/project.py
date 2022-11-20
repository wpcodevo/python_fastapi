import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from app.oauth2 import require_user

router = APIRouter()


@router.get('/', response_model=schemas.ListProjectResponse)
def get_projects(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit

    projects = db.query(models.Project).group_by(models.Project.id).filter(
        models.Project.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(projects), 'projects': projects}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectResponse)
def create_project(project: schemas.CreateProjectSchema, db: Session = Depends(get_db), owner_username: str = Depends(require_user)):
    project.username = owner_username
    new_project = models.Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.put('/{id}', response_model=schemas.ProjectResponse)
def update_project(id: str, project: schemas.UpdateProjectSchema, db: Session = Depends(get_db), username: str = Depends(require_user)):
    project_query = db.query(models.Project).filter(models.Project.id == id)
    updated_project = project_query.first()

    if not updated_project:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No project with this id: {id} found')
    if updated_project.username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    project_query.update(project.dict(), synchronize_session=False)
    db.commit()
    return updated_project


@router.get('/{id}', response_model=schemas.ProjectResponse)
def get_project(id: str, db: Session = Depends(get_db), username: str = Depends(require_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No project with this id: {id} found")
    return project


@router.delete('/{id}')
def delete_project(id: str, db: Session = Depends(get_db), username: str = Depends(require_user)):
    project_query = db.query(models.Project).filter(models.Project.id == id)
    project = project_query.first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No project with this id: {id} found')

    if project.owner_id != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    project_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
