from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import uuid
import os
from datetime import datetime
import schemas, database, crud, auth

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/add-story", response_model=schemas.TravelStoryResponse)
def add_story(story: schemas.TravelStoryCreate, db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    return crud.create_travel_story(db=db, story=story, user_id=current_user.id)

@router.get("/get-all-stories", response_model=List[schemas.TravelStoryResponse])
def get_all_stories(db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    return crud.get_all_stories(db=db, user_id=current_user.id)

@router.post("/image-upload")
async def upload_image(image: UploadFile = File(...)):
    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"{UPLOAD_DIR}/{unique_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {"imageUrl": f"http://127.0.0.1:8000/uploads/{unique_filename}"}

@router.put("/edit-story/{id}", response_model=schemas.TravelStoryResponse)
def edit_story(id: int, story: schemas.TravelStoryUpdate, db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    db_story = crud.update_story(db=db, story_id=id, story=story, user_id=current_user.id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@router.delete("/delete-story/{id}")
def delete_story(id: int, db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    success = crud.delete_story(db=db, story_id=id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"message": "Story deleted successfully"}

@router.put("/update-is-favourite/{id}", response_model=schemas.TravelStoryResponse)
def update_is_favourite(id: int, is_favourite: bool = Query(...), db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    db_story = crud.update_is_favourite(db=db, story_id=id, is_favourite=is_favourite, user_id=current_user.id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@router.get("/search", response_model=List[schemas.TravelStoryResponse])
def search_stories(query: str, db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    return crud.search_stories(db=db, query=query, user_id=current_user.id)

@router.get("/travel-stories/filter", response_model=List[schemas.TravelStoryResponse])
def filter_stories(startDate: str, endDate: str, db: Session = Depends(database.get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    try:
        start = datetime.fromtimestamp(int(startDate) / 1000)
        end = datetime.fromtimestamp(int(endDate) / 1000)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    return crud.filter_stories_by_date_range(db=db, start_date=start, end_date=end, user_id=current_user.id)
