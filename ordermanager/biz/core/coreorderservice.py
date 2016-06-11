from pymongo import MongoClient

class CoreOrderService():

    def __init__(self):
        client = MongoClient('localhost:27017')
        self.db = client.shadowfax

    def get_order(self,order_id):
        return self.db.order_data.find_one({"order_id":order_id})

    def update_order(self,data):
        self.db.order_data.save(data)

    def get_all_orders(self):
        return self.db.order_data.find()
