from fastapi import APIRouter, Body, Depends

from exceptions.custom_http_exceptions import http_exception_handler
from schemas import ParseQuotesRequest, ParseQuotesResponse
from services.celery_worker import parse_and_store_task
import nest_asyncio



parsing_router = APIRouter()

@parsing_router.post("/parse-quotes-task")
async def parse_quotes_task(parse_quotes_request: ParseQuotesRequest = Body(...)) -> ParseQuotesResponse:
    task = parse_and_store_task.delay(page_url=parse_quotes_request.page_url)
    return ParseQuotesResponse(task_id=task.id)