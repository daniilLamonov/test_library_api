from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..deps import CurrentUser
from ..schemas.users import UserRegisterSchema, UserSchema
from ...core.security import verify_password, create_access_token, hash_password
from ...repo.users import UserRepo

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserSchema)
async def register_user(creds: UserRegisterSchema):
    user_in_db = await UserRepo.get_one_or_none(email=creds.email)
    if user_in_db is None:
        try:
            user = await UserRepo.create(
                {
                    "username": creds.username,
                    "email": creds.email,
                    "hashed_password": hash_password(creds.password),
                }
            )
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=409, detail="Email already registered")


@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password
    user = await UserRepo.get_one_or_none(email=email)
    if user:
        if verify_password(password, user.hashed_password):
            token = create_access_token({"sub": str(user.uuid)})
            return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=404, detail="Not found user")

@router.get("/me", response_model=UserSchema)
async def get_users(current_user: CurrentUser):
    return current_user
