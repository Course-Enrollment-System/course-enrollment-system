from pydantic import BaseModel

from src.models.role import Role


class Admin(BaseModel):
    name: str
    email: str
    password: str
    role: Role = Role.ADMIN