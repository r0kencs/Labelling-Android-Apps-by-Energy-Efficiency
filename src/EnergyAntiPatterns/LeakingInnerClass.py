from src.EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern

class LeakingInnerClass(EnergyAntiPattern):
    def __init__(self):
        super().__init__("LeakingInnerClass")
