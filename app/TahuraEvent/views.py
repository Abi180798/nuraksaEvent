from .models import TahuraEvent
from .schemas import EventModel, EventResponse, EventsResponse

class EventViewControl:

  def post(self, event:EventModel):
    response = EventResponse()
    response.badrequest()
    response.data = TahuraEvent.addEvent(event)
    response.created()
    return response

  def get(self):
    response = EventsResponse()
    response.badrequest()
    response.data = TahuraEvent.getEvent()
    response.success()
    return response

  def getSingle(self, id):
    response = EventResponse()
    response.notfound()
    event = TahuraEvent.getEventBy(TahuraEvent.id_event==id)
    if event is not None:
      response.data=event
      response.success()
    return response

  def update(self, event: EventModel,id):
    response = EventResponse()
    response.notfound()
    event = TahuraEvent.update(event, id)
    if event is not None:
      response.data = event
      response.success()
    return response

  def delete(self, id):
    response = EventResponse()
    response.notfound()
    event = TahuraEvent.delete(id)
    if event == True:
      response.success()
      response.message="success delete data"
    return response