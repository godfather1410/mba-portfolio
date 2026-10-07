# Predicting Diabetes: Decision Tree vs Random Forest

**Course:** Business Analytics  
**Programme:** PGPM 2026-27, Great Lakes Institute of Management, Term 3 (Aug-Sep 2026)  
**Type:** Individual  
**Skills:** Python, scikit-learn, classification, model evaluation

## The question / brief
_Summarised from the course brief._

Build and compare a Decision Tree and a Random Forest that predict whether a patient is diabetic (768 records, 8 predictors, 500/268 split).

a) Prepare the data - note that zeros in glucose, blood pressure, skinfold, insulin and BMI are not biologically plausible and must be handled.

b) Build and tune the decision tree.  c) Build and tune the random forest.  d) Compare both on a consistent set of metrics.

Write up the comparison with insights and a recommendation.


## What I did
Classification on the public Pima diabetes dataset (768 patients, 35% positive): spotting implausible zeros and imputing instead of dropping 49% of rows, stratified split, class weighting, decision tree vs random forest comparison, feature importance and decision-threshold tuning for screening.

## Files
| File | Type |
|---|---|
| [Report.docx](Report.docx) | Word original |
| [Report.pdf](Report.pdf) | PDF (viewable on GitHub) |
| [data/diabetes.csv](data/diabetes.csv) | Dataset |
| [diabetes_classification.ipynb](diabetes_classification.ipynb) | Jupyter notebook (renders on GitHub) |

## Note
Academic coursework. Company names in fictional cases are illustrative; figures in case-based work come from the case material provided in class.
