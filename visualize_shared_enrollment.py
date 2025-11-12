import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

def extract_course_num(course):
    match = re.search(r'(\d+)([A-Za-z]*)', course)
    if match:
        number = int(match.group(1))
        suffix = match.group(2)
        return (number, suffix)
    return (0, '')

# Load the data
df = pd.read_csv('enrollment_comparison_shared.csv')

# Ensure quarter order
quarter_order = ['Fall 2024', 'Winter 2025', 'Spring 2025']
df['quarter_label'] = pd.Categorical(df['quarter_label'], categories=quarter_order, ordered=True)

# Sort courses with unique, properly ordered categories
sorted_courses = sorted(df['course'].unique(), key=lambda x: extract_course_num(x))
course_order = sorted_courses
df['course'] = pd.Categorical(df['course'], categories=sorted_courses, ordered=True)


# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Define consistent colors
colors = {
    'enrolled': '#2ecc71',      # Green
    'waitlisted': '#e74c3c',    # Red
    'available': '#95a5a6',     # Gray
    'total': '#3498db'          # Blue
}

quarter_colors = {
    'Fall 2024': '#e67e22',     # Orange
    'Spring 2025': '#3498db',   # Blue
    'Winter 2025': '#9b59b6'    # Purple
}

print("Creating visualizations...")
print("=" * 60)

# ============================================================================
# VISUALIZATION 1: Stacked Bar Chart (Enrolled + Waitlisted) with Total Line
# ============================================================================
print("1. Creating stacked bar chart with capacity comparison...")

fig, ax = plt.subplots(figsize=(18, 10))

quarters = df['quarter_label'].unique()
x = np.arange(len(course_order))
width = 0.25

for i, quarter in enumerate(['Fall 2024', 'Spring 2025', 'Winter 2025']):
    quarter_data = df[df['quarter_label'] == quarter].sort_values('course')
    
    # Position for this quarter's bars
    positions = x + (i - 1) * width
    
    # Stacked bars: enrolled + waitlisted
    enrolled = quarter_data['enrolled'].values
    waitlisted = quarter_data['waitlisted'].values
    total = quarter_data['total'].values
    
    # Plot enrolled (bottom)
    ax.bar(positions, enrolled, width, label=f'{quarter} - Enrolled',
           color=quarter_colors[quarter], alpha=0.8)
    
    # Plot waitlisted (stacked on top of enrolled)
    ax.bar(positions, waitlisted, width, bottom=enrolled,
           color=quarter_colors[quarter], alpha=0.3, hatch='///')
    
    # Add total capacity markers
    ax.scatter(positions, total, color='black', marker='_', s=300, 
               linewidths=3, zorder=5, label=f'{quarter} - Total Capacity' if i == 0 else '')

