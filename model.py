import polars as pl

df = pl.read_csv("results.csv")

categoryDfs = df.partition_by("Category")

for categoryDf in categoryDfs:
    categoryName = pl.first(categoryDf["Category"])
    apps = pl.count(categoryDf["App"])

    max = categoryDf.max()
    min = categoryDf.min()

    categoryDf.sort("EARMO")
    earmoSum = pl.sum(categoryDf.get_column("EARMO"))
    earmoMean = earmoSum / apps
    earmoMax = max.select(pl.col("EARMO")).item()
    earmoMin = min.select(pl.col("EARMO")).item()

    kadabraSum = pl.sum(categoryDf.get_column("Kadabra"))
    kadabraMean = kadabraSum / apps
    kadabraMax = max.select(pl.col("Kadabra")).item()
    kadabraMin = min.select(pl.col("Kadabra")).item()

    lintSum = pl.sum(categoryDf.get_column("Lint"))
    lintMean = lintSum / apps
    lintMax = max.select(pl.col("Lint")).item()
    lintMin = min.select(pl.col("Lint")).item()

    aDoctorSum = pl.sum(categoryDf.get_column("ADoctor"))
    aDoctorMean = aDoctorSum / apps
    aDoctorMax = max.select(pl.col("ADoctor")).item()
    aDoctorMin = min.select(pl.col("ADoctor")).item()

    paprikaSum = pl.sum(categoryDf.get_column("Paprika"))
    paprikaMean = paprikaSum / apps
    paprikaMax = max.select(pl.col("Paprika")).item()
    paprikaMin = min.select(pl.col("Paprika")).item()

    relda2Sum = pl.sum(categoryDf.get_column("Relda2"))
    relda2Mean = relda2Sum / apps
    relda2Max = max.select(pl.col("Relda2")).item()
    relda2Min = min.select(pl.col("Relda2")).item()


    print(f"\n-------------------- {categoryName} ----------------------")
    print(f"Apps: {apps}")
    print(f"Earmo - Sum: {earmoSum} Mean: {earmoMean:.2f} Max: {earmoMax} Min: {earmoMin}")
    print(f"Kadabra - Sum: {kadabraSum} Mean: {kadabraMean:.2f} Max: {kadabraMax} Min: {kadabraMin}")
    print(f"lintSum - Sum: {lintSum} Mean: {lintMean:.2f} Max: {lintMax} Min: {lintMin}")
    print(f"aDoctor - Sum: {aDoctorSum} Mean: {aDoctorMean:.2f} Max: {aDoctorMax} Min: {aDoctorMin}")
    print(f"Paprika - Sum: {paprikaSum} Mean: {paprikaMean:.2f} Max: {paprikaMax} Min: {paprikaMin}")
    print(f"relda2Sum - Sum: {relda2Sum} Mean: {relda2Mean:.2f} Max: {relda2Max} Min: {relda2Min}")
