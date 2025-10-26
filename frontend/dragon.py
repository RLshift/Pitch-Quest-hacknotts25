class Dragon: 
    def __init__(self):
        self.health = 60
        self.alive = True
    
    def getHealth(self):
        return self.health
    
    def redHealth(self, reduce):
        self.health -= reduce
    
    def checkAlive(self):
        if self.health == 0:
            self.alive = False

