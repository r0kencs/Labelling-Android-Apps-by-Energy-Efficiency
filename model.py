import polars as pl

df = pl.read_csv("results.csv")

categoryDfs = df.partition_by("Category")

for categoryDf in categoryDfs:
    categoryName = pl.first(categoryDf["Category"])
    apps = pl.count(categoryDf["App"])

    earmoSum = pl.sum(categoryDf.get_column("EARMO"))
    kadabraSum = pl.sum(categoryDf.get_column("Kadabra"))
    lintSum = pl.sum(categoryDf.get_column("Lint"))
    aDoctorSum = pl.sum(categoryDf.get_column("ADoctor"))
    paprikaSum = pl.sum(categoryDf.get_column("Paprika"))
    relda2Sum = pl.sum(categoryDf.get_column("Relda2"))

    print(f"Category: {categoryName}\t Apps: {apps}\t Earmo: {earmoSum}\t Kadabra: {kadabraSum}\t Lint: {lintSum}\t aDoctor: {aDoctorSum}\t Paprika: {paprikaSum}\t Relda2: {relda2Sum}")

    
