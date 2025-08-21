# src/routers/result.py
import os
import cv2
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.routers.utils import get_db
from src.models.posts import Post
from src.models.result import Result
from src.schema.results import ResultResponseBase
from src.routers.utils import YOLODetector   # class YOLODetector kamu taruh di folder ml misalnya

router = APIRouter(prefix="/result", tags=["result"])

# load sekali biar ga reload tiap request
detector = YOLODetector("model/best.onnx", "model/data.yaml")

@router.post("/{post_id}", response_model=ResultResponseBase)
async def predict_post(post_id: str, db: Session = Depends(get_db)):
    # cari post berdasarkan post_id
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # pastikan path gambar absolute
    img_path = os.path.join(os.getcwd(), post.image_url.lstrip("/"))
    img_arr = cv2.imread(img_path)
    if img_arr is None:
        raise HTTPException(status_code=400, detail=f"Image not found at {img_path}")

    # deteksi
    try:
        boxes, scores, class_ids = detector.detect(img_arr)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

    # simpan ke result table
    result = Result(
        post_id=post_id,
        result={
            "boxes": boxes if boxes is not None else [],
            "scores": [float(s) for s in scores] if scores is not None else [],
            "class_ids": [int(c) for c in class_ids] if class_ids is not None else [],
        }
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # return schema sesuai pydantic
    return ResultResponseBase(
        result_id=result.result_id,
        post_id=result.post_id,
        image_url=post.image_url,
        result=result.result,
        created_at=result.create_at,
        updated_at=result.update_at,
    )
