from datetime import timedelta
from fastapi import (APIRouter,Depends,HTTPException,
                     status)
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt,JWTError
from sqlalchemy import text


from src.schema.users import (RegisterRequest,UserResponse,
                              TokenResponse,ForgetPasswordRequest,
                              ResetPasswordRequest)
from src.models.users import User
from src.routers.utils import (get_db,hash_password,verify_password,
                               oauth2_scheme,create_access_token)
from src.settings.config import settings

router = APIRouter(prefix='/users',tags=['users'])

# decode jwt
def _get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_JWT, 
                             algorithms=[settings.ALGORITHM])
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
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    # kalau sukses -> balikin data user (tanpa password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me",response_model=UserResponse)
def read_users_me(current_user: User = Depends(_get_current_user)):
    return current_user


# make fitur reset password
@router.post("/forgot-password")
async def forget_password(request: ForgetPasswordRequest, db: Session = Depends(get_db)):
    query = text("""
        SELECT * FROM users
        WHERE email = :email AND username = :username
        LIMIT 1
    """)
    result = db.execute(query, {"email": request.email, "username": request.username}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Email/Username not found or mismatch")

    # generate reset token
    reset_token_expires = timedelta(minutes=30)
    reset_token = create_access_token(
        data={"sub": str(result.user_id), "reset": True},
        expires_delta=reset_token_expires
    )

    reset_link = f"http://localhost:8000/users/reset-password?token={reset_token}"
    print("Send this reset link to user:", reset_link)
    # contoh: kirim lewat email
    return {
    "message": "Reset link sent to your email",
    "reset_link": reset_link
    }



@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.token,settings.SECRET_KEY_JWT, 
                             algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if not payload.get("reset"):  # pastikan token ini untuk reset
            raise HTTPException(status_code=400, detail="Invalid token type")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # pastikan password baru != confirm password
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Password dan konfirmasi tidak sama")

    # pastikan password baru != password lama
    if verify_password(request.new_password,user.password):
        raise HTTPException(status_code=400,detail="Password baru tidak boleh sama dengan password lama")
    # update password baru (hash dulu)
    user.password = hash_password(request.new_password)
    db.commit()
    return {"message": "Password has been reset successfully"}
