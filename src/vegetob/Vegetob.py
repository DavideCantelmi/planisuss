class Vegetob:
    def  __init__ (self, density):

        if density < 0:
            self.density = 0
        elif density > 100:
            self.density = 100
        else:
            self.density = density
