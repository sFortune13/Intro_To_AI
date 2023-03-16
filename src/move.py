

class Move:

    def __init__(self, intial, final):
        
        # inital and final are Squares
        self.initial = intial
        self.final = final

    
    def __eq__(self, other):
        
        return self.initial == other.initial and self.final == other.final