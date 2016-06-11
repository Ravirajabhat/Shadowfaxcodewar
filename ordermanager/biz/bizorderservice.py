from core.coreorderservice import *
from core.coreriderservice import *
from core.coregeolocationservice import *

class BizOrderService(object):
    def __init__(self):
        self.geolocationservice=CoreGeoLocationService()
        self.coreorderservice=CoreOrderService()
        self.coreriderservice=CoreRiderService()

    def compute_distancematrix(self):
        for orders in self.coreorderservice.get_all_orders():
            transit_distencemetrix = destself.geolocationservice.get_distancematrix(orders['pickup_latitude'],orders['pickup_latitude'],orders['delivered_latitude'],orders['delivered_longitude'])
            orders['transit_distencemetrix']= transit_distencemetrix
            avalilable_riders = self.coreriderservice.get_riders(orders['scheduled_time'])
            for rider in avalilable_riders:
                
    
if __name__ == "__main__":
    bizorderservice=BizOrderService()
    bizorderservice.compute_distancematrix()
    print ( bizorderservice.get_distancematrix(12.9059519782,77.5855685771,12.88468,77.582))

