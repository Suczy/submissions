import pandas as pd

df=pd.read_csv(r'/datasets/dataset-1.csv')
def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix = pd.DataFrame(index=df['id_1'].unique(), columns=df['id_2'].unique())
    for _, row in df.iterrows():
        id_1 = row['id_1']
        id_2 = row['id_2']
        car_matrix.loc[id_1, id_2] = row['car']

    car_matrix.values[[i for i in range(len(car_matrix))], [i for i in range(len(car_matrix))]] = 0
    return car_matrix
    


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_counts = df['car_type'].value_counts().to_dict()
    return  dict(sorted(type_counts.items()))
    


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    bus_indexes.sort()
    return bus_indexes

    


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_means = df.groupby('route')['truck'].mean()
    filtered_routes = route_means[route_means > 7].index.tolist()
    filtered_routes.sort()
    return filtered_routes




def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.copy()
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix



def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df=pd.read_csv(r'/datasets/dataset-2.csv')
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')
    df = df.dropna(subset=['start_timestamp', 'end_timestamp'])
    df['duration'] = df['end_timestamp'] - df['start_timestamp']
    result = df.groupby(['id', 'id_2']).apply(lambda group: (group['duration'].max() >= pd.Timedelta(days=1) - pd.Timedelta(seconds=1)) and (group['start_timestamp'].dt.dayofweek.nunique() == 7))
    return result

