from sqlalchemy.orm import Session
from src.models.admin import Admin
from src.models.admin_model import AdminModel


class AdminRepository:
    def create(self, db: Session, admin: Admin):
        admin_model = AdminModel(
            name=admin.name,
            email=admin.email,
            password=admin.password
        )

        db.add(admin_model)
        db.commit()
        db.refresh(admin_model)

        return {
            "id": admin_model.id,
            "name": admin_model.name,
            "email": admin_model.email
        }

    def find_by_id(self, db: Session, admin_id: int):
        admin = (db.query(AdminModel).filter(AdminModel.id == admin_id).first())

        if admin is None:
            return None

        return {
            "id": admin.id,
            "name": admin.name,
            "email": admin.email
        }

    def find_all(self, db: Session):
        admins = db.query(AdminModel).all()

        return [
            {
                "id": admin.id,
                "name": admin.name,
                "email": admin.email
            }
            for admin in admins
        ]

    def find_by_email(self, db: Session, email: str):
        return (db.query(AdminModel).filter(AdminModel.email == email).first())