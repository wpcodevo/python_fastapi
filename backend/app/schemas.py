#from __future__ import annotations
from typing import Union
from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, constr


class UserBaseSchema(BaseModel):
    name: str
    username: str
    
    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    
class LoginUserSchema(BaseModel):
    username: str
    password: constr(min_length=8)


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FilteredUserResponse(UserBaseSchema):
    id: uuid.UUID


class ProjectBaseSchema(BaseModel):
    title: str
    zip_code: int
    cost: float
    done: bool
    deadline: datetime
    username: Union[ str, None] = None

    class Config:
        orm_mode = True


class CreateProjectSchema(ProjectBaseSchema):
    pass


class ProjectResponse(ProjectBaseSchema):
    id: uuid.UUID
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime

class ProjectResponseCep(ProjectResponse):
    cidade: str
    uf: str
    

class UpdateProjectSchema(BaseModel):
    title: Union[ str , None] = None
    zip_code: Union[int , None] = None
    cost: Union[float , None] = None
    done: Union[bool , None] = None
    deadline: Union[datetime , None] = None
    username: Union[str , None] = None

    class Config:
        orm_mode = True


class ListProjectResponse(BaseModel):
    status: str
    results: int
    projects: List[ProjectResponse]
