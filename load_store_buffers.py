class LoadStoreBuffer:
    def __init__(self, type, id):
        self.type = type    
        self.id = id        
        self.busy = False   
        self.address = None 

def init_load_store_buffers():
    load_buffers = [LoadStoreBuffer("Load", i) for i in range(3)]
    store_buffers = [LoadStoreBuffer("Store", i) for i in range(1)]
    return load_buffers, store_buffers