# cse_163_final_project
CSE 163 Final Project by Deja, Alison, and Zach.
Language: Python
CSVs Source: Data.WA.gov
GeoDataFrame Data Source: Catalog.Data.gov
GeoJSON Source: https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json

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
    * https://docs.google.com/document/d/1U6RQ-LARbqiL1DrZLg2QrZ_dfE9NlgqaiI4CVHLAgbI/edit?usp=sharing 

To run the code and see the data yourself, here's what you must do:
1. Download and unzip the FinalProject.zip file.

2. Install Anaconda and the CSE 163 Environment, for Pandas & GeoPandas & MatPlotLib
    * https://courses.cs.washington.edu/courses/cse163/software/ 
    * Make sure your IDE is running on the 163 Environment

3. Install plotly:
    * Create a new terminal
    * Do the following command in the terminal: $ conda install -c plotly plotly=5.8.0
    * Type "y" when asked if you want to proceed

4. Go to FinalProject/cse_163_final_project/main/display_data.py

5. Run display_data.py and 20 png files will be downloaded into your current directory.
    If you cannot view these images, you can download them here...
    * https://drive.google.com/drive/folders/1DNtpmB50hrOxnuqRA2W5SpLq3Xv1LfS7?usp=sharing

6. Go to FinalProject/cse_163_final_project/create_interactive.py

7. Run create_interactive.py (Default: Opens 5 Interactive maps in browser)
    * You'll also be able to access the html links inside FinalProject/Documents/Interactive_Maps

8. (Optional) Go to FinalProject/cse_163_final_project/mapping.py

9. (Optional) Open Mapping.py, change plot_rates_map 'show_maps' parameter to False. 
    Maps will only download into the Interactive_Maps folder, and you can open each file
    in the browser individually