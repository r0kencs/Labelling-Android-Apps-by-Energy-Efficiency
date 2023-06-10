from src.Analyzers.Analyzer import Analyzer

from xml.dom.minidom import parse, parseString

class AndroidManifestAnalyzer(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.permissions = []
        self.activities = []
        self.services = []
        self.providers = []

    def analyze(self):
        permissions = []
        activities = []
        services = []
        providers = []

        with open(f"{self.path}resources/AndroidManifest.xml") as file:
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

        self.permissions = permissions
        self.activities = activities
        self.services = services
        self.providers = providers

        self.status = 1

    def toReport(self):
        return f"Permissions: {len(self.permissions)}\nActivities: {len(self.activities)}\nServices: {len(self.services)}\nProviders: {len(self.providers)}\n"

    def toJson(self):
        data = {
            "Permissions": len(self.permissions),
            "Activities": len(self.activities),
            "Services": len(self.services),
            "Providers": len(self.providers)
        }
        return data

    def getResult(self):
        data = {
            "activities": len(self.activities),
            "permissions": len(self.permissions),
            "services": len(self.services),
            "providers": len(self.providers)
        }

        return data
