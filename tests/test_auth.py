import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest
from fastapi.testclient import TestClient
from jose import JWTError, jwt
from main import app
from authentication.auth import authenticate_user, create_access_token, create_refresh_token, get_current_active_user, get_current_user, get_password_hash, verify_password
from config.config import SECRET_KEY, ALGORITHM



client = TestClient(app)

fake_users_db = {}

# Sample user for testing
test_user = {"username": "testuser", "password": "testpassword"}
# Hash the sample user's password and add them to the fake database
fake_users_db[test_user["username"]] = {
    **test_user,
    "hashed_password": get_password_hash(test_user["password"]),
    "disabled": False,
}

def test_password_hashing():
    plain_password = "mysecret"
    hashed_password = get_password_hash(plain_password)
    assert verify_password(plain_password, hashed_password) == True
    assert verify_password("wrongpassword", hashed_password) == False

def test_authenticate_user():
    assert authenticate_user(fake_users_db, test_user["username"], test_user["password"]) is not False
    assert authenticate_user(fake_users_db, test_user["username"], "wrongpassword") is False
    assert authenticate_user(fake_users_db, "nonexistentuser", "password") is False

# def test_token_creation_and_verification():
#     access_token = create_access_token(data={"sub": test_user["username"]})
#     refresh_token = create_refresh_token(data={"sub": test_user["username"]})
#     assert access_token is not None
#     assert refresh_token is not None
#     # Verify if the tokens can be decoded successfully within the expiration time
#     with pytest.raises(Exception):
#         # Attempting to decode with incorrect secret or algorithm should raise an exception
#         jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)


# @pytest.mark.asyncio
# async def test_get_current_user():
#     token = create_access_token(data={"sub": test_user["username"]})
#     response = await get_current_user(token)
#     print(token, response)
#     assert response.username == test_user["username"]

# @pytest.mark.asyncio
# async def test_get_current_active_user():
#     current_user = await get_current_user(create_access_token(data={"sub": test_user["username"]}))
#     response = await get_current_active_user(current_user)
#     assert response.username == test_user["username"]
#     assert response.disabled == False

