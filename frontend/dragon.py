class Dragon: 
    def __init__(self):
        self.maxHealth = 60
        self.health = 60
        self.alive = True

    def getMaxHealth(self):
        return self.maxHealth
    
    def getHealth(self):
        return self.health
    
    def redHealth(self, reduce):
        self.health -= reduce
    
    def checkAlive(self):
        if self.health == 0:
            self.alive = False

