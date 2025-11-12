import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from pathlib import Path
import re

# ------------------------------------------------------------
# Helper Function: Extract numeric and optional letter suffix
# ------------------------------------------------------------
def extract_course_num(course):
    """Extract numeric and optional letter suffix from course code like DSC_40A or DSC_106."""
    match = re.search(r'(\d+)([A-Za-z]*)', course)
    if match:
        num = int(match.group(1))
        suffix = match.group(2)
        return (num, suffix)
    return (0, '')

# ------------------------------------------------------------
# Visualization Style (for later plots if needed)
# ------------------------------------------------------------
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

# ------------------------------------------------------------
# Quarters Configuration
# ------------------------------------------------------------
quarters = ['fa24', 'sp25', 'wi25']
quarter_labels = {'fa24': 'Fall 2024', 'sp25': 'Spring 2025', 'wi25': 'Winter 2025'}

# ------------------------------------------------------------
# Get Courses and Enrollment Data
# ------------------------------------------------------------
def get_courses_in_quarter(quarter):
    """Get all courses available in a quarter."""
    courses = set()
    for division in ['lower_division', 'upper_division']:
        path = Path("webreg_data") / quarter / division
        if path.exists():
            for file in path.glob('DSC_*.csv'):
                course = file.stem
                courses.add(course)
    return courses

def get_final_enrollment_data(quarter, course):
    """Get the last row of enrollment data for a course in a quarter."""
    for division in ['lower_division', 'upper_division']:
        file_path = Path("webreg_data") / quarter / division / f"{course}.csv"
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

# ------------------------------------------------------------
# Step 1: Identify Course Offerings Across Quarters
# ------------------------------------------------------------
print("Finding shared and partial courses across all quarters...")
print("=" * 60)

quarter_courses = {}
for quarter in quarters:
    quarter_courses[quarter] = get_courses_in_quarter(quarter)
    print(f"{quarter_labels[quarter]}: {len(quarter_courses[quarter])} courses")

# Shared and partial sets
shared_courses = quarter_courses['fa24'] & quarter_courses['sp25'] & quarter_courses['wi25']
all_courses = set.union(*quarter_courses.values())
partial_courses = all_courses - shared_courses

print(f"\nShared across all 3 quarters: {len(shared_courses)} courses")
print(f"Partial (offered in 1–2 quarters): {len(partial_courses)} courses")
print("=" * 60)

# ------------------------------------------------------------
# Step 2: Collect Data Helper
# ------------------------------------------------------------
def collect_enrollment_data(course_list, quarters):
    records = []
    for course in course_list:
        for quarter in quarters:
            data = get_final_enrollment_data(quarter, course)
            if data:
                records.append({
                    'course': course,
                    'quarter': quarter,
                    'quarter_label': quarter_labels[quarter],
                    **data
                })
    return pd.DataFrame(records)

# ------------------------------------------------------------
# Step 3A: Shared Courses Analysis
# ------------------------------------------------------------
shared_df = collect_enrollment_data(shared_courses, quarters)

if not shared_df.empty:
    shared_df['utilization_rate'] = (shared_df['enrolled'] / shared_df['total'] * 100).round(2)
    shared_df['waitlist_rate'] = (shared_df['waitlisted'] / shared_df['total'] * 100).round(2)
    shared_df['available_rate'] = (shared_df['available'] / shared_df['total'] * 100).round(2)

    shared_df['course'] = pd.Categorical(
        shared_df['course'],
        categories=sorted(shared_df['course'].unique(), key=lambda x: extract_course_num(x)),
        ordered=True
    )
    shared_df = shared_df.sort_values(['course', 'quarter'])

    shared_df.to_csv('enrollment_comparison_shared.csv', index=False)
    print("✓ Saved shared-course data to 'enrollment_comparison_shared.csv'")
else:
    print("⚠️ No shared courses found, skipping shared CSV export.")

# ------------------------------------------------------------
# Step 3B: Partial Courses Analysis
# ------------------------------------------------------------
partial_df = collect_enrollment_data(partial_courses, quarters)

if not partial_df.empty:
    partial_df['utilization_rate'] = (partial_df['enrolled'] / partial_df['total'] * 100).round(2)
    partial_df['waitlist_rate'] = (partial_df['waitlisted'] / partial_df['total'] * 100).round(2)
    partial_df['available_rate'] = (partial_df['available'] / partial_df['total'] * 100).round(2)

    partial_df['course'] = pd.Categorical(
        partial_df['course'],
        categories=sorted(partial_df['course'].unique(), key=lambda x: extract_course_num(x)),
        ordered=True
    )
    partial_df = partial_df.sort_values(['course', 'quarter'])

    partial_df.to_csv('enrollment_comparison_partial.csv', index=False)
    print("✓ Saved partial-course data to 'enrollment_comparison_partial.csv'")
else:
    print("⚠️ No partial courses found, skipping partial CSV export.")

# ------------------------------------------------------------
# Step 4: Summary Reporting
# ------------------------------------------------------------
def print_summary(df, label):
    print("\n" + "=" * 60)
    print(f"{label.upper()} COURSE SUMMARY")
    print("=" * 60)
    if df.empty:
        print("⚠️ No data available.")
        return

    for course in df['course'].unique():
        course_data = df[df['course'] == course]
        print(f"\n{course}:")
        print(f"  {'Quarter':<15} {'Enrolled':>8} {'Waitlist':>8} {'Avail':>8} {'Total':>7} {'Util%':>7}")
        print("  " + "-" * 60)
        for _, row in course_data.iterrows():
            print(f"  {row['quarter_label']:<15} {row['enrolled']:>8.0f} {row['waitlisted']:>8.0f} "
                  f"{row['available']:>8.0f} {row['total']:>7.0f} {row['utilization_rate']:>6.1f}%")

# Print both summaries
print_summary(shared_df, "Shared")
print_summary(partial_df, "Partial")

print("\n" + "=" * 60)
print("Analysis complete! Generated:")
print(" - enrollment_comparison_shared.csv (offered all 3 quarters)")
print(" - enrollment_comparison_partial.csv (offered in 1–2 quarters)")
print("=" * 60)
