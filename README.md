# Traffic Patterns in US Traffic 2015 Dataset

## Installation Instructions
The following steps are required only if you want to run the .ipynb and .py files on your local machine.
#### To run the scripts on your local machine (Assumes that you already have an existing anaconda (Windows/Mac) or conda installation (Linux), with Python installed):
```
git clone 
cd traffic
pip install -r requirements.txt
pip install notebook # Can skip this if you already have Jupyter Notebook installed in your current environment
jupyter notebook
```
## Viewing Instructions
To view the Jupyter Notebook containing the analyis results:
<br>From the Home Page of the Jupyter Notebook, navigate to Top 5 Patterns.ipynb in the traffic folder and launch it

## Folders and Files
### Folders
datasets: 
> Contains
> - The original datasets (dot_traffic_2015.txt.gz and dot_traffic_stations_2015.txt.gz)
> - The pickled datasets (dot_traffic_2015.pkl.gz and dot_traffic_stations_2015.pkl)
> - The pickled mapping dictionary (dot_mappings_2015.pkl)
>
helpers: 
> Contains utils.py which contains helper classes and functions for cleaning (i.e. removal of columns) and pickling the datasets
>
### Files
Top 5 Patterns.ipynb
> Jupyter Notebook containing the analysis results
> 
Top 5 Patterns.html
> HTML version of Top 5 Patterns.ipynb
> 
