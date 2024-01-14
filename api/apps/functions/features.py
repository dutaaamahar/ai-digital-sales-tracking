from datetime import datetime
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from ..apps import AppsConfig
from ..libraries import utils

def build_pivot(data):
    # Create a cross-tabulation of sales_name and pipeline_status
    pivot_sales = pd.crosstab(index=data['sales_name'], columns=data['pipeline_status'])

    # Calculate the total count of pipeline_status for each sales_name
    pivot_sales['count_pipeline_status'] = (
        pivot_sales['L1'] + pivot_sales['L2'] + pivot_sales['L3'] + pivot_sales['L4']
    )

    # Calculate the sum of total_payment for pipeline_status 'L4' for each sales_name
    df_l4_sum = data[data['pipeline_status'] == 'L4'].groupby('sales_name')['total_payment'].sum()

    # Join the sum_payment_L4 column to the pivot_sales dataframe
    pivot_sales = (
        pivot_sales
        .join(df_l4_sum, on='sales_name')
        .rename(columns={'total_payment': 'sum_payment_L4'})
        .fillna(0)
    )

    # Convert sum_payment_L4 to int64
    pivot_sales['sum_payment_L4'] = pivot_sales['sum_payment_L4'].astype('int64')

    # Scale sum_payment_L4 to a range between 0 and 1000 using Min-Max scaling
    scaler = MinMaxScaler(feature_range=(0, 1000))
    pivot_sales['sum_sales_success_point'] = (
        scaler.fit_transform(pivot_sales[['sum_payment_L4']])
        .astype('int64')
    )

    # Sort the pivot_sales dataframe based on sum_payment_L4 in descending order
    pivot_sales_sorted = pivot_sales.sort_values(by='sum_payment_L4', ascending=False)

    return pivot_sales_sorted

def tracking_per_sales_staff(request):
    try:
        # Get the current date in the format YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")

        # Get the model from the AppsConfig class
        model = AppsConfig.tracking_per_sales_staff_model

        # Generate the output file name for the dataset
        dataset_output_file_name = f'dataset_tracking_per_sales_staff_{current_date}.csv'

        # Read the input data from the request
        input_df = pd.read_csv(request.get('request'))

        # Transform the input data into a pivot table
        pivot_df = build_pivot(input_df)

        # Drop unnecessary columns from the pivot table
        columns_to_drop = ['count_pipeline_status', 'sum_payment_L4', 'sum_sales_success_point']
        pivot_filtered = pivot_df.drop(columns=columns_to_drop)

        # Make predictions using the model on the filtered pivot table
        output = model.predict(pivot_filtered)

        # Process the prediction results
        result = process_result(pivot_filtered, output)

        # Build a new dataframe using the original pivot table and the processed results
        df = build_dataframe(pivot_df, result)

        # create a new dataset from the dataframe and save it to a CSV file
        utils.create_new_dataset_from_result(dataset_output_file_name, df)

        # Return the result
        return result

    except Exception as e:
        # Handle exceptions and print an error message
        print(f"Error: {e}")
        return str(e)

def process_result(x, pred):
    # Set a threshold for success
    threshold = 1000

    # Initialize an empty list to store the results
    results = []

    # Loop through the data
    for idx in range(len(x)):
        # Calculate success rate based on the prediction score and threshold
        score = pred[idx]
        success_rate = score / threshold
        success_rate = round(success_rate * 100, 2)

        # Ensure success rate is not negative
        if success_rate <= 0:
            success_rate = 0

        # Create a dictionary with sales information
        data = {
            'sales_name': x.index[idx],
            'success_rate': success_rate,
            'information': (
                f"Sales {x.index[idx]} berhasil menjual produk M-Knows dengan "
                f"tingkat kesuksesan penjualan sebesar {success_rate}%. "
                f"Dimana sales tersebut berhasil mendapatkan klien sebanyak "
                f"{x['L1'].iloc[idx] + x['L2'].iloc[idx] + x['L3'].iloc[idx] + x['L4'].iloc[idx]}, "
                f"dengan rincian sebagai berikut: "
                f"L1 = {x['L1'].iloc[idx]}, L2 = {x['L2'].iloc[idx]}, "
                f"L3 = {x['L3'].iloc[idx]} dan L4 = {x['L4'].iloc[idx]}."
            )
        }

        # Append the data to the results list
        results.append(data)

    # Return the list of results
    return results

def build_dataframe(pivot_df, result):
    # Create a DataFrame from the result list
    df = pd.DataFrame(result)

    # Set the index of the DataFrame to match the index of the pivot_df
    df.set_index(pivot_df.index, inplace=True)

    # Return the DataFrame
    return df
