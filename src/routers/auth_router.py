from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.student import Student
from src.models.admin import Admin
from src.schemas.auth_schema import LoginRequest, LoginResponse
from src.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service = AuthService()


@router.post("/register/student")
def register_student(
    student: Student,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.register_student(
            db,
            student
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/register/admin")
def register_admin(
    admin: Admin,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.register_admin(
            db,
            admin
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/login/student",
    response_model=LoginResponse
)
def login_student(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.login_student(
            db,
            request.email,
            request.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.post(
    "/login/admin",
    response_model=LoginResponse
)
def login_admin(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.login_admin(
            db,
            request.email,
            request.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.post("/logout")
def logout():
    return auth_service.logout()