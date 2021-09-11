import pickle
import pandas as pd
from typing import Tuple


"""
    Columns to include when loading the data from dot_traffic_2015.txt.gz

    The columns record_type, restrictions, year_of_data and lane_of_travel were excluded
    as they did not contain very useful information

    i.e. record_type: 3 for all the rows
         restrictions: blank for all rows
         year_of_data: 15 for all the rows
         lane_of_travel: denotes which lane(s) the data was collected from (not very useful as
         its corresponds to either data with lanes combined, outside (rightmost) lane or 
         other lanes and logically, data with lanes combined should have a higher recorded 
         traffic volume as compared to the rest)
"""
traffic_columns = ['date',
                 'day_of_data',
                 'day_of_week',
                 'direction_of_travel',
                 'direction_of_travel_name',
                 'fips_state_code',
                 'functional_classification',
                 'functional_classification_name',
                 'month_of_data',
                 'station_id',
                 'traffic_volume_counted_after_0000_to_0100',
                 'traffic_volume_counted_after_0100_to_0200',
                 'traffic_volume_counted_after_0200_to_0300',
                 'traffic_volume_counted_after_0300_to_0400',
                 'traffic_volume_counted_after_0400_to_0500',
                 'traffic_volume_counted_after_0500_to_0600',
                 'traffic_volume_counted_after_0600_to_0700',
                 'traffic_volume_counted_after_0700_to_0800',
                 'traffic_volume_counted_after_0800_to_0900',
                 'traffic_volume_counted_after_0900_to_1000',
                 'traffic_volume_counted_after_1000_to_1100',
                 'traffic_volume_counted_after_1100_to_1200',
                 'traffic_volume_counted_after_1200_to_1300',
                 'traffic_volume_counted_after_1300_to_1400',
                 'traffic_volume_counted_after_1400_to_1500',
                 'traffic_volume_counted_after_1500_to_1600',
                 'traffic_volume_counted_after_1600_to_1700',
                 'traffic_volume_counted_after_1700_to_1800',
                 'traffic_volume_counted_after_1800_to_1900',
                 'traffic_volume_counted_after_1900_to_2000',
                 'traffic_volume_counted_after_2000_to_2100',
                 'traffic_volume_counted_after_2100_to_2200',
                 'traffic_volume_counted_after_2200_to_2300',
                 'traffic_volume_counted_after_2300_to_2400']


"""
    Columns to include when loading the data from dot_traffic_stations_2015.txt.gz
"""
station_columns = ['fips_county_code',
                 'fips_state_code',
                 'latitude',
                 'longitude',
                 'number_of_lanes_in_direction_indicated',
                 'number_of_lanes_monitored_for_traffic_volume',
                 'station_id',
                 'station_location',
                 'year_station_discontinued',
                 'year_station_established']


"""
    Mapping between fips state code and state abbreviation
    
    Obtained from: 
    https://gist.github.com/wavded/1250983/bf7c1c08f7b1596ca10822baeb8049d7350b0a4b
"""
fips_state_abb = {'01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA', 
                  '08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL', 
                  '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN', 
                  '19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME', 
                  '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS', 
                  '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH', 
                  '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND', 
                  '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI', 
                  '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT', 
                  '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI', 
                  '56': 'WY'}


