import polars as pl

class Stats:
    def __init__(self):
        self.fdf = pl.read_csv("results.csv")

    def addData(self, data):

        print(self.fdf)

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

        print(df)

        filtered = self.fdf.filter(pl.col("App") == data["appName"])

        if (filtered.is_empty()):
            final_df = pl.concat([self.fdf, df])
        else:
            final_df = df.join(self.fdf, on="App", how="left")

        print(final_df)

        #df.write_csv("results.csv")
