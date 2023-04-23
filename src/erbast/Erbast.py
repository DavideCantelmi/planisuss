import random

class Erbast:
    def __init__(self, energy, lifetime, social_attitude):
        if energy > 0:
            self.energy = energy
        else:
            self.energy = 0
        self.lifetime = lifetime #Days
        self.age = 0
        if social_attitude > 1:
            self.social_attitude = 1
        elif social_attitude < 0:
            self.social_attitude = 0
        else:
            self.social_attitude = social_attitude
        if energy > 0:
            self.living = True
        else:
            self.living = False

    def checkIfIsLiving(self):
        if self.age >= self.lifetime:
            self.living = False

    def fight(self, selection):
        #attack sarà una lista di attacchi
        attacks = ["attack1", "attack2", "attack3", "attack4"]

        prob = random.randint(0,1)

        if self.living:
            if prob == 1:
                if (attacks[selection] == "attack1"):
                    valueOfTheAttack = 10
                    return valueOfTheAttack
                elif (attacks[selection] == "attack2"):
                    valueOfTheAttack = 20
                    self.energy -= 2
                    return valueOfTheAttack
                elif (attacks[selection] == "attack3"):
                    valueOfTheAttack = 15
                    self.energy -= 1
                    return valueOfTheAttack
                elif (attacks[selection] == "attack4"):
                    valueOfTheAttack = 30
                    self.energy -= 10
                    return valueOfTheAttack
                self.checkIfIsLiving()
        else:
            print("Non puoi combattere perché il tuo erbast è morto")

    def takeDamange(self, valueOfTheAttack):
        self.energy -= valueOfTheAttack
        self.checkIfIsLiving()

    def move(self):
        if self.living:
            self.energy -= 1
            # temporaneamente diminuiamo l'energia di 1 ma è da considerare l'implementazione voluta dal prof del movimento.
            self.checkIfIsLiving()
        else:
            print("Non puoi muoverti perché il tuo erbast è morto")

    def graze(self):
        if self.living:
            self.energy +=1
        else:
            print("Non puoi pascolare perché il tuo erbast è morto")
