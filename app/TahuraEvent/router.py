from fastapi import APIRouter
from app.response import *
from .views import EventViewControl
from .schemas import *

eventRouter = APIRouter()
viewControl = EventViewControl()

@eventRouter.post("/",status_code=status.HTTP_201_CREATED,response_model=EventResponse)
async def post(
  res:Response,
  event:EventModel
  ):
  return httpResponse(viewControl.post,res=res,event=event)

@eventRouter.get("/",status_code=status.HTTP_200_OK,response_model=EventsResponse)
async def get(
  res:Response,
  ):
  return httpResponse(viewControl.get,res=res) 

@eventRouter.get("/{id}",status_code=status.HTTP_200_OK,response_model=EventResponse)
async def getById(
  res:Response,
  id:int
  ):
  return httpResponse(viewControl.getSingle,res=res,id=id)

@eventRouter.put("/{id}",status_code=status.HTTP_200_OK,response_model=EventResponse)
async def updateById(
  res:Response,
  id:int,
  event:EventModel
  ):
  return httpResponse(viewControl.update,res=res,id=id,event=event) 
  
@eventRouter.delete("/{id}",status_code=status.HTTP_200_OK,response_model=EventResponse)
async def deleteById(
  res:Response,
  id:int,
  ):
  return httpResponse(viewControl.delete,res=res,id=id) 