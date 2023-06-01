class ReportWriter:
    def __init__(self, appInfo, *analyzers):

        self.analyzers = analyzers[0]
        self.appInfo = appInfo
