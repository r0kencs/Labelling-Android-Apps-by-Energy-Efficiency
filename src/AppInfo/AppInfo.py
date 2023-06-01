class AppInfo():
    def __init__(self, name, category, size, numberOfFiles):
        self.name = name
        self.category = category
        self.size = size
        self.numberOfFiles = numberOfFiles

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getSize(self):
        return self.size

    def getNumberOfFiles(self):
        return self.numberOfFiles

    def getTime(self):
        return self.time

    def setTime(self, time):
        self.time = time
