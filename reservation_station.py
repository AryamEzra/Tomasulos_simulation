class ReservationStation:
    def __init__(self, station_type, id):
        self.type = station_type  
        self.id = id              
        self.busy = False         
        self.op = None            
        self.dest = None          
        self.src1 = None          
        self.src2 = None          
        
        

def init_reservation_stations():
    reservation_stations = {"Add": [], "Mul": []}
    for i in range(3):  
        reservation_stations["Add"].append(ReservationStation("Add", i))
    for i in range(2):  
        reservation_stations["Mul"].append(ReservationStation("Mul", i))
    
    return reservation_stations