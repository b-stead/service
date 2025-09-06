from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from backend.repository import queries, models
from backend.db import Store
import structlog

logger = structlog.get_logger(module=__name__)

Customer = models.Customer
router = APIRouter()


@router.post("/user/{sub}/customer", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(store: Store, sub: str, input: queries.CreateCustomerParams) -> Customer:
    """
    Create a new user.
    """
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
    store: Store, sub: str, customer_id: str, input: queries.UpdateCustomerParams
) -> Customer:
    """
    Update an existing customer. Partial updates are supported.
    """
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