from app.schemas import BaseModel, BaseResponse, ListMeta, Field
from typing import List, Optional
from datetime import datetime

class EventBaseModel(BaseModel):
    id_event : Optional[int] = Field(description="event id, generate from server")
    judul_event : str = Field(description="judul event name")
    deskripsi_event : str = Field(description="description event")
    gambar_event : Optional[str] = Field(description="gambar event")
    tanggal_event : datetime = Field(description="tanggal event")
    tanggal_post : Optional[datetime] = Field(description="tanggal post")

    class Config:
      orm_mode=True

class EventModel(EventBaseModel):
    tanggal_event : str = Field(description="tanggal event",default=str(datetime.now()))

class EventParseModel(EventModel):
    tanggal_event : datetime = Field(description="tanggal event",default=str(datetime.now()))

class EventResponse(BaseResponse):
    data : EventParseModel = None 


class EventsResponse(BaseResponse):
    data : List[EventParseModel] = []
    meta : ListMeta = ListMeta()