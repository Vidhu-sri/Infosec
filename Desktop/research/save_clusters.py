import pandas as pd
file = pd.read_csv(r"C:\Users\Lenovo\Desktop\cluster.csv")
file = file.drop(file.iloc[:,6:],axis=1)

from collections import defaultdict
final = defaultdict(list)
for col in set(file['label']):
    final[col] = [*file[file['label'] == col].iloc[:,0]]

print(final)
    