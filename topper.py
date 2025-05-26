import pandas as pd

students = pd.read_csv("students.csv")
classes = pd.read_csv("classes.csv")
marks = pd.read_csv("marks.csv")

# Merging students with marks
df = pd.merge(students, marks, left_on='id', right_on='student_id')

# Grouping by name and summing up the marks for each student
students_total_marks = df.groupby('name')['marks'].sum().reset_index()
print(students_total_marks.sort_values('marks'))

# Finding out the topper based on total marks
topper = students_total_marks.loc[students_total_marks['marks'].idxmax()]

print(topper)