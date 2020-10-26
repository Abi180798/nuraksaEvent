from fastapi import APIRouter,Depends,File,UploadFile
from app.response import *
from .views import EventViewControl
from .models import TahuraEvent,session
from .schemas import *
from app.Auth.auth import get_current_superadmin, get_current_admin

import os, io
from starlette.responses import StreamingResponse

ALOWRD_FILE = ['png', 'jpg', 'jpeg']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FOTO_DIR = os.path.join(BASE_DIR, "images")

eventRouter = APIRouter()
viewControl = EventViewControl()

@eventRouter.post("/",status_code=status.HTTP_201_CREATED,response_model=EventResponse)
async def post(
  res:Response,
  event:EventModel,
  authorized = Depends(get_current_admin)
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
  event:EventModel,
  authorized = Depends(get_current_admin)
  ):
  return httpResponse(viewControl.update,res=res,id=id,event=event) 
  
@eventRouter.delete("/{id}",status_code=status.HTTP_200_OK,response_model=EventResponse)
async def deleteById(
  res:Response,
  id:int,
  authorized = Depends(get_current_admin)
  ):
  return httpResponse(viewControl.delete,res=res,id=id) 


@eventRouter.post("/events/photo", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
async def uploadPhoto( 
    res : Response,
    id : int,
    photo :UploadFile = File(...)
    ):
    response = EventResponse()
    event : TahuraEvent = TahuraEvent.getEventBy(TahuraEvent.id_event==id)
    print(event)
    if event is None:
        return response.notfound()
    # photo.file.
    try:
        img_path = os.path.join(FOTO_DIR, photo.filename)
        file_format = img_path.split(".")[1]
        if not file_format in ALOWRD_FILE:
            res.status_code = status.HTTP_400_BAD_REQUEST
            response.badrequest()
            return response
        with open(img_path, 'wb') as f:
            [f.write(chunk) for chunk in iter(lambda: photo.file.read(10000), b'')]

        event.gambar_event = photo.filename
        session.commit()
        response.created()
        response.data = event
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")

@eventRouter.get("/events/photo/{photo_name}", status_code = status.HTTP_200_OK)
async def getPhot(
    res : Response,
    photo_name : str
    ):
    try:
        image_result = open(os.path.join(FOTO_DIR, photo_name), "rb")
        if image_result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="image not found")
        file_format = photo_name.split(".")[1]
        return StreamingResponse(io.BytesIO(image_result.read()), media_type="image/{}".format(file_format))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))