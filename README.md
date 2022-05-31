# cse_163_final_project
CSE 163 Final Project by Deja, Alison, and Zach.
Language: Python
CSVs Source: Data.WA.gov
GeoDataFrame Data Source: Catalog.Data.gov
JSON Source: https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json

Summary:
Here you will find the code for our CSE 163 Final Project. Our group
decided to analyze highschool and college statistics in Washington State
by county. Our data comes from Data.WA.gov and Catalog.Data.gov. Our goal
is to create a variety of graphs that represent the seven-year cohorts of
students that started high school from 2008 through 2012 (the latest of whom
in each group finished in the 2014-15 through 2018-19 school years), to find
graduation trends between different student demographics such as Race, Income,
English Language Learners, and Gender. Our graphs allow the viewers to easily
come to their own conclusion about the data. Though, we dive into a deeper analysis. 
To read our analysis, ...

To run the code and see the data yourself, here's what you must do:
1. Create a Folder. Example: "FinalProject" (can be named anything)
2. Inside of FinalProject, clone this repository
    * git clone https://github.com/Quesadeha/cse_163_final_project.git
3. Also inside of FinalProject, create a folder named "Documents" (must be named Documents)
4. Inside of Documents, download the CSV data files and GeoDataFrame folder
    * https://drive.google.com/drive/folders/1njVSLZgUeG0PwVA8U_9XlLPpvtzMnRc2?usp=sharing
5. Install plotly:
    * Create a new terminal
    * Do the following command in the terminal: $ conda install -c plotly plotly=5.8.0
    * Type "y" when asked if you want to proceed
6. Go to FinalProject/cse_163_final_project/main/displayData.py
7. Run displayData.py and 18 png files will my downloaded into your current directory.
    If you cannot view these images, you can download them here...
    * https://drive.google.com/drive/folders/1DNtpmB50hrOxnuqRA2W5SpLq3Xv1LfS7?usp=sharing
8. If you chose to input "False" for the show_maps parameter when calling plot_rates_maps,
    then you will need to go to Documents/Interactive_Maps and open each file to view and
    interact with each map in a browser.

