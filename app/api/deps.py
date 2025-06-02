from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.core import settings
from app.db.models import Users
from app.repo.users import UserRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401,
                            detail="Could not validate credentials")
    expire = payload.get('exp')
    if expire is None or datetime.fromtimestamp(expire, tz=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail='Token expired')
    return payload

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    uuid = payload.get('sub')
    if uuid is None:
        raise HTTPException(status_code=401,
                            detail='User not found')
    user = await UserRepo.get_one_or_none(uuid=uuid)
    if not user:
        raise HTTPException(status_code=401,
                            detail='User not found')
    return user

CurrentUser = Annotated[Users, Depends(get_current_user)]