"""
    Mapping between fips state code and full name of state
    
    Obtained from: 
    https://gist.github.com/wavded/1250983/bf7c1c08f7b1596ca10822baeb8049d7350b0a4b
"""
fips_state_full = {"01": "Alabama",
                   "02": "Alaska",
                   "04": "Arizona",
                   "05": "Arkansas",
                   "06": "California",
                   "08": "Colorado",
                   "09": "Connecticut",
                   "10": "Delaware",
                   "11": "District of Columbia",
                   "12": "Florida",
                   "13": "Georgia",
                   "15": "Hawaii",
                   "16": "Idaho",
                   "17": "Illinois",
                   "18": "Indiana",
                   "19": "Iowa",
                   "20": "Kansas",
                   "21": "Kentucky",
                   "22": "Louisiana",
                   "23": "Maine",
                   "24": "Maryland",
                   "25": "Massachusetts",
                   "26": "Michigan",
                   "27": "Minnesota",
                   "28": "Mississippi",
                   "29": "Missouri",
                   "30": "Montana",
                   "31": "Nebraska",
                   "32": "Nevada",
                   "33": "New Hampshire",
                   "34": "New Jersey",
                   "35": "New Mexico",
                   "36": "New York",
                   "37": "North Carolina",
                   "38": "North Dakota",
                   "39": "Ohio",
                   "40": "Oklahoma",
                   "41": "Oregon",
                   "42": "Pennsylvania",
                   "44": "Rhode Island",
                   "45": "South Carolina",
                   "46": "South Dakota",
                   "47": "Tennessee",
                   "48": "Texas",
                   "49": "Utah",
                   "50": "Vermont",
                   "51": "Virginia",
                   "53": "Washington",
                   "54": "West Virginia",
                   "55": "Wisconsin",
                   "56": "Wyoming"}


class TrafficUtils:
    """
        Perform basic data preprocessing and pickling for faster load times

        Args
        ----------
        traffic_path: str (Optional, default dot_traffic_2015.txt.gz)
                    file path to read from for the traffic dataset

        station_path: str (Optional, default dot_traffic_stations_2015.txt.gz)
                    file path to read from for the stations dataset      

        traffic_pkl: str (Optional, default dot_traffic_2015.pkl.gz)
                    pickle file path to save the traffic dataset to 

        station_pkl: str (Optional, default dot_traffic_stations_2015.pkl)
                    pickle file path to save the stations dataset to

        mapping_pkl: str (Optional, default dot_mappings_2015.pkl)
                    pickle file path to save the mappings to

        Returns
        ----------
        None
    """
    def __init__(self, 
                 traffic_path: str = "dot_traffic_2015.txt.gz", 
                 station_path: str = "dot_traffic_stations_2015.txt.gz",
                 traffic_pkl: str = "dot_traffic_2015.pkl.gz", 
                 station_pkl: str = "dot_traffic_stations_2015.pkl", 
                 mapping_pkl: str = "dot_mappings_2015.pkl") -> None:
        
        self.traffic = pd.read_csv(traffic_path, usecols=traffic_columns)
        self.station = pd.read_csv(station_path, usecols=station_columns)
        
        self.traffic = self.pad_fips_state(self.traffic, "fips_state_code")
        self.station = self.pad_fips_state(self.station, "fips_state_code")
        
        self.mappings = {"fips_state_abb": fips_state_abb,
                         "fips_state_full": fips_state_full}
        self.create_mappings()
        
        self.convert_to_pickle(traffic_pkl, station_pkl, mapping_pkl)
        
        
    @staticmethod
    def pad_fips_state(df: pd.DataFrame, fipscol: str) -> pd.DataFrame:
        """
            Convert fips_state_code to string and pad it with leading 0s
            to make it 2 digits long

            Args
            ----------
            df: pd.DataFrame
                        input dataframe
            
            fipscol: str
                        name of the column in the df that contains the fips_state_code

            Returns
            ----------
            df: pd.DataFrame
                        modified df with its fips_state_code stringed and padded 
        """
        # Add leading 0s to make fips_state_code 2 digits long
        df[fipscol] = df[fipscol].astype(str).str.zfill(2)
        
        return df
    
        
    def create_mappings(self) -> None:
        """
            Create mappings between the numerical encoding of categorical variables (i.e.
            direction_of_travel and functional_classification) and the full names of their
            categories

            Returns
            ----------
            None
        """
        # Create direction_of_travel: direction_of_travel_name mapping
        self.create_mapping(self.traffic, "direction_of_travel", "direction_of_travel_name")
        
        # Create functional_classification: functional_classification_name mapping
        self.create_mapping(self.traffic, "functional_classification", "functional_classification_name")
        
    
    def create_mapping(self, df: pd.DataFrame, keycol: str, valuecol: str, feature_name: str = None) -> None:
        """
            Creates mapping between the numerical encoding of the selected categorical variable and the
            full names of its categories

            Args
            ----------
            df: pd.DataFrame
                        input dataframe containing the categorical variables

            keycol: str
                        name of the column in df that contains the numerical encoding

            valuecol: str
                        name of the column in df that contains the full name of the category

            feature_name: str (Optional, default None)
                        key to use for saving the created mapping to master mappings 
                        (i.e. self.mappings[feature_name] = created_mapping)

            Returns
            ----------
            None            
        """
        # Drop duplicate rows based on both keycol and valuecol
        df_unique = df[[keycol, valuecol]].drop_duplicates()
        
        # Check for duplicate keys and values
        assert len(df_unique[keycol].unique()) == len(df_unique), "Duplicate keys detected"
        assert len(df_unique[valuecol].unique()) == len(df_unique), "Duplicate values detected"
        
        # Create dictionary based on key-value pairs
        mapping = dict(zip(df_unique[keycol].values, df_unique[valuecol].values))
        
        # Sort the dictionary based on keys
        sorted_mapping = dict(sorted(mapping.items()))
        
        feature_name = feature_name if feature_name else keycol
        assert feature_name not in self.mappings, f"The key {feature_name} is already in mappings"
        self.mappings[feature_name] = sorted_mapping
        
        # Drop the value column
        df.drop(columns=[valuecol], inplace=True)

    
    def convert_to_pickle(self, traffic_pkl: str, station_pkl: str, mapping_pkl: str) -> None:
        """
            Save the traffic dataset, stations dataset and mappings to pickle files

            Args:
            ----------
            traffic_pkl: str 
                        pickle file path to save the traffic dataset to 

            station_pkl: str 
                        pickle file path to save the stations dataset to

            mapping_pkl: str 
                        pickle file path to save the mappings to

            Returns
            ----------
            None
        """
        self.traffic.to_pickle(traffic_pkl)
        self.station.to_pickle(station_pkl)
        
        with open(mapping_pkl, "wb") as file:
            pickle.dump(self.mappings, file)


