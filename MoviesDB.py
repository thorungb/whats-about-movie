import numpy as np
import pandas as pd


class MoviesDB:
    def __init__(self):
        self.movies_database = None

    def read_file(self):
        self.movies_database = pd.read_csv('imdb_top_1000.csv')
        return self.movies_database


class DataManage:
    def __init__(self):
        self.movies_db = pd.DataFrame(MoviesDB().read_file())
        self.MDdf = self.movies_db.copy()
        self.preprocessing()

    def exploration(self):
        # shape of data
        print('The shape of the dataset is: ', self.MDdf.shape, '\n')
        # data types of each column
        print(self.MDdf.info())
        # summary statistics
        print('\nSummary statistics: \n', self.MDdf.describe())
        # missing values of each column
        print('\nMissing values:\n', self.MDdf.isnull().sum())

    def preprocessing(self):
        # convert 'Gross' column to numeric (removing commas)
        self.MDdf['Gross'] = self.MDdf['Gross'].str.replace(',', '')
        self.MDdf['Gross'] = self.MDdf['Gross'].replace(np.nan, 0)
        self.MDdf['Gross'] = self.MDdf['Gross'].astype(int)
        # rename 'Series_Title' to 'Title'
        self.MDdf = self.MDdf.rename(columns={'Series_Title': 'Title'})
        # extracting numeric values from 'Runtime' column
        self.MDdf['Runtime'] = self.MDdf['Runtime'].str.extract(r'(\d+)', expand=False).astype(int)
        self.MDdf = self.MDdf.rename(columns={'Runtime': 'Runtime (minutes)'})
        # convert 'Released_Year' column to numeric (removing commas)
        self.MDdf['Released_Year'] = pd.to_numeric(self.MDdf['Released_Year'], errors='coerce')
        self.MDdf = self.MDdf.dropna(subset=['Released_Year'])
        self.MDdf['Released_Year'] = self.MDdf['Released_Year'].astype(int)
        # create 'casts' column
        self.MDdf['Casts'] = (self.MDdf[['Star1', 'Star2', 'Star3', 'Star4']]
                              .apply(lambda x: ','.join(x.dropna()), axis=1))
        # check data types of each column again
        # print(self.MDdf.info())
