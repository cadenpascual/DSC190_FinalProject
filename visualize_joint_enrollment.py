import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ------------------------------------------------------------
# Output directory
# ------------------------------------------------------------
OUTPUT_DIR = "webreg_plots/joint_data_plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
df_full = pd.read_csv("webreg_data/results/enrollment_comparison_shared.csv")
df_partial = pd.read_csv("webreg_data/results/enrollment_comparison_partial.csv")

df_full['offering_type'] = 'Fully Offered'
df_partial['offering_type'] = 'Partially Offered'

df_all = pd.concat([df_full, df_partial], ignore_index=True)

# ------------------------------------------------------------
# Required vs Elective
# ------------------------------------------------------------
required_courses = {
    'DSC_10', 'DSC_20', 'DSC_30', 'DSC_40A', 'DSC_40B',
    'DSC_80', 'DSC_100', 'DSC_102', 'DSC_106',
    'DSC_140A', 'DSC_140B', 'DSC_148',
    'DSC_180A', 'DSC_180B'
}

df_all['course_type'] = np.where(
    df_all['course'].isin(required_courses),
    'Required',
    'Elective'
)

sns.set_style("whitegrid")

# ============================================================
# 1️⃣ Capacity Stress Matrix
# ============================================================
stress = (
    df_all
    .groupby(['course', 'offering_type', 'course_type'])
    .agg(
        avg_utilization=('utilization_rate', 'mean'),
        avg_waitlist=('waitlisted', 'mean'),
        avg_enrolled=('enrolled', 'mean')
    )
    .reset_index()
)

plt.figure(figsize=(12, 9))
sns.scatterplot(
    data=stress,
    x='avg_utilization',
    y='avg_waitlist',
    hue='offering_type',
    style='course_type',
    size='avg_enrolled',
    sizes=(100, 1000),
    alpha=0.85
)

plt.axvline(100, color='red', linestyle='--', alpha=0.5)
plt.axhline(stress['avg_waitlist'].median(), color='gray', linestyle='--', alpha=0.5)

plt.title("Capacity Stress Matrix (Utilization vs Waitlist)")
plt.xlabel("Average Utilization Rate (%)")
plt.ylabel("Average Waitlist Size")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/capacity_stress_matrix.png", dpi=300)
plt.close()

# ============================================================
# 2️⃣ Offering Frequency vs Utilization
# ============================================================
frequency = (
    df_all
    .groupby('course')
    .agg(
        quarters_offered=('quarter_label', 'nunique'),
        mean_utilization=('utilization_rate', 'mean'),
        course_type=('course_type', 'first')
    )
    .reset_index()
)

plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=frequency,
    x='quarters_offered',
    y='mean_utilization',
    hue='course_type',
    s=150,
    alpha=0.85
)

sns.regplot(
    data=frequency,
    x='quarters_offered',
    y='mean_utilization',
    scatter=False,
    color='black',
    line_kws={'linestyle': '--'}
)

plt.title("Offering Frequency vs Utilization")
plt.xlabel("Number of Quarters Offered")
plt.ylabel("Mean Utilization Rate (%)")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/offering_frequency_vs_utilization.png", dpi=300)
plt.close()

# ============================================================
# 3️⃣ Enrollment vs Capacity (Combined)
# ============================================================
plt.figure(figsize=(11, 9))
sns.scatterplot(
    data=df_all,
    x='total',
    y='enrolled',
    hue='quarter_label',
    style='course_type',
    s=140,
    alpha=0.85
)

max_cap = df_all['total'].max()
plt.plot([0, max_cap], [0, max_cap], 'r--', linewidth=2)

plt.title("Enrollment vs Capacity (All Courses)")
plt.xlabel("Total Capacity")
plt.ylabel("Enrolled Students")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/enrollment_vs_capacity_all_courses.png", dpi=300)
plt.close()

# ============================================================
# 4️⃣ Joint Utilization Heatmap
# ============================================================
pivot_util = df_all.pivot_table(
    index='course',
    columns='quarter_label',
    values='utilization_rate',
    aggfunc='mean'
).sort_index()

plt.figure(figsize=(10, max(8, len(pivot_util) * 0.35)))
sns.heatmap(
    pivot_util,
    annot=True,
    fmt='.1f',
    cmap='RdYlGn',
    vmin=0,
    vmax=100,
    linewidths=0.5,
    cbar_kws={'label': 'Utilization Rate (%)'}
)

plt.title("Course Utilization Heatmap (All Courses)")
plt.xlabel("Quarter")
plt.ylabel("Course")
plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/utilization_heatmap_all_courses.png", dpi=300)
plt.close()

# ============================================================
# 5️⃣ Required vs Elective Utilization Heatmaps
# ============================================================
quarter_order = ['Fall 2024', 'Winter 2025', 'Spring 2025']

fig, axes = plt.subplots(1, 2, figsize=(16, 10), constrained_layout=True)

for ax, ctype in zip(axes, ['Required', 'Elective']):
    subset = df_all[df_all['course_type'] == ctype]
    pivot = subset.pivot_table(
        index='course',
        columns='quarter_label',
        values='utilization_rate',
        aggfunc='mean'
    ).reindex(columns=quarter_order)

    sns.heatmap(
        pivot,
        annot=True,
        fmt='.1f',
        cmap='RdYlGn',
        vmin=0,
        vmax=100,
        linewidths=0.5,
        mask=pivot.isna(),
        cbar=False,
        ax=ax
    )

    ax.set_title(f"{ctype} Courses")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Course")

cbar = fig.colorbar(
    axes[0].collections[0],
    ax=axes,
    orientation='vertical',
    fraction=0.03,
    pad=0.02
)
cbar.set_label("Utilization Rate (%)")

fig.suptitle("Utilization Heatmaps by Course Type")

plt.savefig(f"{OUTPUT_DIR}/utilization_heatmaps_by_course_type.png", dpi=300)
plt.close()

# ============================================================
# 6️⃣ Capacity Pressure Heatmap
# ============================================================
df_all['capacity_pressure'] = df_all['utilization_rate'] - 100

pivot_pressure = df_all.pivot_table(
    index='course',
    columns='quarter_label',
    values='capacity_pressure',
    aggfunc='mean'
)

plt.figure(figsize=(10, max(8, len(pivot_pressure) * 0.35)))
sns.heatmap(
    pivot_pressure,
    annot=True,
    fmt='+.1f',
    cmap='coolwarm',
    center=0,
    linewidths=0.5,
    cbar_kws={'label': 'Capacity Pressure (%)'}
)

plt.title("Capacity Pressure Heatmap (Over/Under Capacity)")
plt.xlabel("Quarter")
plt.ylabel("Course")
plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/capacity_pressure_heatmap.png", dpi=300)
plt.close()

print("✓ All joint-data plots saved to:", OUTPUT_DIR)
