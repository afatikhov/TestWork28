from typing import Any

from fastapi import APIRouter, Depends

from exceptions.custom_http_exceptions import http_exception_handler
from infrastructure.rest_api.depends.quotes_depends import get_quotes_service
from services.quotes_service import QuotesService

quotes_router = APIRouter()

@quotes_router.get("/quotes")
@http_exception_handler
async def get_quotes(author: str | None = None,
                     tag: str | None = None,
                     quotes_service: QuotesService=Depends(get_quotes_service)):
    result: list[dict[str, Any]] = await quotes_service.get_quotes_by_filer(author=author,
                                                                            tag=tag)
    return result