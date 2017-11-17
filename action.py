

class Action:
    element = ""
    utility = 0

    def __init__(self,word):
        self.element=word

    def normalize(self,max):
        self.utility=(max-self.utility)/max
