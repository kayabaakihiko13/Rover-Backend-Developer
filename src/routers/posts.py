from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os

from src.routers.utils import get_db
from src.models.posts import Post
from src.models.users import User
from src.schema.posts import PostResponse
from src.models import utils
router = APIRouter(prefix='/posts', tags=['posts'])

# pastikan folder benar (uploads, bukan uploades)
os.makedirs("uploads/post_images", exist_ok=True)


@router.post("/{user_id}", response_model=PostResponse)
async def create_post(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # cek user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # generate file name
    file_name = f"{utils.generate_uuid()}_{file.filename}"
    file_location = os.path.join("uploads", "post_images", file_name)

    # saving file object
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    # simpan record di DB (simpan relative path biar gampang dipakai di frontend)
    image_url = file_location

    new_post = Post(
        post_id=utils.generate_uuid(),
        user_id=user_id,
        image_url=image_url,
        create_at=datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
