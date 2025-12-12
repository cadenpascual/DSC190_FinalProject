# Final Variables Used for Analysis

## Target Variable (Dependent Variable)

**From WebReg:**
- **`utilization_rate`**: Course enrollment utilization rate (percentage) - This is the target/predicted variable

## Feature Variables (Independent Variables / Predictors)

### From SET Data:

**1. Raw SET Features:**
- **`study_hours`**: Average hours worked per week (Avg Hours Worked)
- **`avg_grade`**: Average grade received (Avg Grade Received, converted to GPA)
- **`learning_avg`**: Learning Average* rating (1-5 scale)
- **`structure_avg`**: Structure Average* rating (1-5 scale)
- **`environment_avg`**: Environment Average* rating (1-5 scale)

**2. Derived Difficulty Labels (Binary 0/1):**
- **`difficulty_manual`**: Composite difficulty label (0=Easy, 1=Difficult) based on median split of composite difficulty score
- **`difficulty_study_hours`**: Binary label based on median split of study_hours
- **`difficulty_avg_grade`**: Binary label based on median split of avg_grade (lower = difficult)
- **`difficulty_learning_avg`**: Binary label based on median split of learning_avg (lower = difficult)
- **`difficulty_structure_avg`**: Binary label based on median split of structure_avg (lower = difficult)
- **`difficulty_environment_avg`**: Binary label based on median split of environment_avg (lower = difficult)

**3. Composite Score:**
- **`difficulty_score`**: Composite difficulty score (0-1 range) created by normalizing and averaging:
  - study_hours (normalized directly)
  - learning_avg (inverted normalization)
  - structure_avg (inverted normalization)
  - environment_avg (inverted normalization)

### Merging Keys:
- **`course_number`**: Course number (e.g., 100, 180, 190)
- **`quarter`**: Term/quarter identifier (e.g., 'fa24', 'wi25', 'sp25')

---

## Analysis Structure

### T-Test Analysis:
- **Target**: `utilization_rate` (from WebReg)
- **Predictors**: All binary difficulty labels (difficulty_manual, difficulty_study_hours, difficulty_avg_grade, difficulty_learning_avg, difficulty_structure_avg, difficulty_environment_avg)
- **Test**: Independent samples t-test comparing utilization_rate between Easy (0) and Difficult (1) groups

### Two-Way ANOVA Analysis:
- **Target**: `utilization_rate` (from WebReg)
- **Main Effects**: 
  - `difficulty_manual` (composite difficulty, binary)
  - Individual features: `study_hours`, `avg_grade`, `learning_avg`, `structure_avg`, `environment_avg`
- **Interaction Terms**: `difficulty_manual × feature` for each individual feature
- **Test**: Two-way ANOVA testing interaction effects between composite difficulty and individual features on utilization_rate

---

## Data Sources Summary:

**SET Data (Features):**
- study_hours
- avg_grade
- learning_avg
- structure_avg
- environment_avg
- All derived difficulty labels

**WebReg Data (Target):**
- utilization_rate

**Final Merged Dataset (`df_with_util`):**
- 41 courses with both difficulty labels and utilization_rate
- Merged on: course_number + quarter


