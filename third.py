class SingleResult():

    def __init__(self, resultNumber, listOfFails, resultDate):
        self.listOfFails = listOfFails
        self.resultNumber = resultNumber
        self.resultDate = resultDate


class ListofResults():

    def __init__(self):
        self.ResultsList = []

    def AddResulttoList(self, SingleResultsList):
        self.ResultsList.append(SingleResultsList)

    def __len__(self):
        return len(self.ResultsList)