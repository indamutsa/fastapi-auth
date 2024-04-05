from pydantic import BaseModel

# Create a token class
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None
    
# Create ToeknData class
class TokenData(BaseModel):
    username: str | None = None
    
# Create a User class
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    
# Create a UserInDB class
class UserInDB(User):
    hashed_password: str