from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user: dict):
    """
    Create a new user.
    """
    user=user
    # Here you would typically add logic to save the user to a database
    return {"message": "User created successfully", "user": user}

@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    """
    Retrieve a user by ID.
    """
    # fetch user from db by user_id
    user = user_id
    return {"message": "User fetched successfully", "user": user}
