from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

class UserBase(BaseModel):
    """Core user data common to all endpoints."""
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., description="User's full name")
    preferred_language: str = Field("en", description="Preferred language code (en, fj, hi)")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password for registration")

class UserResponse(UserBase):
    id: int = Field(..., description="User unique identifier")

# Simulated user storage for scaffolding (replace with real DB layer)
_fake_users_db = {}

# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new eVisa portal user. Returns user profile on success.",
    responses={400: {"description": "User with this email already exists."}},
)
def create_user(user: UserCreate):
    """
    Register a new user.

    - **email**: Email address (must be unique)
    - **full_name**: User's full name
    - **preferred_language**: Language code
    - **password**: Password
    """
    if user.email in _fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists.")
    user_id = len(_fake_users_db) + 1
    _fake_users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "full_name": user.full_name,
        "preferred_language": user.preferred_language
    }
    return UserResponse(
        id=user_id,
        email=user.email,
        full_name=user.full_name,
        preferred_language=user.preferred_language
    )

# PUBLIC_INTERFACE
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Fetch user profile for given user id.",
    responses={404: {"description": "User not found."}},
)
def get_user(user_id: int):
    """
    Get user profile by user ID.
    """
    for user in _fake_users_db.values():
        if user["id"] == user_id:
            return UserResponse(**user)
    raise HTTPException(status_code=404, detail="User not found.")
