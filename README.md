# Analysis of correlations between traffic data depended congestion detection and incident causalities
## Master-Thesis B.Sc. Jakob Erpf

## Abstract
Current navigation systems often use accumulation strategies to estimate travel time while considering time delays through congestions based on analyzing the history of the underlying street network. This approach can be disturbed through uncommon events creating short time block- ages or be biased through regular accruing, long-term traffic volume reductions. This thesis evaluates a new approach of predicting congestion and accident characteristics through the correlation of congestions and incidents which are placed in temporal and spatial vicinity of each other. To evaluate this in a exploratory data analysis, three real world datasets from the year 2019 will be considered providing traffic movement and incident data. After an algorithmic approach to analyzing a derivative of a floating car dataset for jams and locating spatial and timely adjacent incidents from the BAYSIS and ArbIS, the thesis will evaluate if and how these incidents and jams are correlated with each other with statistical methods. Therefore the methodology consist of the clustering of FCD, adjacent incident matching, correlation and prediction analysis.

The results show that there are significant correlations between congestion and incident characteristics which means that individual accident characteristics statistical lead to jams with a certain length and duration. This length and duration relationship is also present with the road- work characteristics of the roadwork’s location (road) and the month of the roadwork. Although these correlations provide a first indication of predictability, a separate analysis revealed not predictability between any of the characteristics. At this point it also has to be noted that many relations had insufficient sample size after classifying the data and a larger dataset would be necessary to find more significant and reliable results.

## Contents

- Thesis in LaTex
- Thesis Assest (Literatur,Bibliogrphy)
- Evaluation-Tool Codebase in Java
- Analysis-Tool Codebase in Python/R
