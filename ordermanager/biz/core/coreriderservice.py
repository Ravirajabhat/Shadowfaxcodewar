from datetime import datetime
from pymongo import MongoClient

class CoreRiderService(object):

    def __init__(self):
        client = MongoClient('localhost:27017')
        self.db = client.shadowfax

    def get_riders(self,scheduled_time):
        scheduled_time=datetime.strptime(scheduled_time,"%Y-%m-%d %H:%M:%S")
        uniqueriderid=[]
        response=[]
        for rider in self.db.rider_location.find({"create_timestamp" : { "$gte": str(scheduled_time) } } ):
            if rider['rider_id'] not in uniqueriderid:
                uniqueriderid.append(rider['rider_id'])
                response.append(rider)
        return response

    def get_riders(self,scheduled_time,cluster_id):
        scheduled_time=datetime.strptime(scheduled_time,"%Y-%m-%d %H:%M:%S")
        uniqueriderid=[]
        response=[]
        ridersInthisclusters=self.db.rider_data.distinct("rider_id",{"clusters":cluster_id})
        
        for rider in self.db.rider_location.find({"$and":[{"rider_id":{"$in":ridersInthisclusters}},{"create_timestamp" : { "$gte": str(scheduled_time) } }] }):
            if rider['rider_id'] not in uniqueriderid:
                uniqueriderid.append(rider['rider_id'])
                response.append(rider)
        return response

    def populate_riders(self):
        for distinctriderid in self.db.rider_location.distinct("rider_id"):
            rider={}
            rider["rider_id"]=distinctriderid
            rider["clusters"]=self.db.order_data.distinct("cluster_id",{"rider_id":distinctriderid})
            self.db.rider_data.insert(rider)

    def compute_riderlocation(self):
        for rider_location in self.db.rider_location.find():
            self.db.rider_location.save(rider_location)
            
            
    
if __name__ == "__main__":
##    riderservice=CoreRiderService()
##    for rider in riderservice.get_riders("2016-04-08 08:24:05"):
##        print (rider)
    riderservice=CoreRiderService()
    riderservice.populate_riders()
    print("done")
    
