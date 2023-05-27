import polars as pl

class Stats:
    def __init__(self):
        self.fdf = pl.read_csv("results.csv")

    def addData(self, data):

        df = pl.DataFrame(
            {
                "App": [data["appName"]],
                "Category": [data["category"]],
                "Time": [data["time"]],
                "EARMO": [data["earmo"]],
                "Kadabra": [data["kadabra"]],
                "Lint": [data["lint"]],
                "ADoctor": [data["adoctor"]],
                "Paprika": [data["paprika"]],
                "Relda2": [data["relda2"]],
                "Activities": [data["activities"]],
                "Permissions": [data["permissions"]],
                "Services": [data["services"]],
                "Providers": [data["providers"]]
            }
        )

        if not self.fdf.is_empty():
            final_df = pl.concat([self.fdf, df])
            final_df = final_df.unique(subset="App", keep="last")
        else:
            final_df = df

        final_df.write_csv("results.csv")
