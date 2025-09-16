from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from backend.repository import queries, models
from backend.db import Store
from backend.routers.auth import Actor
import structlog

logger = structlog.get_logger(module=__name__)

Job = models.Job
ListJob = queries.ListJobsWithCustomerBySubRow
router = APIRouter()


@router.post("/api/user/{sub}/job", response_model=Job, status_code=status.HTTP_201_CREATED)
async def create_job(store: Store, sub: str, actor: Actor, input: queries.CreateJobParams) -> Job:
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.create_job(
            queries.CreateJobParams(
                sub=sub,
                customer_id=input.customer_id,
                job_title=input.job_title,
                start_date=input.start_date,
                end_date=input.end_date,
            )
        )
        return (result)

    except IntegrityError as err:
        logger.warning(f"action blocked by database integrity error: {err}")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/api/user/{sub}/job/{job_id}", response_model=Job)
async def update_job(
    store: Store, sub: str, actor: Actor, input: queries.UpdateJobParams
) -> Job:
    """
    Update an existing job. Partial updates are supported.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.update_job(input)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    except IntegrityError as err:
        logger.warning(f"action blocked by database integrity error: {err}")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/api/user/{sub}/job/{job_id}", response_model=Job)
async def get_job(store: Store, sub: str, actor: Actor, job_id: str) -> Job:
    """
    Get a job by ID.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.get_job_by_id(job_id=job_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/api/user/{sub}/jobs", response_model=list[Job])
async def list_jobs_by_sub(store: Store, sub: str, actor: Actor) -> list[Job]:
    """
    List all jobs for a user.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        sub_ = sub
        result = [job async for job in store.list_jobs_by_sub(sub=sub_)]
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/api/user/{sub}/job/{job_id}", status_code=status.HTTP_200_OK)
async def delete_user(store: Store, sub: str, actor: Actor, job_id: str) -> dict:
    """
    Delete a job by ID.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        job_id = job_id
        await store.delete_job(job_id=job_id)
        return {"message": "Job deleted successfully"}
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/api/user/{sub}/jobs/{customer_id}", response_model=list[Job], status_code=status.HTTP_200_OK)
async def get_jobs_by_customer(store: Store, sub: str, actor: Actor) -> list[Job]:
    """
    List all jobs by customer id.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = [job async for job in store.get_jobs_by_customer_id()]
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/api/user/{sub}/jobs/{status}", response_model=list[Job], status_code=status.HTTP_200_OK)
async def get_jobs_by_status(store: Store, sub: str, actor: Actor) -> list[Job]:
    """
    List all jobs by status.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = [job async for job in store.get_jobs_by_status()]
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/api/user/{sub}/jobs/dates/{start}/{end}", response_model=list[Job], status_code=status.HTTP_200_OK)
async def get_jobs_by_date_range(store: Store, sub: str, actor: Actor) -> list[Job]:
    """
    List all jobs by date range.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = [job async for job in store.get_jobs_by_date_range()]
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/api/user/{sub}/jobs-customer/", response_model=list[ListJob], status_code=status.HTTP_200_OK)
async def list_jobs_with_customer_by_sub(store: Store, sub: str, actor: Actor) -> int:
    """
    List all jobs with customer details for a user.
    """
    if sub != actor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        sub_ = sub
        result = [job async for job in store.list_jobs_with_customer_by_sub(sub=sub_)]
        return result

    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
