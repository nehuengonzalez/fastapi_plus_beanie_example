import re

from beanie import Document, Indexed

from pydantic import BaseModel, field_validator
from typing import List, Annotated


#######################################
# fastapi/beanie models
#######################################

class Thing(BaseModel):
    thing_id: Annotated[str, Indexed(str, unique=True)]
    type: str
    params: str

    @classmethod
    @field_validator("id")
    def well_formed_id(cls, c_id: str) -> str:
        regex = '[^A-Za-z0-9\-\__]'
        if re.search(regex, c_id) is not None:
            raise ValueError("Contains illegal characters")
        return c_id


class MongoThing(Document, Thing):
    hidden_field: str = "algo"


class PaginatedArray(BaseModel):
    data_count: int
    total_count: int | None
    next: str
    previous: str


class ThingsPaginatedArray(PaginatedArray):
    data: List[Thing]


class UpsertResponse(BaseModel):
    added: List[Thing]
    updated: List[Thing]
    errors: List[Thing]
