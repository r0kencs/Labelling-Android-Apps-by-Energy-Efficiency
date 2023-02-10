from Analyzer import Analyzer

class Earmo(Analyzer):
    def __init__(self, path):
        super().__init__(path)

    def analyze(self):
        print("Earmo analyzing...")
