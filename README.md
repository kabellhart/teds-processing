# teds-processing
Code for processing and analyzing the publicly available datasets TEDS-A and TEDS-D

TEDA-A and TEDS-D are free to use, public datasets recording drug treatment events in the United States. 
These datasets can be difficult to use at scale because the data dictionaries are provided in PDF format. 
Furthermore, there are different data dictionaries for TEDS-A versus TEDS-D, and they can also vary from year to year. 
Reading the PDF files into a usable format can be challenging. 

To address these challenges, this repository provides the following:
1. CSV files containing the tabular representation of existing TEDS data dictionaries.
2. The Python files used to generate these CSV files. These may prove useful for future releases of TEDS data dictionaries.
3. A CSV file (teds_d_harmonization.csv) listing harmonized definitions for inconsistent categories across TEDS-D dictionaries.
For example, in TEDS-D 2015, an ethnicity of "4" indicates the patient is "NOT OF HISPANIC OR LATINO ORIGIN" whereas
in TEDS-D 2006-2014, a "4" indicates the patient is "OTHER SPECIFIC HISPANIC." 
Without harmonizing the fields and simply taking them as distinct strings, there are ten categories for ethnicity across TEDS-D:
Puerto Rican; Mexican; Cuban; Cuban or other specific Hispanic; Other specific Hispanic; Not of Hispanic origin; Not of Hispanic or Latino origin; Hispanic, specific origin not specified; Hispanic or Latino, specific origin not specified; and Missing/unknown/not collected/invalid
Relabeling the data using the harmonization file results in only six categories.


For **TEDS-D 2006-2014**: 

Used read_tedsd_2006_2014.py

The result was imperfect and required several manual corrections. These manual corrections are shown in the file:

TEDS-D-2006-2014-DS0001-info-codebook_codes_manual_step.xlsx

The corrected CSV is posted with the other CSVs.


For **TEDS-D 2015** and **TEDS-D 2016**

Used read_tedsd_2006_2014.py

Both results had minor issues and needed a few manual corrections. 

Corrected CSVs are posted. 


For **TEDS-D 2017, TEDS-D 2018, TEDS-D 2019, and TEDS-A 2000-2019**

Used read_tedsa_and_tedsd_2017_19.py

No manual corrections needed. Output CSVs are posted.

