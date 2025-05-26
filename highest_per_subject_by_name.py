import pandas as pd

students = pd.read_csv("students.csv")
classes = pd.read_csv("classes.csv")
marks = pd.read_csv("marks.csv")

# Merging classes with marks
df = pd.merge(classes, marks, left_on='id', right_on='student_id')

# merge with students
df = pd.merge(df, students, left_on='id', right_on='id')

idx = df.groupby('subject')['marks'].idxmax()

result = df.loc[idx][['subject', 'marks', 'name']]

print(result)

