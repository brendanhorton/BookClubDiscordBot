class MemberList:
    def __init__(self):
        self.memberCollection = {}

    def populateList(self, memberList):
        self.memberCollection = memberList

    def getMembers(self):
        for member in self.memberCollection:
            print(f"{member} is {self.memberCollection[member]}")

    def markFinished(self, member):
        self.memberCollection[member] = 'finished'

    def checkFinished(self, member):
        if self.memberCollection[member] == 'finished':
            return True
        return False

    def reset(self):
        for member in self.memberCollection:
            self.memberCollection[member] = 'unfinished'

    def checkAll(self):
        for member in self.memberCollection:
            if self.memberCollection[member] == 'unfinished':
                return False
        
        return True
    
     