from src.Reports.ReportWriter import ReportWriter

class TextReportWriter(ReportWriter):
    def __init__(self, appInfo, *analyzers):
        super().__init__(appInfo, analyzers)

    def write(self):
        report = open("output/" + self.appInfo.getName() + "/report.txt", "w")

        report.write(f"Categories: {self.appInfo.getCategories()}\n")
        report.write(f"Size: {self.appInfo.getSize()} MB\n")
        report.write(f"Number of files: {self.appInfo.getNumberOfFiles()}\n")

        for analyzer in self.analyzers:
            report.write(analyzer.toReport())

        report.write(f"Analysis time: {self.appInfo.getTime():.2f} s\n")

        report.close()
