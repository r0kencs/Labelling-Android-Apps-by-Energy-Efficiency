import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import pearsonr

data = pd.read_csv("results.csv")

data.dropna()

data = data.drop(labels=["Name", "Category"], axis=1)

corr_mat = data.corr().round(2)

plt.figure(figsize=(20,16))
plot = sns.heatmap(corr_mat, annot=True)
plt.savefig("correlation_matrix.png")
