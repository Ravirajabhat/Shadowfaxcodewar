import json
import requests

class CoreGeoLocationService(object):

    def __init__(self):
        self.APIKEY = 'AIzaSyD-YMs3upLuvzOz1mQ9cODJ-5wTwQ6eVMo'    

    def get_distancematrix(self,source_latitude,source_longitude,destination_latitude,destination_longitude):
        origins='origins='+str(source_latitude)+','+str(source_longitude)
        destinations='destinations='+str(destination_latitude)+','+str(destination_longitude)
        url= 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'+origins+'&'+destinations+'&'+self.APIKEY 
        apiResponse = requests.get(url).json()
        print (apiResponse)
        response={}
        response['distance']=(apiResponse.get('rows'))[0]['elements'][0]['distance']['value'] #in meeters
        response['duration']=(apiResponse.get('rows'))[0]['elements'][0]['duration']['value'] #in secounds
        return response
    
if __name__ == "__main__":
    geolocationservice=CoreGeoLocationService()
    print ( geolocationservice.get_distancematrix(12.9059519782,77.5855685771,12.88468,77.582))
