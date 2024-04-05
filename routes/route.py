from datetime import timedelta
from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from database.db import fake_users_db
from models.model import Token, User
from authentication.auth import get_current_active_user, authenticate_user, create_tokens

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to log in and receive an access token.

    Parameters:
    - form_data (OAuth2PasswordRequestForm): The form data containing the username and password.

    Returns:
    - Token: The access token.
    - Token: The refresh token.
    - str: The token type.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    tokens= create_tokens(data={"sub": user.username}, expires_delta=token_expires)
    return {
        "access_token": tokens.access_token,
        "token_type": "bearer",
        "refresh_token": tokens.refresh_token,
    }
    
@router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: str):
    """
    Endpoint to refresh an access token using a refresh token.

    Parameters:
    - refresh_token (str): The refresh token.

    Returns:
    - Token: The new access token.
    - Token: The new refresh token.
    - str: The token type.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        tokens = create_tokens(data={"sub": username}, expires_delta=access_token_expires)
        return {
            "access_token": tokens.access_token,
            "token_type": "bearer",
            "refresh_token": tokens.refresh_token,
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to retrieve information about the current user.

    Parameters:
    - current_user (User): The current user.

    Returns:
    - User: The current user.
    """
    return current_user

@router.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to retrieve items belonging to the current user.

    Parameters:
    - current_user (User): The current user.

    Returns:
    - dict: A dictionary containing the items belonging to the current user.
    """
    return {"items": [{"item_id": "Foo", "owner": current_user}]}