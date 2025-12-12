# Difficulty Score Methodology - Presentation Bullet Points

## How the Difficulty Score Was Engineered

• **Four SET features combined**: Study hours, Learning average, Structure average, and Environment average

• **Normalization approach**:
  - Study hours: Higher = more difficult → Direct normalization [0,1]
  - SET ratings (Learning/Structure/Environment): Lower = more difficult → Inverted normalization [0,1]

• **Equal-weight averaging**: All four normalized components averaged to create composite score (0-1 scale)

• **Binary classification**: Median split (median = 0.406) creates "Easy" vs "Difficult" labels
  - Score ≥ 0.406 → "Difficult" (1)
  - Score < 0.406 → "Easy" (0)

---

## Alternative Shorter Version (for tighter slides):

• **Composite score** = Average of 4 normalized SET features (study hours + 3 inverted quality ratings)

• **Normalization**: Study hours normalized directly; SET ratings inverted (lower ratings = higher difficulty)

• **Classification**: Median split creates binary "Easy" vs "Difficult" labels

---

## Even More Concise Version (for very tight slides):

• **4 SET features** normalized and averaged (study hours + 3 inverted quality ratings)

• **Binary labels** via median split: Score ≥ 0.406 = "Difficult", < 0.406 = "Easy"