ax.set_xlabel('Course', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold')
ax.set_title('DSC Course Enrollment Comparison Across Quarters\n(Solid = Enrolled, Hatched = Waitlisted, Black Line = Total Capacity)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(course_order, rotation=45, ha='right')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('enrollment_comparison_stacked.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: enrollment_comparison_stacked.png")
plt.close()

# ============================================================================
# VISUALIZATION 2: Utilization Rate Comparison (Percentage-based)
# ============================================================================
print("2. Creating utilization rate comparison...")

fig, ax = plt.subplots(figsize=(18, 10))

for i, quarter in enumerate(['Fall 2024', 'Spring 2025', 'Winter 2025']):
    quarter_data = df[df['quarter_label'] == quarter].sort_values('course')
    positions = x + (i - 1) * width
    
    ax.bar(positions, quarter_data['utilization_rate'].values, width,
           label=quarter, color=quarter_colors[quarter], alpha=0.8)

# Add 100% reference line
ax.axhline(y=100, color='red', linestyle='--', linewidth=2, alpha=0.5, label='100% Capacity')

ax.set_xlabel('Course', fontsize=14, fontweight='bold')
ax.set_ylabel('Utilization Rate (%)', fontsize=14, fontweight='bold')
ax.set_title('Course Utilization Rates by Quarter\n(Enrolled / Total Capacity × 100%)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(course_order, rotation=45, ha='right')
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, max(df['utilization_rate'].max() * 1.1, 110))

plt.tight_layout()
plt.savefig('enrollment_utilization_rates.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: enrollment_utilization_rates.png")
plt.close()

# ============================================================================
# VISUALIZATION 3: Proportional Stacked Bar (100% stacked)
# ============================================================================
print("3. Creating proportional stacked bar chart...")

fig, ax = plt.subplots(figsize=(18, 10))

for i, quarter in enumerate(['Fall 2024', 'Spring 2025', 'Winter 2025']):
    quarter_data = df[df['quarter_label'] == quarter].sort_values('course')
    positions = x + (i - 1) * width
    
    enrolled_pct = quarter_data['utilization_rate'].values
    waitlist_pct = quarter_data['waitlist_rate'].values
    available_pct = quarter_data['available_rate'].values
    
    # Stacked bars showing proportions
    ax.bar(positions, enrolled_pct, width, label=f'{quarter} - Enrolled' if i == 0 else '',
           color=colors['enrolled'], alpha=0.7 + i*0.1)
    ax.bar(positions, waitlist_pct, width, bottom=enrolled_pct,
           label=f'{quarter} - Waitlisted' if i == 0 else '',
           color=colors['waitlisted'], alpha=0.7 + i*0.1)
    ax.bar(positions, available_pct, width, 
           bottom=enrolled_pct + waitlist_pct,
           label=f'{quarter} - Available' if i == 0 else '',
           color=colors['available'], alpha=0.7 + i*0.1)

ax.set_xlabel('Course', fontsize=14, fontweight='bold')
ax.set_ylabel('Percentage of Total Capacity (%)', fontsize=14, fontweight='bold')
ax.set_title('Course Enrollment Distribution by Quarter\n(Proportional View: Enrolled + Waitlisted + Available = 100%)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(course_order, rotation=45, ha='right')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 105)

plt.tight_layout()
plt.savefig('enrollment_proportional.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: enrollment_proportional.png")
plt.close()

# ============================================================================
# VISUALIZATION 4: Faceted View (Individual Course Comparisons)
# ============================================================================
print("4. Creating faceted course-by-course comparison...")

n_courses = len(course_order)
n_cols = 4
n_rows = int(np.ceil(n_courses / n_cols))

fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 15))
axes = axes.flatten()

for idx, course in enumerate(course_order):
    ax = axes[idx]
    course_data = df[df['course'] == course].sort_values('quarter_label')
    
    quarters_list = course_data['quarter_label'].values
    x_pos = np.arange(len(quarters_list))
    
    # Create grouped bars for each metric
    width = 0.25
    ax.bar(x_pos - width, course_data['enrolled'].values, width, 
           label='Enrolled', color=colors['enrolled'], alpha=0.8)
    ax.bar(x_pos, course_data['waitlisted'].values, width,
           label='Waitlisted', color=colors['waitlisted'], alpha=0.8)
    ax.bar(x_pos + width, course_data['available'].values, width,
           label='Available', color=colors['available'], alpha=0.8)
    
    # Add total capacity line
    ax.plot(x_pos, course_data['total'].values, 'ko-', linewidth=2, 
            markersize=8, label='Total Capacity')
    
    ax.set_title(f'{course}', fontweight='bold', fontsize=11)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([q.split()[0] for q in quarters_list], fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylabel('Students', fontsize=9)
    
    if idx == 0:
        ax.legend(fontsize=8, loc='upper left')

# Hide empty subplots
for idx in range(n_courses, len(axes)):
    axes[idx].axis('off')

fig.suptitle('Individual Course Enrollment Patterns Across Quarters', 
             fontsize=18, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('enrollment_faceted.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: enrollment_faceted.png")
plt.close()

# ============================================================================
# VISUALIZATION 5: Heatmap of Utilization Rates
# ============================================================================
print("5. Creating heatmap of utilization rates...")

pivot_util = df.pivot(index='course', columns='quarter_label', values='utilization_rate')
pivot_util = pivot_util[['Fall 2024', 'Winter 2025', 'Spring 2025']]  # Order columns

fig, ax = plt.subplots(figsize=(10, 12))
sns.heatmap(pivot_util, annot=True, fmt='.1f', cmap='RdYlGn', center=75,
            vmin=0, vmax=100, cbar_kws={'label': 'Utilization Rate (%)'},
            linewidths=0.5, linecolor='white', ax=ax)
ax.set_title('Course Utilization Rate Heatmap\n(% of Total Capacity Filled)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
ax.set_ylabel('Course', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('enrollment_heatmap.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: enrollment_heatmap.png")
plt.close()

# ============================================================================
# VISUALIZATION 6: Comprehensive Multi-Metric Comparison
# ============================================================================
print("6. Creating comprehensive multi-metric dashboard...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.25)

# Top panel: Absolute numbers comparison
ax1 = fig.add_subplot(gs[0, :])
for i, quarter in enumerate(['Fall 2024', 'Spring 2025', 'Winter 2025']):
    quarter_data = df[df['quarter_label'] == quarter].sort_values('course')
    positions = x + (i - 1) * width
    
    enrolled = quarter_data['enrolled'].values
    waitlisted = quarter_data['waitlisted'].values
    
    ax1.bar(positions, enrolled, width, label=f'{quarter}',
            color=quarter_colors[quarter], alpha=0.8)
    ax1.bar(positions, waitlisted, width, bottom=enrolled,
            color=quarter_colors[quarter], alpha=0.3, hatch='///')
    
    # Total capacity markers
    ax1.scatter(positions, quarter_data['total'].values, color='black', 
                marker='_', s=200, linewidths=2, zorder=5)

ax1.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
ax1.set_title('Absolute Enrollment Numbers (Solid=Enrolled, Hatched=Waitlist, Line=Capacity)', 
              fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(course_order, rotation=45, ha='right')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(axis='y', alpha=0.3)

# Middle left: Utilization rates
ax2 = fig.add_subplot(gs[1, 0])
for i, quarter in enumerate(['Fall 2024', 'Spring 2025', 'Winter 2025']):
    quarter_data = df[df['quarter_label'] == quarter].sort_values('course')
    positions = x + (i - 1) * width
    ax2.bar(positions, quarter_data['utilization_rate'].values, width,
            label=quarter, color=quarter_colors[quarter], alpha=0.8)
ax2.axhline(y=100, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax2.set_ylabel('Utilization Rate (%)', fontsize=11, fontweight='bold')
ax2.set_title('Capacity Utilization by Course', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(course_order, rotation=45, ha='right', fontsize=9)
ax2.grid(axis='y', alpha=0.3)

# Middle right: Waitlist analysis
ax3 = fig.add_subplot(gs[1, 1])
for i, quarter in enumerate(['Fall 2024', 'Spring 2025', 'Winter 2025']):
    quarter_data = df[df['quarter_label'] == quarter].sort_values('course')
    positions = x + (i - 1) * width
    ax3.bar(positions, quarter_data['waitlisted'].values, width,
            label=quarter, color=quarter_colors[quarter], alpha=0.8)
ax3.set_ylabel('Waitlisted Students', fontsize=11, fontweight='bold')
ax3.set_title('Waitlist Size by Course', fontsize=12, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(course_order, rotation=45, ha='right', fontsize=9)
ax3.grid(axis='y', alpha=0.3)

# Bottom left: Total capacity comparison
ax4 = fig.add_subplot(gs[2, 0])
for i, quarter in enumerate(['Fall 2024', 'Spring 2025', 'Winter 2025']):
    quarter_data = df[df['quarter_label'] == quarter].sort_values('course')
    positions = x + (i - 1) * width
    ax4.bar(positions, quarter_data['total'].values, width,
            label=quarter, color=quarter_colors[quarter], alpha=0.8)
ax4.set_ylabel('Total Capacity', fontsize=11, fontweight='bold')
ax4.set_title('Total Seat Capacity by Course', fontsize=12, fontweight='bold')
ax4.set_xlabel('Course', fontsize=11, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(course_order, rotation=45, ha='right', fontsize=9)
ax4.grid(axis='y', alpha=0.3)

# Bottom right: Summary statistics table
ax5 = fig.add_subplot(gs[2, 1])
ax5.axis('off')

# Create summary stats
summary_stats = []
for quarter in ['Fall 2024', 'Winter 2025', 'Spring 2025']:
    qdata = df[df['quarter_label'] == quarter]
    summary_stats.append([
        quarter,
        f"{qdata['enrolled'].sum():.0f}",
        f"{qdata['waitlisted'].sum():.0f}",
        f"{qdata['total'].sum():.0f}",
        f"{(qdata['enrolled'].sum() / qdata['total'].sum() * 100):.1f}%"
    ])

table = ax5.table(cellText=summary_stats,
                  colLabels=['Quarter', 'Total\nEnrolled', 'Total\nWaitlist', 'Total\nCapacity', 'Overall\nUtil%'],
                  cellLoc='center',
                  loc='center',
                  bbox=[0, 0.2, 1, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style header
for i in range(5):
    table[(0, i)].set_facecolor('#3498db')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Color rows by quarter
for i, quarter in enumerate(['Fall 2024', 'Winter 2025', 'Spring 2025']):
    table[(i+1, 0)].set_facecolor(quarter_colors[quarter])
    table[(i+1, 0)].set_text_props(weight='bold', color='white')

ax5.set_title('Overall Summary Statistics', fontsize=12, fontweight='bold', pad=20)

fig.suptitle('DSC Course Enrollment Comprehensive Dashboard', 
             fontsize=18, fontweight='bold', y=0.995)

plt.savefig('enrollment_dashboard.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: enrollment_dashboard.png")
plt.close()

print("\n" + "=" * 60)
print("✓ All visualizations created successfully!")
print("=" * 60)
print("\nGenerated files:")
print("  1. enrollment_comparison_stacked.png - Stacked bars with capacity lines")
print("  2. enrollment_utilization_rates.png - Utilization percentage comparison")
print("  3. enrollment_proportional.png - 100% stacked proportional view")
print("  4. enrollment_faceted.png - Individual course breakdowns")
print("  5. enrollment_heatmap.png - Utilization rate heatmap")
print("  6. enrollment_dashboard.png - Comprehensive multi-metric dashboard")
print("\nData file:")
print("  - enrollment_comparison.csv - Raw comparison data")


# ============================================================================
# VISUALIZATION 7: Course-Level Trend Line Plot
# ============================================================================
plt.figure(figsize=(14, 8))
sns.lineplot(data=df, x='quarter_label', y='enrolled', hue='course', marker='o')
plt.title('Enrollment Trends Across Quarters by Course', fontsize=16, fontweight='bold')
plt.ylabel('Number of Enrolled Students')
plt.xlabel('Quarter')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('enrollment_trends_by_course.png', dpi=300)
plt.close()


# ============================================================================
# VISUALIZATION 8: Waitlist-to-Capacity Ratio Chart
# ============================================================================
df['waitlist_ratio'] = (df['waitlisted'] / df['total']) * 100
plt.figure(figsize=(12, 8))
sns.barplot(data=df, x='course', y='waitlist_ratio', hue='quarter_label', palette=quarter_colors)
plt.title('Waitlist Pressure (% of Total Capacity)', fontsize=16, fontweight='bold')
plt.ylabel('Waitlisted / Capacity (%)')
plt.xlabel('Course')
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('waitlist_pressure.png', dpi=300)
plt.close()


# ============================================================================
# VISUALIZATION 9: Capacity vs Enrollment Scatter Plot
# ============================================================================
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='total', y='enrolled', hue='quarter_label', style='course', s=150)
plt.plot([0, df['total'].max()], [0, df['total'].max()], 'r--', label='Perfect Capacity Usage')
plt.xlabel('Total Capacity')
plt.ylabel('Enrolled Students')
plt.title('Enrollment vs. Capacity by Quarter', fontsize=16, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('enrollment_vs_capacity.png', dpi=300)
plt.close()


# ============================================================================
# VISUALIZATION 10: Bottleneck Courses Over Time
# ============================================================================
top_waitlist = df.groupby('quarter_label').apply(lambda x: x.nlargest(5, 'waitlisted'))
plt.figure(figsize=(12, 8))
sns.barplot(data=top_waitlist, x='course', y='waitlisted', hue='quarter_label', dodge=True)
plt.title('Top 5 Courses by Waitlist Size Each Quarter', fontsize=16, fontweight='bold')
plt.ylabel('Waitlisted Students')
plt.xlabel('Course')
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('top_waitlist_courses.png', dpi=300)
plt.close()



# ============================================================================
# VISUALIZATION 11: Quarter-over-Quarter Change Plot
# ============================================================================
df_sorted = df.sort_values(['course', 'quarter_label'])
df_sorted['enrollment_change'] = df_sorted.groupby('course')['enrolled'].pct_change() * 100
plt.figure(figsize=(14, 8))
sns.barplot(data=df_sorted, x='course', y='enrollment_change', hue='quarter_label', palette=quarter_colors)
plt.title('Quarter-over-Quarter Enrollment Change (%)', fontsize=16, fontweight='bold')
plt.ylabel('Enrollment Change (%)')
plt.xlabel('Course')
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='black', linewidth=1)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('enrollment_change_by_quarter.png', dpi=300)
plt.close()
