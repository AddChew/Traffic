# 2015 US Traffic Patterns
This project analyses the top 5 most obvious patterns in US Traffic 2015 dataset.
## Installation Instructions
The steps here are required only if you want to view/run the Jupyter Notebook (i.e. .ipynb and .py files) on your local machine. If not, you can just proceed to ***Viewing Instructions: To view the HTML version of the analyis results***, which does not require any prior setup.
#### To run the scripts on your local machine (Assumes that you already have an existing anaconda (Windows/Mac) or conda installation (Linux), with Python installed):
```
$ git clone https://github.com/AddChew/Traffic.git
$ cd traffic
$ pip install -r requirements.txt
$ pip install notebook # Can skip this if you already have Jupyter Notebook installed in your current environment
$ jupyter notebook
```
## Viewing Instructions
#### To view the Jupyter Notebook version of the analyis results:
- From the Home Page of the Jupyter Notebook, navigate to and open Top 5 Patterns.ipynb from the traffic folder.
#### To view the HTML version of the analyis results:
- Download Top 5 Patterns.html from this repository and open it in your browser.
#### To view the helper scripts used in Top 5 Patterns.ipynb:
- Navigate to and open utils.py in traffic/helpers folder.

## Folders and Files
### Folders
datasets: 
> Contains
> - The original datasets (dot_traffic_2015.txt.gz and dot_traffic_stations_2015.txt.gz)
> - The pickled datasets (dot_traffic_2015.pkl.gz and dot_traffic_stations_2015.pkl)
> - The pickled mapping dictionary (dot_mappings_2015.pkl)
>
helpers: 
> - Contains utils.py which contains helper classes and functions for cleaning (i.e. removal of columns) and pickling the datasets
>
### Files
Top 5 Patterns.ipynb
> - Jupyter Notebook containing the analysis results
> 
Top 5 Patterns.html
> - HTML version of Top 5 Patterns.ipynb
> 
