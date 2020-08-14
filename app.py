import matplotlib.pyplot as plt
import pandas as pd
import re
df = pd.read_csv('assignment_solution.csv', parse_dates=True, index_col='Date')
print(df.head())
print(df.info())
score = df['Score Rating']

print(score.head())

fatima = df.loc[:, 'Score Rating'].resample('M').sum()

fatima.plot()
plt.show()