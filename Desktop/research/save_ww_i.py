import pandas as pd

file = pd.read_csv(r"C:\Users\Lenovo\Desktop\papers_to_review.csv")
file = file.drop(file.iloc[:,3:],axis=1)


ww = file[file['interest']=='WW']
i=file[file['interest'] == 'I']

file_path = r"C:\Users\Lenovo\Desktop\2nd_attempt.csv"
to_save = pd.concat([ww,i], axis=0)
to_save.to_csv(file_path)