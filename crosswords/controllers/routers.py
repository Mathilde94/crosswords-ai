from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from crosswords.service.crossword_service import CrosswordService
from crosswords.service.tasks.tasks import generate_crossword_task

from .crossword_request import CrosswordRequest, CrosswordVerifyRequest

crosswords_router = APIRouter(prefix="/crosswords")


@crosswords_router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    crossword_request: CrosswordRequest, background_tasks: BackgroundTasks
):
    new_crossword = CrosswordService.create_crossword(
        crossword_request.context, crossword_request.concepts
    )
    background_tasks.add_task(generate_crossword_task, new_crossword.id, tries=2)
    return new_crossword.serialize()


@crosswords_router.post("/verify", status_code=status.HTTP_201_CREATED)
async def create(
    crossword_verify_request: CrosswordVerifyRequest
):
    try:
        crossword = CrosswordService.get_crossword(crossword_verify_request.id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crossword not found"
        )
    return {"correct": crossword.verify(crossword_verify_request.matrix)}


@crosswords_router.get("/", status_code=status.HTTP_200_OK)
async def get(crossword_id: str):
    try:
        crossword = CrosswordService.get_crossword(crossword_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crossword not found"
        )
    return crossword.serialize()


routers = [crosswords_router]
