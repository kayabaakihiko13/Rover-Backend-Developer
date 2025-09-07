from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

import numpy as np
import onnxruntime as ort
import yaml
import cv2


from passlib.context import CryptContext
from src.settings.db import SessionLocal
from src.settings.config import settings

from typing import Any,List


# pasword hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_pw,hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_JWT, 
                             algorithm=settings.ALGORITHM)
    return encoded_jwt



class YOLODetector:
    def __init__(self, model_path:str, label_yaml:str,
                 conf_thresh:float=0.25, iou_thresh:float=0.7,optimize:bool=True):
        """
        this class purpose to vanila parser with onnxruntime ecosystem
        model_path:str = path file model onnx file
        label_yaml:str = path file untuk yaml file
        conf_thresh:float = nilai minum untuk konfinde klasifikasi objek
        iou_thresh:float = nilai minum untuk konfiden deteksi objek
        source:
        https://docs.ultralytics.com/modes/predict/#inference-arguments
        """
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        # Load classes from YAML
        with open(label_yaml, 'r') as f:
            self.CLASSES = yaml.safe_load(f)['names']
        opts = ort.SessionOptions()
        # Load model
        if optimize:
            opts = ort.SessionOptions()
            opts.intra_op_num_threads = 1
            opts.add_session_config_entry("session.intra_op.allow_spinning", "0")
            self.session = ort.InferenceSession(model_path,opts,providers=['CPUExecutionProvider'])
        else:
            self.session = ort.InferenceSession(model_path,opts,providers=['CPUExecutionProvider'])
        input_shape = self.session.get_inputs()[0].shape
        self.INPUT_H = input_shape[2]
        self.INPUT_W = input_shape[3]

    def preprocess(self, image:np.ndarray)->np.ndarray:
        img_resized = cv2.resize(image, (self.INPUT_W, self.INPUT_H))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_norm = img_rgb.astype(np.float32) / 255.0
        img_chw = np.transpose(img_norm, (2, 0, 1))
        return np.expand_dims(img_chw, axis=0)

    def postprocess(self, outputs:Any, orig_h:int, orig_w:int):
        preds = outputs[0]
        preds = np.transpose(preds, (0, 2, 1))[0]
        boxes_xywh = preds[:, :4]
        scores_all = preds[:, 4:]
        class_ids = np.argmax(scores_all, axis=1)
        confidences = np.max(scores_all, axis=1)

        mask = confidences > self.conf_thresh
        boxes_xywh, confidences, class_ids = boxes_xywh[mask], confidences[mask], class_ids[mask]

        boxes = []
        for cx, cy, w, h in boxes_xywh:
            xmin = max(0, (cx - w / 2) * orig_w / self.INPUT_W)
            ymin = max(0, (cy - h / 2) * orig_h / self.INPUT_H)
            xmax = min(orig_w, (cx + w / 2) * orig_w / self.INPUT_W)
            ymax = min(orig_h, (cy + h / 2) * orig_h / self.INPUT_H)
            boxes.append([int(xmin), int(ymin), int(xmax), int(ymax)])

        idxs = cv2.dnn.NMSBoxes(boxes, confidences.tolist(), self.conf_thresh, self.iou_thresh)
        final_boxes, final_scores, final_class_ids = [], [], []
        if len(idxs) > 0:
            for i in idxs.flatten():
                final_boxes.append(boxes[i])
                final_scores.append(confidences[i])
                final_class_ids.append(class_ids[i])
        return final_boxes, final_scores, final_class_ids


    def detect(self, image:np.ndarray)->List:
        orig_h, orig_w = image.shape[:2]
        img_tensor = self.preprocess(image)
        outputs = self.session.run(None, {self.session.get_inputs()[0].name: img_tensor})
        boxes,score,class_ids= self.postprocess(outputs,orig_h,orig_w)
        return boxes,score,class_ids


if __name__ == "__main__":
    model_onnx_path = "model/best.onnx"
    class_yaml_path = "model/data.yaml"
    detector = YOLODetector(model_onnx_path,class_yaml_path)
    img_arr = cv2.imread("uploads/post_images/3d93c4af-3c6e-4515-a5db-638baa83a5b4_aaf9fa17d5e565a21a4a74745922bc8a.jpg")
    _,score,class_ids = detector.detect(img_arr)
    results ={
        "class_id":class_ids,
        "scores":score
    }
    print(results)