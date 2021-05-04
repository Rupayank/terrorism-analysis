Application is deployed in [link](https://terrorism-trend-analysis.herokuapp.com/).
# Overview
This web application is basically a predictive analysis tool. It uses "global terrorism database"(GTD) which is a dataset of nearly 1,90,000 records maintained by the "National Consortium for the study of terrorism and Responses to terrorism" (START).
# Requirements
For the terror_analysis.py to run properly the databse is required to be downloaded from the [link](https://www.start.umd.edu/gtd/access/) & saved in the same workspace as the source code. 

This application has been made using python data visualisation library -Dash hence ensure dash is installed in the local machine
# Features
1. It includes two methods of visualizing the data; *Map tool*- For visualising data in the world map & *Area chart*- For visualising the data as number of incident counts per year
2. Both the tools includes options to compare the data of the World & India (specifically)
3. Map tool includes filter options so as to select specific- *Month , Date, Region, Country, State/Provicnce, City, Attack type and the of range of year*
4. Chart tool has options to select various parameters from the database and a search input to enable the user to search for a specific value in selected parameter.
5. There is also an option to run a time lapse between the range of year selected.
# Conclusion
Since military resources of countries are almost uniformly distributed and are less in numbers, it would be of help for them in the allocation of suitable military resources at places of interest using this analysis tool.
