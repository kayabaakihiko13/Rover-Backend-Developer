from datetime import timedelta
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt,JWTError


from src.schema.users import (RegisterRequest,UserResponse,
                              TokenResponse)
from src.models.users import User
from src.routers.utils import (get_db,hash_password,
                               verify_password,oauth2_scheme,
                               SECRET_KEY,ALGORITHM,
                               create_access_token,
                               ACCESS_TOKEN_EXPIRE_MINUTES)


router = APIRouter(prefix='/users',tags=['users'])

# decode jwt
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.user_id == str(user_id)).first()
    if user is None:
        raise credentials_exception
    return user



# create user

@router.post("/register",response_model=UserResponse)
async def register_user(user:RegisterRequest,db:Session = Depends(get_db)):
    # ceck email unik
    existing_user = db.query(User).filter(User.email == user.email).first()
    if (existing_user):
        raise HTTPException(status_code=400, 
                            detail="Email already registered")
    
    # check username unik
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400,detail="Username already taken")

    hashed_pw = hash_password(user.password)

    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    # kalau sukses -> balikin data user (tanpa password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me",response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user