def load_data(traffic_pkl: str = "datasets/dot_traffic_2015.pkl.gz", 
              station_pkl: str = "datasets/dot_traffic_stations_2015.pkl", 
              mapping_pkl: str = "datasets/dot_mappings_2015.pkl",
              traffic_path: str = "datasets/dot_traffic_2015.txt.gz", 
              station_path: str = "datasets/dot_traffic_stations_2015.txt.gz"
              ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
        Load the pickled traffic dataset, stations dataset and mappings. 
        
        If the pickled files do not exist, then:

            1) Load the original text file datasets
            2) Perform basic preprocessing
            3) Pickle the datasets
            4) Try to load the pickled datasets again

        Args
        ----------
        traffic_pkl: str (Optional, default datasets/dot_traffic_2015.pkl.gz)
                    pickle file path to load the traffic dataset from

        station_pkl: str (Optional, default datasets/dot_traffic_stations_2015.pkl)
                    pickle file path to load the stations dataset from

        mapping_pkl: str (Optional, default datasets/dot_mappings_2015.pkl)
                    pickle file path to load the mappings from   

        traffic_path: str (Optional, default datasets/dot_traffic_2015.txt.gz)
                    text file path to read from for the original traffic dataset

        station_path: str (Optional, default datasets/dot_traffic_stations_2015.txt.gz)
                    text file path to read from for the original stations dataset

        Returns
        ----------
        (traffic, station, mappings): tuple of 3 pd.DataFrame
                    the traffic dataset, stations dataset and mappings
    """
    def load_pickle() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
            Load the pickled datasets

            Returns
            ----------
            (traffic, station, mappings): tuple of 3 pd.DataFrame
                    the traffic dataset, stations dataset and mappings
        """
        traffic = pd.read_pickle(traffic_pkl)
        station = pd.read_pickle(station_pkl)
        
        with open(mapping_pkl, "rb") as file:
            mappings = pickle.load(file)
            
        return traffic, station, mappings
    
    try:
        return load_pickle()
        
    except:
        # Perform basic preprocessing and pickle the traffic dataset, stations dataset and mappings
        TrafficUtils(traffic_path, station_path, traffic_pkl, station_pkl, mapping_pkl)
        return load_pickle()