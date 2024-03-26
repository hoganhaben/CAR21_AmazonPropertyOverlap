# CAR21_AmazonPropertyOverlap
This repository is for Paul Furumo et al 2024 (in review) Land conflicts from overlapping claims in Brazil’s rural environmental registry

It contains 3 Rmd files 
1. CAR21_PoissonOverlap.Rmd - this is the main analysis file which fits the Poisson generalize linear mixed-effects models.
      * the dataset can be found here: https://www.dropbox.com/scl/fi/en02cup52fjp9og47uv46/CAR21_GLMMs_dataset_oct_FINAL.csv?rlkey=1sowd8uwdpykzarh6dio2yyju&dl=0.  The dataset is large and the glmm models take some time to fit.
      * Therefore, an Rdata workspace with save model objects can be loaded form here:  https://www.dropbox.com/scl/fi/xo5zwykz3uj9dggj24kdg/Final_Model_Run_WKSPCE_DEC.2023.RData?rlkey=xqdkuqjkzs9yy1on9id3pt12b&dl=0

2. CAR21_ChiSquared.Rmd - this file contains the Chi-square test for evaluation whether deforestation occurs disproportionately in property overlaps.
   
3. CAR21_temporalANOVAS.Rmd - this file contains Analysis of Variance to test whether CAR21 property overlap is increasing over time.

It also contains 4 Python/Python Notebook files
1. def_statistics_CS.py - this file calculates the deforestation statistics used in the Chi-square analysis.
2. LR_statistics_CS.py - this file calculates the LR (legal forest reserve) statistics used in the Chi-square analysis.
3. and 4. duplicate_filter.ipynb and identify_duplicates - these files are used to identify suspected duplicates in the CAR.

Finally, it contains 3 figures which appear in the main text or supporing information appendix of the manuscript. 

For questions regarding the details of the study or the dataset, please contact Paul Furumo (pfurumo at gmail dot com). 
