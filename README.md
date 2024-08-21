# CAR21_AmazonPropertyOverlap
This repository is for Paul Furmuro, Jevan Yu, J. Aaron Hogan, Luis M. Tavares de Carvalho, Brenda Brito & Eric F. Lambin. 2024 "Land conflicts from overlapping claims in Brazil’s rural environmental registry" _PNAS_ **121(33)**:e2407357121.  [https://doi.org/10.1073/pnas.2407357121](https://doi.org/10.1073/pnas.2407357121)

[![DOI](https://zenodo.org/badge/775467877.svg)](https://zenodo.org/doi/10.5281/zenodo.13356638)


It contains 3 Python/Jupyter Notebook files:
1. def_statistics_CS.py - this file calculates the deforestation statistics used in the Chi-square analysis.
2. LR_statistics_CS.py - this file calculates the LR (legal forest reserve) statistics used in the Chi-square analysis.
3. duplicate_filter.ipynb - this file is used to identify suspected duplicates in the CAR database.

It contains 3 R Markdown files:
1. CAR21_PoissonOverlap.Rmd - this is the main analysis file which fits the Poisson generalized linear mixed-effects models.
      * the dataset can be found here: https://www.dropbox.com/scl/fi/en02cup52fjp9og47uv46/CAR21_GLMMs_dataset_oct_FINAL.csv?rlkey=1sowd8uwdpykzarh6dio2yyju&dl=0.  The dataset is large and the glmm models take some time to fit.
      * Therefore, an Rdata workspace with saved model objects can be loaded form here:  https://www.dropbox.com/scl/fi/xo5zwykz3uj9dggj24kdg/Final_Model_Run_WKSPCE_DEC.2023.RData?rlkey=xqdkuqjkzs9yy1on9id3pt12b&dl=0

2. CAR21_ChiSquared.Rmd - this file contains the Chi-squared tests for evaluation whether deforestation occurs disproportionately in property overlaps.
   
3. CAR21_temporalANOVAS.Rmd - this file contains Analysis of Variance to test whether CAR21 property overlap is increasing over time.

Finally, it contains 3 figures which appear in the main text or supporing information appendix of the manuscript. 

For questions regarding the details of the study or the dataset, please contact Paul Furumo (pfurumo at gmail dot com). 
