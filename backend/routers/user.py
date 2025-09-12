from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from backend.repository import queries, models
from backend.routers.auth import Actor, NewActor
from backend.db import Store
import structlog
from pydantic import BaseModel

logger = structlog.get_logger(module=__name__)

User = models.User
router = APIRouter()


class CreateUserResponse(BaseModel):
    message: str
    user: User


@router.post("/api/user", response_model=CreateUserResponse)
async def create_user(store: Store, actor: NewActor, input: queries.CreateUserParams) -> User:
    """
    Create a new user.
    """
    if input.sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        # username: models.Username = await assign_username(store)
        result = await store.create_user(
            queries.CreateUserParams(
                sub=input.sub,
                email=input.email,
                first_name=input.first_name,
                last_name=input.last_name,
                birthdate=input.birthdate,
            )
        )
        assert isinstance(result, models.User)
    except IntegrityError as err:
        logger.warning(f"action blocked by database integrity error: {err}")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return CreateUserResponse(message="User created successfully", user=result)


@router.get("/api/user/{sub}", status_code=status.HTTP_200_OK)
async def get_user(store: Store, sub: str, actor: Actor) -> User:
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.get_user_by_sub(sub=sub)
        assert isinstance(result, models.User)
        return result
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/api/user/{sub}", status_code=status.HTTP_200_OK)
async def delete_user(store: Store, sub: str, actor: Actor) -> dict:
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        await store.delete_user_by_sub(sub=sub)
        return {"message": "User deleted successfully"}
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/api/users", response_model=list[User], status_code=status.HTTP_200_OK)
async def list_users(store: Store) -> list[User]:
    try:
        result = [user async for user in store.list_users()]  # Consume the async generator
        return result
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
