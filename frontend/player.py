import random 

class Player: 

    def __init__(self):
        self.health = 6
        self.mult = 1
        self.shield = False
        self.potion = False
        self.combo = False
        self.usingShield = False

    def getHealth(self):
        return self.health

    def redHealth(self):
        self.health -= 1
    
    def fullHealth(self):
        self.health = 6

    def getShield(self):
        return self.shield
    
    def useShield(self):
        if(self.getShield()):
            self.shield = False
            self.usingShield = True
        else:
            return False
    
    def resetShield(self):
        self.usingShield = False

    def getPotion(self):
        return self.potion
    
    def usePotion(self):
        if(self.getPotion()):
            self.potion = False
            self.fullHealth()
        else:
            return False
        
    def getCombo(self):
        return self.combo
    
    def useCombo(self):
        if (self.getCombo()):
            self.combo = False
            self.mult = 2
        else:
            return False
        
    def resetCombo(self):
        self.mult = 1

    def getMult(self):
        return self.mult
    
    def newPowerUp(self):
        if (not(self.getCombo and self.getPotion and self.getShield)):
            while True:
                rand = random.randint(1, 3)
                if (rand == 1):
                    if not self.getCombo():
                        self.combo = True
                        return 
                elif (rand == 2):
                    if not self.getPotion():
                        self.potion = True
                        return 
                else:
                    if not self.getShield():
                        self.shield = True
                        return 
    
                
            


    