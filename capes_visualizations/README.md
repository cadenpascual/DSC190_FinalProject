# DSC CAPEs Data Visualizations

This folder contains 5 detailed visualizations generated from the CAPEs course evaluation data for DSC (Data Science) department only (Summer 2007 - Spring 2023).

## Generated Files

### 1. Difficulty Distribution by Course Level (`1_difficulty_distribution_by_course_level.png`)
**Type:** Stacked Bar Chart

**Description:** Shows the proportional distribution of difficulty categories (Very Easy, Easy, Moderate, Difficult, Very Difficult, Extremely Difficult) across DSC course levels (Lower, Lower-Mid, Upper, Upper-Mid, Graduate). Each bar represents 100% of courses for that course level, with segments colored by difficulty level.

**Key Insights:**
- Visualizes which course levels have more challenging vs. easier courses
- Shows the relative proportion of each difficulty category within each course level
- Helps identify course levels with consistent difficulty patterns

---

### 2. Study Hours Trends Over Time (`2_study_hours_trends_over_time.png`)
**Type:** Multi-line Chart

**Description:** Tracks the average study hours per week across all terms (FA07 to WI23) for each DSC course level. Each course level is represented by a colored line showing how study hours have changed over time. Also includes an overall DSC average line.

**Key Insights:**
- Reveals trends in study hours over the 16-year period for DSC courses
- Compares study hour patterns between different course levels
- Identifies course levels with increasing or decreasing study hour requirements
- Shows seasonal or long-term trends in DSC course workload

---

### 3. Recommendation Ratings Comparison (`3_recommendation_ratings_comparison.png`)
**Type:** Grouped Bar Chart

**Description:** Compares average "Recommend Class" vs. "Recommend Instructor" ratings across DSC course levels. Each course level has two bars side-by-side showing both metrics.

**Key Insights:**
- Identifies course levels with high student satisfaction
- Reveals discrepancies between class and instructor ratings
- Highlights course levels where students recommend the class more than the instructor (or vice versa)
- Shows overall student satisfaction levels by course level

---

### 4. Difficulty Score Heatmap (`4_difficulty_score_heatmap.png`)
**Type:** Heatmap

**Description:** A color-coded matrix showing average difficulty scores by DSC course level (rows) and year (columns). Colors range from green (easier) to red (more difficult), with numeric values displayed in each cell.

**Key Insights:**
- Shows how difficulty scores vary across course levels and years
- Identifies temporal trends in DSC course difficulty
- Highlights course levels and years with particularly high or low difficulty scores
- Reveals patterns in difficulty changes over time for DSC courses

---

### 5. Comprehensive CAPEs Dashboard (`5_comprehensive_capes_dashboard.png`)
**Type:** Multi-panel Dashboard

**Description:** A comprehensive dashboard with 5 subplots providing an overview of key CAPEs metrics:

**Panel 1 (Top Left):** Average Difficulty Score by Course Level
- Bar chart with error bars showing mean and standard deviation
- Compares overall difficulty across DSC course levels

**Panel 2 (Top Right):** Enrollment vs. Study Hours Scatter Plot
- Scatter plot colored by difficulty score
- Shows relationship between class size and study hours
- Color intensity indicates difficulty level

**Panel 3 (Bottom Left):** Response Rate Analysis
- Average CAPEs response rate (Evals Made / Enrollment) by course level
- Shows which course levels have higher student participation in evaluations

**Panel 4 (Bottom Right):** Overall Difficulty Category Distribution
- Bar chart showing total count of courses in each difficulty category
- Provides overall distribution across all departments

**Panel 5 (Bottom Spanning):** Study Hours Distribution by Difficulty
- Boxplot showing distribution of study hours for each difficulty category
- Includes median, quartiles, and outliers
- Red dashed line indicates mean values

**Key Insights:**
- Provides a comprehensive overview of all key DSC metrics
- Enables quick comparison across multiple dimensions
- Identifies outliers and patterns in DSC course data

---

## Data Source

All visualizations are based on the `combined_courses.csv` file, filtered to DSC department only, which contains:
- 265 unique DSC course evaluations
- Data from DSC (Data Science) department only
- Time period: Summer 2007 (SU07) to Spring 2023 (SP23)
- Metrics: Enrollment, evaluations, recommendations, study hours, grades, difficulty scores

## Usage

To regenerate these visualizations, run:
```bash
python3 generate_capes_visualizations.py
```

The script will create all 5 visualizations in high resolution (300 DPI) PNG format in this directory.

