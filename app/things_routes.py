from app.models import Thing, ThingsPaginatedArray, UpsertResponse, MongoThing
from app.settings import TaskServiceBaseSettings

from fastapi import APIRouter, Request, HTTPException, status, Query
from typing import Union, List
from beanie.operators import Set
from beanie.odm.queries.update import UpdateResult

settings = TaskServiceBaseSettings()

router = APIRouter()


@router.put("/", response_description="Create a new task",
            status_code=status.HTTP_201_CREATED, response_model=UpsertResponse)
async def create_task(things: List[Thing]):
    added = []
    updated = []
    errors = []

    for doc in things:
        try:
            r: UpdateResult = await MongoThing.find_one(MongoThing.thing_id == doc.thing_id).update_one(
                Set({MongoThing.type: doc.type, MongoThing.params: doc.params}), upsert=True)

            if r.acknowledged:
                if r.matched_count == 0:
                    added.append(doc)
                elif r.matched_count == 1:
                    updated.append(doc)
                else:
                    errors.append(doc)
            else:
                errors.append(doc)
        except:
            errors.append(doc)

    return {"added": added, "updated": updated, "errors": errors}


@router.get("/", response_description="List all tasks",
            response_model=ThingsPaginatedArray)
async def list_tasks(request: Request, page: Union[int, None] = Query(default=0, ge=0),
                     page_size: Union[int, None] = Query(default=1000, ge=1, le=1000)):

    things = await MongoThing.find_all().skip(page * page_size).limit(page_size).to_list()

    return {"data": things, "data_count": len(things), "total_count": None,
            "previous": str(request.url.replace_query_params(page=page, page_size=page_size)),
            "next": str(request.url.replace_query_params(page=page+1, page_size=page_size))}


@router.get("/{id}", response_description="Get a single task by id", response_model=Thing)
async def find_task(id: str):

    r = await MongoThing.find_one(MongoThing.thing_id == id)

    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found")

    return r


@router.delete("/{id}", response_description="Delete a task", response_model=Thing)
async def delete_task(id: str):

    r = await MongoThing.find_one(MongoThing.thing_id == id)

    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found")

    await r.delete()

    return r
