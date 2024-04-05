from config.config import ALGORITHM, SECRET_KEY
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from models.model import User, UserInDB, Token, TokenData
from database.db import fake_users_db

# Initialize the CryptContext and OAuth2PasswordBearer
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """
    Verify if a plain password matches a hashed password.

    Args:
        plain_password (str): The plain password to be verified.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hashes the given password using the pwd_context.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def get_user(db, username: str):
    """
    Retrieve a user from the database based on the given username.

    Args:
        db (dict): The database containing user information.
        username (str): The username of the user to retrieve.

    Returns:
        UserInDB: An instance of the UserInDB class representing the retrieved user.

    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str):
    """
    Authenticates a user by checking if the provided username and password match the stored credentials.

    Args:
        fake_db (dict): A dictionary representing a fake database.
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        user (User) or False: If the authentication is successful, returns the authenticated user object.
                              Otherwise, returns False.
    """
    user = get_user(fake_db, username)
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a refresh token using the provided data and expiration delta.

    Args:
        data (dict): The data to be encoded in the refresh token.
        expires_delta (timedelta, optional): The expiration delta for the token. If not provided, a default expiration of 30 days will be used.

    Returns:
        str: The encoded refresh token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create access token, if the user is logged in, we need refresh token but for the first time don't need refresh token
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create an access token with the provided data and expiration time.

    Args:
        data (dict): The data to be encoded in the access token.
        expires_delta (timedelta, optional): The expiration time for the access token.
            If not provided, a default expiration time of 15 minutes will be used.

    Returns:
        str: The encoded access token.

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_tokens(data: dict, expires_delta: timedelta = None):
    access_token = create_access_token(data, expires_delta)
    refresh_token = create_refresh_token(data, expires_delta)
    return Token(access_token=access_token, token_type="bearer", refresh_token = refresh_token)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user based on the provided token.

    Parameters:
    - token (str): The authentication token.

    Returns:
    - user (User): The current user.

    Raises:
    - HTTPException: If the credentials cannot be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Retrieves the current active user.

    Parameters:
    - current_user (User): The current user object.

    Returns:
    - User: The current active user.

    Raises:
    - HTTPException: If the current user is disabled.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
