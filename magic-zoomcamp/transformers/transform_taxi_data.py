if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    """
    Transformer block to clean data and add a new column.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        A cleaned and transformed DataFrame.
    """
    # Remove rows where the passenger count is 0 or the trip distance is 0
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # Rename columns from Camel Case to Snake Case
    data.columns = [col.lower() for col in data.columns]
    data.rename(columns=lambda x: x.replace('id', '_id'), inplace=True)

    print(f"There are {data['passenger_count'].isin([0]).sum()} rows with zero passengers")
    print(f"There are {data['trip_distance'].isin([0]).sum()} rows with zero trip distance")

    return data

@test
def test_output(output, *args) -> None:
    """
    Test code for validating the transformations.
    """
    # Assertion to ensure no rides with zero passengers
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    # Assertion to ensure no rides with zero trip distance
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero trip distance'
    # Assertions for `vendor_id` values, assuming the existing values are known
    assert output['vendor_id'].isin([1, 2]).all(), 'Vendor ID values are not valid'
    # Ensure passenger_count is greater than 0
    assert (output['passenger_count'] > 0).all(), 'There are invalid passenger counts'
    # Ensure trip_distance is greater than 0
    assert (output['trip_distance'] > 0).all(), 'There are invalid trip distances'
