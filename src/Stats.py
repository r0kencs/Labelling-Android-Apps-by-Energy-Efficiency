import polars as pl

class Stats:
    #def __init__(self):

    def addData(self, data):
        df = pl.DataFrame(
            {
                "App": [data["appName"]],
                "Time": [data["time"]],
                "EARMO": [data["earmo"]],
                "Kadabra": [data["kadabra"]],
                "Activities": [data["activities"]],
                "Permissions": [data["permissions"]],
                "Services": [data["services"]],
                "Providers": [data["providers"]]
            }
        )

        df.write_csv("results.csv")
