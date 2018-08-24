import pandas as pd
csv_file = 'question_correct_rate.csv'
df = pd.read_csv(csv_file, header=0, index_col='id')
scores = df['correct_rate']
df['correct_rate'] = (scores - scores.mean())
series = df['correct_rate']
missing_indices = list(set(range(1, 151)) - set(series.index))
series = series.append(pd.Series([0], index = missing_indices))
series = series / series.std() + 1
series = series.sort_index()
series.to_csv("updated_scores.csv")