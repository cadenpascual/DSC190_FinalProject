import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------
df = pd.read_csv("enrollment_comparison_partial.csv")

# ------------------------------------------------------------
# Sort courses and quarters for consistent display
# ------------------------------------------------------------
def extract_course_num(course):
    match = re.search(r'(\d+)([A-Za-z]*)', course)
    if match:
        num = int(match.group(1))
        suffix = match.group(2)
        return (num, suffix)
    return (0, '')

df['course'] = pd.Categorical(
    df['course'],
    categories=sorted(df['course'].unique(), key=lambda x: extract_course_num(x)),
    ordered=True
)

quarter_order = ['Fall 2024', 'Winter 2025', 'Spring 2025']
df['quarter_label'] = pd.Categorical(df['quarter_label'], categories=quarter_order, ordered=True)

# ------------------------------------------------------------
# Define color palettes
# ------------------------------------------------------------
colors = {
    'enrolled': '#2ecc71',
    'available': '#95a5a6',
    'waitlisted': '#e74c3c'
}

quarter_colors = {
    'Fall 2024': '#e67e22',
    'Winter 2025': '#9b59b6',
    'Spring 2025': '#3498db'
}

sns.set_style("whitegrid")

# ============================================================
# 1️⃣ Enrollment Distribution (Stacked)
# ============================================================
x_labels = sorted(df['course'].unique(), key=lambda x: extract_course_num(x))
x_positions = np.arange(len(x_labels))
width = 0.25

for i, quarter in enumerate(quarter_order):
    qdata = df[df['quarter_label'] == quarter].sort_values('course')
    if qdata.empty:
        continue

    # Match bar positions to where the course actually exists
    pos_map = [x_positions[x_labels.index(c)] for c in qdata['course']]
    enrolled = qdata['enrolled'].values
    available = qdata['available'].values
    waitlisted = qdata['waitlisted'].values

    plt.bar(np.array(pos_map) + (i - 1) * width, enrolled, width,
            color=quarter_colors[quarter], alpha=0.8, label=f'{quarter} - Enrolled')
    plt.bar(np.array(pos_map) + (i - 1) * width, available, width,
            bottom=enrolled, color='gray', alpha=0.4, label=f'{quarter} - Available')
    plt.bar(np.array(pos_map) + (i - 1) * width, waitlisted, width,
            bottom=enrolled + available, color='red', alpha=0.5, label=f'{quarter} - Waitlist')


plt.xlabel('Course', fontsize=13, fontweight='bold')
plt.ylabel('Number of Students', fontsize=13, fontweight='bold')
plt.title('Enrollment Distribution for Partially Offered Courses', fontsize=15, fontweight='bold')
plt.xticks(x_positions, x_labels, rotation=45, ha='right')
handles, labels = plt.gca().get_legend_handles_labels()
unique = dict(zip(labels, handles))
plt.legend(unique.values(), unique.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('partial_enrollment_distribution.png', dpi=300)
plt.close()
print("✓ Saved: partial_enrollment_distribution.png")


# ============================================================
# 2️⃣ Utilization Rate Comparison
# ============================================================
plt.figure(figsize=(14, 8))
sns.barplot(data=df, x='course', y='utilization_rate', hue='quarter_label', palette=quarter_colors)
plt.axhline(100, color='red', linestyle='--', linewidth=1.5, label='Full Capacity')
plt.title('Utilization Rates for Partially Offered Courses', fontsize=15, fontweight='bold')
plt.ylabel('Utilization (%)', fontsize=13)
plt.xlabel('Course', fontsize=13)
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('partial_utilization_rates.png', dpi=300)
plt.close()
print("✓ Saved: partial_utilization_rates.png")

# ============================================================
# 3️⃣ Faceted View: Enrollment Breakdown per Course
# ============================================================
unique_courses = df['course'].unique()
n = len(unique_courses)
cols = 3
rows = int(np.ceil(n / cols))

fig, axes = plt.subplots(rows, cols, figsize=(18, 12))
axes = axes.flatten()

for idx, course in enumerate(unique_courses):
    cdata = df[df['course'] == course].sort_values('quarter_label')
    ax = axes[idx]
    ax.bar(cdata['quarter_label'], cdata['enrolled'], color=colors['enrolled'], label='Enrolled', alpha=0.8)
    ax.bar(cdata['quarter_label'], cdata['available'], bottom=cdata['enrolled'],
           color=colors['available'], label='Available', alpha=0.8)
    ax.bar(cdata['quarter_label'], cdata['waitlisted'],
           bottom=cdata['enrolled'] + cdata['available'], color=colors['waitlisted'], alpha=0.8)
    ax.set_title(course, fontsize=11, fontweight='bold')
    ax.set_ylim(0, max(df['total']) * 1.1)
    ax.grid(axis='y', alpha=0.3)
    if idx == 0:
        ax.legend(fontsize=9)
for j in range(idx + 1, len(axes)):
    axes[j].axis('off')
fig.suptitle('Enrollment Composition by Course (Partial Offerings)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('partial_faceted_courses.png', dpi=300)
plt.close()
print("✓ Saved: partial_faceted_courses.png")

# ============================================================
# 4️⃣ Heatmap of Utilization
# ============================================================
pivot = df.pivot(index='course', columns='quarter_label', values='utilization_rate')
plt.figure(figsize=(10, 8))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlGnBu', linewidths=0.5, cbar_kws={'label': 'Utilization (%)'})
plt.title('Utilization Heatmap – Partially Offered Courses', fontsize=15, fontweight='bold')
plt.xlabel('Quarter')
plt.ylabel('Course')
plt.tight_layout()
plt.savefig('partial_utilization_heatmap.png', dpi=300)
plt.close()
print("✓ Saved: partial_utilization_heatmap.png")

# ============================================================
# 5️⃣ Average Utilization Summary Plot
# ============================================================
plt.figure(figsize=(10, 6))
avg_util = df.groupby('quarter_label')['utilization_rate'].mean().reset_index()
sns.barplot(data=avg_util, x='quarter_label', y='utilization_rate', palette=quarter_colors)
plt.title('Average Utilization Across Quarters (Partial Courses)', fontsize=15, fontweight='bold')
plt.ylabel('Average Utilization (%)')
plt.xlabel('Quarter')
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('partial_avg_utilization.png', dpi=300)
plt.close()
print("✓ Saved: partial_avg_utilization.png")

print("\n✅ All partial-course visualizations complete!")
