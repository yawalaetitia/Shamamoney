from sqlalchemy.orm import Session
import models, database, crud, schemas

def seed_super_admin():
    db: Session = database.SessionLocal()
    existing = crud.get_user_by_username(db, "superadmin")
    if not existing:
        crud.create_user(db, schemas.UserCreate(
            username="superadmin",
            password="admin123",  # tu peux hasher plus tard
            role=schemas.UserRole.super_admin
        ))
    db.close()
