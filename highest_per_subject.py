import pandas as pd

students = pd.read_csv("students.csv")
classes = pd.read_csv("classes.csv")
marks = pd.read_csv("marks.csv")

# Merging classes with marks
df = pd.merge(classes, marks, left_on='id', right_on='student_id')

# Grouping by subject and taking max
max_per_subject = df.groupby('subject')['marks'].max().reset_index()
print(max_per_subject.sort_values('marks'))

