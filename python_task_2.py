import pandas as pd

df=pd.read_csv(r'D:\MapUp-Data-Assessment-F-main\MapUp-Data-Assessment-F-main\datasets\dataset-3.csv')

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    df = df.rename(columns={'id_start': 'ID_A', 'id_end': 'ID_B', 'distance': 'Distance'})

    # Create a DataFrame with unique locations (IDs) as both index and columns
    locations = sorted(list(set(df['ID_A'].unique()) | set(df['ID_B'].unique())))
    distance_matrix = pd.DataFrame(0, index=locations, columns=locations)

    # Populate the distance matrix with cumulative distances along known routes
    for _, row in df.iterrows():
        id_a = row['ID_A']
        id_b = row['ID_B']
        distance_ab = row['Distance']

        # Update the distance matrix for both directions (A to B and B to A)
        distance_matrix.loc[id_a, id_b] += distance_ab
        distance_matrix.loc[id_b, id_a] += distance_ab

    # Set diagonal values to 0
    for i in locations:
        distance_matrix.loc[i, i] = 0

    return distance_matrix



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df = pd.melt(df, id_vars=df.columns[0], var_name='id_end', value_name='distance')

    unrolled_df = unrolled_df.rename(columns={df.columns[0]: 'id_start'})

    unrolled_df = unrolled_df.sort_values(by=['id_start', 'id_end']).reset_index(drop=True)

    return unrolled_df

    


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_df = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_average_distance = reference_df['distance'].mean()

    # Calculate the threshold for 10% of the reference_id's average distance
    threshold = 0.1 * reference_average_distance

    # Find IDs whose average distance is within the specified threshold
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= (reference_average_distance - threshold)) &
                          (result_df['distance'] <= (reference_average_distance + threshold))]

    # Sort the DataFrame based on average distance
    result_df = result_df.sort_values(by='distance')

    return result_df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    # Write your logic here
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    return df
    

def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    time_ranges = [
        {'start_time_range': time(0, 0, 0), 'end_time_range': time(10, 0, 0), 'discount_factor': 0.8},
        {'start_time_range': time(10, 0, 0), 'end_time_range': time(18, 0, 0), 'discount_factor': 1.2},
        {'start_time_range': time(18, 0, 0), 'end_time_range': time(23, 59, 59), 'discount_factor': 0.8}
    ]

    # Apply time-based toll rates based on the defined time ranges
    for time_range in time_ranges:
        mask = (df['start_time'] >= time_range['start_time_range']) & (df['end_time'] <= time_range['end_time_range'])
        df.loc[mask, 'discount_factor'] = time_range['discount_factor']

    # Apply constant discount factor for weekends
    weekend_mask = (df['start_day'].isin(['Saturday', 'Sunday']))
    df.loc[weekend_mask, 'discount_factor'] = 0.7

    # Calculate toll rates based on time-based discount factors
    df['toll_rate'] = df['distance'] * df['discount_factor']

    return df


