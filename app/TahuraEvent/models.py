from database import Base, session
from sqlalchemy import *
from .schemas import EventModel
from datetime import datetime

class TahuraEvent(Base):
  __tablename__ = "tahuraevent"
  id_event= Column(Integer, primary_key=True, index=True)
  judul_event= Column(String, nullable=False, default="")
  deskripsi_event= Column(Text, default="")
  gambar_event = Column(String, default="")
  tanggal_event = Column(DateTime, default="")
  tanggal_post =  Column(DateTime, nullable=False, default=datetime.now())

  @staticmethod
  def fromModel(event: EventModel):
    return TahuraEvent(
      judul_event = event.judul_event,
      deskripsi_event = event.deskripsi_event,
      gambar_event = event.gambar_event,
      tanggal_event = datetime.strptime(event.tanggal_event,"%d-%m-%Y"),
      tanggal_post = datetime.now()
    )
  
  @staticmethod
  def addEvent(event: EventModel):
    newEvent = TahuraEvent.fromModel(event)
    session.add(newEvent)
    session.commit()
    return newEvent

  @staticmethod
  def getEvent():
    return session.query(TahuraEvent).all()

  @staticmethod
  def getEventBy(*args, **kwargs):
    return session.query(TahuraEvent).filter(*args, **kwargs).first()

  def setJudulEvent(self,newJudul):
    if newJudul is not None and newJudul:
      self.judul_event=newJudul

  def setDeskripsiEvent(self,newDeskripsi):
    if newDeskripsi is not None and newDeskripsi:
      self.deskripsi_event=newDeskripsi

  def setGambarEvent(self,newGambar):
    if newGambar is not None and newGambar:
      self.gambar_event=newGambar

  def setTanggalEvent(self,newTanggalE):
    if newTanggalE is not None and newTanggalE:
      self.tanggal_event=datetime.strptime(newTanggalE,"%d-%m-%Y")
  
  @staticmethod
  def update(event:EventModel,id):
    old_event : TahuraEvent=TahuraEvent.getEventBy(TahuraEvent.id_event==id)
    if old_event is not None:
      old_event.setJudulEvent(event.judul_event)
      old_event.setDeskripsiEvent(event.deskripsi_event)
      old_event.setGambarEvent(event.gambar_event)
      old_event.setTanggalEvent(event.tanggal_event)
      session.commit()
    return old_event

  @staticmethod
  def delete(id):
    event: TahuraEvent = TahuraEvent.getEventBy(TahuraEvent.id_event==id)
    if event is not None:
      session.delete(event)
      session.commit()
      return True
    return event