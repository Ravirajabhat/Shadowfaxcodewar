from core.coreorderservice import *
from core.coreriderservice import *
from core.coregeolocationservice import *

class BizOrderService(object):
    
    def __init__(self):
        self.geolocationservice=CoreGeoLocationService()
        self.coreorderservice=CoreOrderService()
        self.coreriderservice=CoreRiderService()

    def compute_distancematrix(self):
        count =0
        apiHitCount=0
        for orders in list(self.coreorderservice.get_all_orders()):
            count+=1
            if 'transit_distancemetrix' not in orders.keys():
                transit_distencemetrix = self.geolocationservice.get_distancematrix(orders['pickup_latitude'],orders['pickup_longitude'],orders['delivered_latitude'],orders['delivered_longitude'])
                orders['transit_distancemetrix']= transit_distencemetrix
                apiHitCount+=1
            riders_distencemetrix=[]
              
            if orders['scheduled_time'] is not None and "riders_distancemetrix" not in orders.keys():
                avalilable_riders = self.coreriderservice.get_riders(orders['scheduled_time'],orders['cluster_id'])
                print ("avalilable "+str(len(avalilable_riders)) +" in cluster " + str(orders['cluster_id']))
                for rider in avalilable_riders:
                    rider_distencemetrix = self.geolocationservice.get_distancematrix(orders['pickup_latitude'],orders['pickup_longitude'],rider['latitude'],rider['longitude'])
                    rider_distencemetrix['availabe_rider_id']=rider['rider_id']
                    riders_distencemetrix.append(rider_distencemetrix)
                    apiHitCount+=1
                orders['riders_distancemetrix'] = riders_distencemetrix
            
            self.coreorderservice.update_order(orders)
            print (str(count) + " : "+ str(apiHitCount))
            if count == 500 :
                break
             
if __name__ == "__main__":
    bizorderservice=BizOrderService()
    bizorderservice.compute_distancematrix()


