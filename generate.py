# Re-import necessary modules after code execution environment reset
import pandas as pd
import random
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Generate marks data such that each student takes exactly 5 out of 8 subjects
marks_data = []

for student_id in range(1, 101):
    subject_ids = random.sample(range(1, 9), 5)  # Pick 5 unique subjects for each student
    for subject_id in subject_ids:
        mark = random.randint(40, 100)
        marks_data.append({"student_id": student_id, "subject_id": subject_id, "marks": mark})

# Create DataFrame
marks_fixed = pd.DataFrame(marks_data)

# Save to CSV
marks_fixed_path = "marks_fixed.csv"
marks_fixed.to_csv(marks_fixed_path, index=False)

marks_fixed_path
