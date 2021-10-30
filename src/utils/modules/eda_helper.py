import pandas as pd
import numpy as np
from math import floor

"""[summary]
Class for EDA Operations
Returns:
    [type]: [description]
"""
class EDA:
    data_types = ['bool', "int_", "int8", "int16", "int32", "int64", "uint8", "uint16",
                 "uint32", "uint64", "float_","float16", "float32", "float64" ]
    
    @staticmethod
    def five_point_summary(dataframe):
        """[summary]
        Return 5 Point Summary For Given  Dataset
        Args:
            dataframe ([type]): [description]

        Returns:
            [type]: DataFrame/ Exception
        """
        my_dict = {'Features': [], 'Min': [], 'Q1': [], 'Median': [], 'Q3': [],
                    'Max': []}
        for column in dataframe.select_dtypes(include=np.number).columns:
            try:
                column_data=dataframe[pd.to_numeric(dataframe[column], errors='coerce').notnull()][column]
                q1 = np.percentile(column_data, 25)
                q3 = np.percentile(column_data, 75)
                
                my_dict['Features'].append(column)
                my_dict['Min'].append(np.min(column_data))
                my_dict['Q1'].append(q1)
                my_dict['Median'].append(np.median(column_data))
                my_dict['Q3'].append(q3)
                my_dict['Max'].append(np.max(column_data))

            except Exception as e:
                print(e)

        return pd.DataFrame(my_dict).sort_values(by=['Features'], ascending=True)
    
    @staticmethod
    def correlation_report(dataframe,method='pearson'):
        try:
            return dataframe.corr(method=method)
        except Exception as e:
                print(e)
    
    @staticmethod
    def get_no_records(dataframe,count=100,order='top'):
        try:
            if order=='top':
                return dataframe.head(count)
            else:
                return dataframe.tail(count)
        except Exception as e:
                print(e)
                
    @staticmethod       
    def find_dtypes(df3):
        l = []
        for i in df3.columns:
            yield str(df3[i].dtypes)
            
    @staticmethod                
    def find_median(df3):
        for i in df3.columns:
            if df3[i].dtypes in EDA.data_types:
                yield str(round(df3[i].median(), 2))
            else:
                yield str('-')  
                
    @staticmethod
    def find_mode(df3):
        l = []
        for i in df3.columns:
            yield str(df3[i].mode()[0])

    @staticmethod
    def find_mean(df3):
        for i in df3.columns:
            if df3[i].dtypes in EDA.data_types:
                yield str(round(df3[i].mean(), 2))
            else:
                yield str('-') 
                         
    @staticmethod            
    def missing_cells_table(df):
        df = df[[col for col in df.columns if df[col].isnull().any()]]

        missing_value_df = pd.DataFrame({
                                            'Column':df.columns,
                                            'Missing values': df.isnull().sum(),
                                            'Missing values (%)': (df.isnull().sum()/ len(df)) * 100,
                                            'Mean': EDA.find_mean(df),
                                            'Median': EDA.find_median(df),
                                            'Mode': EDA.find_mode(df),
                                            'Datatype': EDA.find_dtypes(df)
                                            }).sort_values(by='Missing values',ascending=False)
        return missing_value_df
    
    @staticmethod
    def outlier_detection_iqr(dataframe,lower_bound=25,upper_bound=75):
        my_dict = {'Features': [], f'IQR ({lower_bound}-{upper_bound})': [], 'Q3 + 1.5*IQR': [], 'Q1 - 1.5*IQR': [], 'Upper outlier count': [],
                   'Lower outlier count': [], 'Total outliers': [], 'Outlier percent': []}
        for column in dataframe.select_dtypes(include=np.number).columns:
            try:
                upper_count = 0
                lower_count = 0
                q1 = np.percentile(dataframe[column].fillna(dataframe[column].mean()), lower_bound)
                q3 = np.percentile(dataframe[column].fillna(dataframe[column].mean()), upper_bound)
                IQR = round(q3 - q1)
                upper_limit = floor(q3 + (IQR * 1.5))
                lower_limit = round(q1 - (IQR * 1.5))

                for element in dataframe[column].fillna(dataframe[column].mean()):
                    if element > upper_limit:
                        upper_count += 1
                    elif element < lower_limit:
                        lower_count += 1

                my_dict['Features'].append(column)
                my_dict[f'IQR ({lower_bound}-{upper_bound})'].append(IQR)
                my_dict['Q3 + 1.5*IQR'].append(upper_limit)
                my_dict['Q1 - 1.5*IQR'].append(lower_limit)
                my_dict['Upper outlier count'].append(upper_count)
                my_dict['Lower outlier count'].append(lower_count)
                my_dict['Total outliers'].append(upper_count + lower_count)
                my_dict['Outlier percent'].append(round((upper_count + lower_count) / len(dataframe[column]) * 100, 2))

            except Exception as e:
                print(e)

        return pd.DataFrame(my_dict).sort_values(by=['Total outliers'], ascending=False)
    
    @staticmethod
    def z_score_outlier_detection(dataframe):
        my_dict = {"Features": [], "Mean": [], "Standard deviation": [], 'Upper outlier count': [],
                   'Lower outlier count': [], 'Total outliers': [], 'Outlier percent': []}

        for column in dataframe.select_dtypes(include=np.number).columns:
            try:
                upper_outlier = 0
                lower_outlier = 0
                col_mean = np.mean(dataframe[column].fillna(dataframe[column].mean()))
                col_std = np.std(dataframe[column].fillna(dataframe[column].mean()))

                for element in dataframe[column].fillna(dataframe[column].mean()):
                    z = (element - col_mean) / col_std
                    if z > 3:
                        upper_outlier += 1
                        continue
                    elif z < -3:
                        lower_outlier += 1

                my_dict["Features"].append(column)
                my_dict["Mean"].append(col_mean)
                my_dict["Standard deviation"].append(col_std)
                my_dict["Upper outlier count"].append(upper_outlier)
                my_dict["Lower outlier count"].append(lower_outlier)
                my_dict["Total outliers"].append(upper_outlier + lower_outlier)
                my_dict["Outlier percent"].append(round((upper_outlier + lower_outlier) / len(dataframe[column]) * 100, 2))

            except Exception as e:
                print(e)
        df=pd.DataFrame(my_dict).sort_values(by=['Total outliers'], ascending=False).reset_index()
        return df