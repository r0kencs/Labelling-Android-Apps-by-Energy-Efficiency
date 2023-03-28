import polars as pl

class Stats:
    def __init__(self):
        self.fdf = pl.read_csv("results.csv")

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

        final_df = pl.concat([self.fdf, df])
        final_df = final_df.unique(subset="App", keep="last")

        final_df.write_csv("results.csv")
