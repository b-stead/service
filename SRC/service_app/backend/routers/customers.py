from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from backend.repository import queries, models
from backend.db import Store
from backend.routers.auth import Actor
import structlog

logger = structlog.get_logger(module=__name__)

Customer = models.Customer
router = APIRouter()


@router.post("/user/{sub}/customer", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(store: Store, sub: str, actor: Actor, input: queries.CreateCustomerParams) -> Customer:
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.create_customer(
            queries.CreateCustomerParams(
                sub=sub,
                company_name=input.company_name,
                email=input.email,
            )
        )
        return (result)

    except IntegrityError as err:
        logger.warning(f"action blocked by database integrity error: {err}")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/user/{sub}/customer/{customer_id}", response_model=Customer)
async def update_customer(
    store: Store, sub: str, actor: Actor, input: queries.UpdateCustomerParams
) -> Customer:
    """
    Update an existing customer. Partial updates are supported.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.update_customer(input)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    except IntegrityError as err:
        logger.warning(f"action blocked by database integrity error: {err}")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/user/{sub}/customer/{customer_id}", response_model=Customer)
async def get_customer(store: Store, sub: str, actor: Actor, customer_id: str) -> Customer:
    """
    Get a customer by ID.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.get_customer_by_id(queries.GetCustomerByIdParams(sub=sub, customer_id=customer_id))
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/user/{sub}/customers", response_model=list[Customer])
async def list_customers_by_sub(store: Store, sub: str, actor: Actor) -> list[Customer]:
    """
    List all customers for a user.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        sub_ = sub  # to avoid unused variable warning
        result = [customer async for customer in store.list_customers_by_sub(sub=sub_)]
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
