from datetime import datetime
from pymongo import MongoClient

class CoreRiderService(object):

    def __init__(self):
        client = MongoClient('localhost:27017')
        self.db = client.shadowfax

    def get_riders(self,scheduled_time):
        scheduled_time=datetime.strptime(scheduled_time,"%Y-%m-%d %H:%M:%S")
        time=scheduled_time.strftime('%m/ %d/%Y  %H:%M').lstrip("0").replace(" 0", "")

        uniqueriderid=[]
        response=[]
        for rider in self.db.rider_location.find({"update_timestamp" : time }):
            if rider['rider_id'] not in uniqueriderid:
                uniqueriderid.append(rider['rider_id'])
                response.append(rider)
        return response
    
if __name__ == "__main__":
    riderservice=CoreRiderService()
    for rider in riderservice.get_riders("2016-04-03 05:01:45"):
        print (rider)
    
