import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

# Define quarters
quarters = ['fa24', 'sp25', 'wi25']
quarter_labels = {'fa24': 'Fall 2024', 'sp25': 'Spring 2025', 'wi25': 'Winter 2025'}

def get_courses_in_quarter(quarter):
    """Get all courses available in a quarter"""
    courses = set()
    for division in ['lower_division', 'upper_division']:
        path = Path(quarter) / division
        if path.exists():
            for file in path.glob('DSC_*.csv'):
                # Extract course name without extension
                course = file.stem
                courses.add(course)
    return courses

def get_final_enrollment_data(quarter, course):
    """Get the last row of enrollment data for a course in a quarter"""
    for division in ['lower_division', 'upper_division']:
        file_path = Path(quarter) / division / f"{course}.csv"
        if file_path.exists():
            df = pd.read_csv(file_path)
            if len(df) > 0:
                last_row = df.iloc[-1]
                return {
                    'enrolled': last_row['enrolled'],
                    'available': last_row['available'],
                    'waitlisted': last_row['waitlisted'],
                    'total': last_row['total'],
                    'time': last_row['time']
                }
    return None

# Find courses shared across all three quarters
print("Finding shared courses across all quarters...")
print("=" * 60)

quarter_courses = {}
for quarter in quarters:
    quarter_courses[quarter] = get_courses_in_quarter(quarter)
    print(f"{quarter_labels[quarter]}: {len(quarter_courses[quarter])} courses")

# Find intersection
shared_courses = quarter_courses['fa24'] & quarter_courses['sp25'] & quarter_courses['wi25']
shared_courses = sorted(list(shared_courses))

print(f"\nShared across all 3 quarters: {len(shared_courses)} courses")
print("Shared courses:", ', '.join(shared_courses))
print("=" * 60)

# Collect final enrollment data for all shared courses
enrollment_data = []

for course in shared_courses:
    for quarter in quarters:
        data = get_final_enrollment_data(quarter, course)
        if data:
            enrollment_data.append({
                'course': course,
                'quarter': quarter,
                'quarter_label': quarter_labels[quarter],
                **data
            })

# Create DataFrame
df = pd.DataFrame(enrollment_data)

# Add calculated columns
df['utilization_rate'] = (df['enrolled'] / df['total'] * 100).round(2)
df['waitlist_rate'] = (df['waitlisted'] / df['total'] * 100).round(2)
df['available_rate'] = (df['available'] / df['total'] * 100).round(2)

# Save summary data
df.to_csv('enrollment_comparison.csv', index=False)
print("\n✓ Saved enrollment comparison data to 'enrollment_comparison.csv'")

# Display summary statistics
print("\n" + "=" * 60)
print("ENROLLMENT SUMMARY BY COURSE")
print("=" * 60)
for course in shared_courses:
    course_data = df[df['course'] == course]
    print(f"\n{course}:")
    print(f"  {'Quarter':<15} {'Enrolled':>8} {'Waitlist':>8} {'Available':>9} {'Total':>7} {'Util%':>7}")
    print(f"  {'-'*15} {'-'*8} {'-'*8} {'-'*9} {'-'*7} {'-'*7}")
    for _, row in course_data.iterrows():
        print(f"  {row['quarter_label']:<15} {row['enrolled']:>8.0f} {row['waitlisted']:>8.0f} {row['available']:>9.0f} {row['total']:>7.0f} {row['utilization_rate']:>6.1f}%")

print("\n" + "=" * 60)
print("Analysis complete! Now generating visualizations...")
print("=" * 60)

