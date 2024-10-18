import pandas as pd
from datetime import datetime as dt

    
class Event: 

    def __init__(self ,name , place  , date  , time ):

        self.name = name
        self.date = date
        self.time = time
        self.place = place
         
class Agenda: 

    def __init__(self):
        self.events = []

    def add_event(self,name,place,date,time):
        event = Event(name,place,date,time)
        self.events.append(event)

    def display_events(self):
        if len(self.events) == 0:
            return f"Daha etkinlik eklenmedi"
        else:
            data = {"ID": list(range(1,len(self.events) + 1)),
                "Name": [event.name for event in self.events],
                "Place": [event.place for event in self.events],
                "Date": [event.date for event in self.events],
                "Time": [event.time for event in self.events] }
            
            event_df = pd.DataFrame(data)
            print(event_df.to_string(index= False))

    def search_event(self, id, display=True):
        if 1 <= id <= len(self.events):  # ID'yi dinamik olarak liste uzunluğu üzerinden kontrol ediyoruz
            event = self.events[id - 1]  # Liste index'i 0'dan başladığı için ID - 1
            if display:
                print(f"Event Found: ID: {id}, Name: {event.name}, Place: {event.place}, Date: {event.date}, Time: {event.time}")
            return event
        else:
            if display:
                print(f"No event found with ID: {id}")
            return None


    
    def delete_event(self, id):
        if 1 <= id <= len(self.events):
            del self.events[id - 1]  # Liste index'i üzerinden silme işlemi yapıyoruz
            print(f"Etkinlik silindi: {id}")
        else:
            print(f"No event found with ID: {id}")



    def update_event(self, id, new_name=None, new_place=None, new_date=None, new_time=None):
        event = self.search_event(id,display= False)
        if event:
            if new_name:
                event.name = new_name
            if new_place:
                event.place = new_place
            if new_date:
                event.date = new_date
            if new_time:
                event.time = new_time
            

            print(f"Event with ID {id} has been updated.")
            self.search_event(id)
        else:
            print(f"No event found with ID {id}")

    def today_events(self, start=None, end=None, display=True):
        
        today = dt.today()

        start = dt.strptime(start, "%d-%m-%Y") if start else today
        end = dt.strptime(end, "%d-%m-%Y") if end else start

        upcoming = []

        for event in self.events:
            event_date = dt.strptime(event.date, "%d-%m-%Y")
            if start <= event_date <= end:
                upcoming.append(event)
                if display:
                    print(f"Bugün {event.place}'da {event.time} saatinde {event.name} etkinliğiniz vardır!!")

        if not upcoming and display:
            print("Belirttiğiniz tarihlerde hiçbir etkinliğiniz bulunmamaktadır!!")

        return upcoming if upcoming else None

