# Digital Ads Segmentation with Clustering

**Course:** Business Analytics  
**Programme:** PGPM 2026-27, Great Lakes Institute of Management, Term 3 (Aug-Sep 2026)  
**Type:** Group project (team members are credited inside the submission)  
**Skills:** Python, clustering (hierarchical, K-means), marketing analytics

## The question / brief
_Summarised from the course brief._

ads24x7, a digital marketing company with $10M seed funding, wants its ads segmented into homogeneous groups using clustering on CPM, CPC and CTR.

Steps: basic data analysis; impute missing CPC/CTR/CPM with the given formulas via a user-defined function; check and decide on outlier treatment for K-means; z-score scaling and its effect; hierarchical clustering (Ward, Euclidean dendrogram); elbow plot up to k=10 and silhouette scores; final K-means; profile the clusters and give recommendations.


## What I did
Segmented 25,857 digital ad records by CTR, CPM and CPC for an ad-tech firm: rebuilt missing derived metrics from raw fields, fixed a CTR unit inconsistency, treated outliers, z-score scaling, hierarchical (Ward) clustering and K-means with elbow and silhouette checks, then profiled clusters into marketing recommendations.

## Files
| File | Type |
|---|---|
| [Report.pdf](Report.pdf) | PDF (viewable on GitHub) |
| [ads_clustering.ipynb](ads_clustering.ipynb) | Jupyter notebook (renders on GitHub) |
| [data/ads_data.xlsx](data/ads_data.xlsx) | Excel workbook |

## Note
Academic coursework. Company names in fictional cases are illustrative; figures in case-based work come from the case material provided in class.
