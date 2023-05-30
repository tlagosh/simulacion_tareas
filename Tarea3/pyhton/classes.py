
class Checkout:
    def __init__(self, u):
        self.u = u
        self.bussy = False
        self.client = None
    
class Client:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.departure_time = 0
        self.queue_time = 0