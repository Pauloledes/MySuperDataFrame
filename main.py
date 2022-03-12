from typing import List, Union, TypeVar
import treefiles as tf
import pandas as pd

T = TypeVar("T", bound="MySuperDF")


class MySuperDF(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_csv(cls, *args, **kwargs):
        return cls(pd.read_csv(*args, **kwargs))

    # def get_numeric_data(self):
    #     my_numerical_data = []
    #     for i, j in zip(self.dtypes, self.columns):
    #         if i == 'float64':
    #             my_numerical_data.append(j)
    #     return self[my_numerical_data]
    #
    # def get_bool_data(self):
    #     my_bool_data = []
    #     for i, j in zip(self.dtypes, self.columns):
    #         if i == 'bool':
    #             my_bool_data.append(j)
    #     return self[my_bool_data]
    #
    # def get_object_data(self):
    #     my_object_data = []
    #     for i, j in zip(self.dtypes, self.columns):
    #         if i == 'object':
    #             my_object_data.append(j)
    #     return self[my_object_data]
    @property
    def filter_numeric(self):
        return filter_df(self, 'float64')

    @property
    def filter_bool(self):
        return filter_df(self, 'bool')

    @property
    def filter_object(self):
        return filter_df(self, 'object')

    @property
    def filling_rate(self) -> T:
        results = pd.DataFrame(columns=['missing_values', 'filling_rate'])

        #  Count of rows
        nb_rows = self.shape[0]

        # for each feature
        for column in self.columns:

            # Count of the values on each column
            values_count = self[column].count()

            # Computing missing values
            missing_values = nb_rows - values_count

            # Computing filling rates
            filling_rate = values_count / nb_rows

            # Adding a row in the results' dataframe
            results.loc[column] = [missing_values, filling_rate]

        # Sorting the features by number of missing_values
        return MySuperDF(results.dropna(subset=['filling_rate']))




    # POSSIBLE_TYPES = {'numeric': 'float64', 'bool': 'bool', 'object': 'object'}
    #
    # def __getattr__(self, item):
    #     y = item[7:]
    #     print(y)
    #     if item.startswith('filter_') and y in self.POSSIBLE_TYPES:
    #         return filter_df(self, self.POSSIBLE_TYPES[y])
    #     else:
    #         return super().__getattribute__(item)


def filter_df(df, selected_type:Union[str, List[str]]) -> T:
    my_data = []
    for i, j in zip(df.dtypes, df.columns):
        if i in tf.get_iterable(selected_type):
            my_data.append(j)
    return MySuperDF(df[my_data])
