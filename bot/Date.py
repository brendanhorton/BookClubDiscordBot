import datetime

class Date:
    def __init__(self):
        self.date = datetime.datetime.now()

    def updateDate(self):
        self.date = datetime.datetime.now()
        
    def getDate(self):
        return self.date

    def getMonth(self):
        return self.date.strftime("%B")

    def getDay(self):
        return self.date.day