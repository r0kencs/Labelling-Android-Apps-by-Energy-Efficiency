class AppInfo():
    def __init__(self, name, categories, size, numberOfFiles):
        self.name = name
        self.categories = categories
        self.size = size
        self.numberOfFiles = numberOfFiles

    def getName(self):
        return self.name

    def getCategories(self):
        return self.categories

    def getSize(self):
        return self.size

    def getNumberOfFiles(self):
        return self.numberOfFiles

    def getTime(self):
        return self.time

    def setTime(self, time):
        self.time = time
