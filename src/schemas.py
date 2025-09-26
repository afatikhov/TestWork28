from pydantic import BaseModel, HttpUrl


class ParseQuotesRequest(BaseModel):
    page_url: str

class ParseQuotesResponse(BaseModel):
    task_id: str