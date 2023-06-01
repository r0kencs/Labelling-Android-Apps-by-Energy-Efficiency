from src.Reports.ReportWriter import ReportWriter

import json

class JsonReportWriter(ReportWriter):
    def __init__(self, appInfo, *analyzers):
        super().__init__(appInfo, analyzers)

    def write(self):
        report = open("output/" + self.appInfo.getName() + "/report.txt", "w")

        data = {
            "name": self.appInfo.getName(),
            "size": self.appInfo.getSize(),
            "category": self.appInfo.getCategory(),
            "time": self.appInfo.getTime()
        }

        for analyzer in self.analyzers:
            data.update(analyzer.toJson())

        report = open("output/" + self.appInfo.getName() + "/report.json", "w")
        report.write(json.dumps(data))
        report.close()
