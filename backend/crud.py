from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, auth

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, fullName=user.fullName, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_travel_story(db: Session, story: schemas.TravelStoryCreate, user_id: int):
    db_story = models.TravelStory(**story.dict(), userId=user_id)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

def get_all_stories(db: Session, user_id: int):
    return db.query(models.TravelStory).filter(models.TravelStory.userId == user_id).order_by(models.TravelStory.isFavourite.desc()).all()

def update_story(db: Session, story_id: int, story: schemas.TravelStoryUpdate, user_id: int):
    db_story = db.query(models.TravelStory).filter(models.TravelStory.id == story_id, models.TravelStory.userId == user_id).first()
    if db_story:
        update_data = story.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_story, key, value)
        db.commit()
        db.refresh(db_story)
    return db_story

def delete_story(db: Session, story_id: int, user_id: int):
    db_story = db.query(models.TravelStory).filter(models.TravelStory.id == story_id, models.TravelStory.userId == user_id).first()
    if db_story:
        db.delete(db_story)
        db.commit()
        return True
    return False

def update_is_favourite(db: Session, story_id: int, is_favourite: bool, user_id: int):
    db_story = db.query(models.TravelStory).filter(models.TravelStory.id == story_id, models.TravelStory.userId == user_id).first()
    if db_story:
        db_story.isFavourite = is_favourite
        db.commit()
        db.refresh(db_story)
    return db_story

def search_stories(db: Session, query: str, user_id: int):
    return db.query(models.TravelStory).filter(
        models.TravelStory.userId == user_id,
        (models.TravelStory.title.ilike(f"%{query}%")) | (models.TravelStory.story.ilike(f"%{query}%"))
    ).all()

def filter_stories_by_date_range(db: Session, start_date: datetime, end_date: datetime, user_id: int):
    return db.query(models.TravelStory).filter(
        models.TravelStory.userId == user_id,
        models.TravelStory.visitedDate >= start_date,
        models.TravelStory.visitedDate <= end_date
    ).all()
