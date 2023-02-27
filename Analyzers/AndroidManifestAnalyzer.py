from Analyzers.Analyzer import Analyzer

from xml.dom.minidom import parse, parseString

class AndroidManifestAnalyzer(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)


    def analyze(self):
        permissions = []
        activities = []
        services = []
        providers = []

        with open(self.path + "app/src/main/AndroidManifest.xml") as file:
            document = parse(file)

            nodes = document.getElementsByTagName('uses-permission')
            for node in nodes:
                permissions.append(node.getAttribute("android:name"))

            nodes = document.getElementsByTagName('activity')
            for node in nodes:
                activities.append(node.getAttribute("android:name"))

            nodes = document.getElementsByTagName('service')
            for node in nodes:
                services.append(node.getAttribute("android:name"))

            nodes = document.getElementsByTagName('provider')
            for node in nodes:
                providers.append(node.getAttribute("android:name"))
