import os
import pandas

def create_new_dataset_from_result(dataset_file_name, data):
    # Get the full path of the dataset file
    dataset_path = load_dataset_path(dataset_file_name)

    # Save the new DataFrame to the specified dataset file
    save_new_dataframe(dataset_path, data)

def load_dataset_path(file_name):
    # Get the directory of the current script (assuming this is part of a script or module)
    feature_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the "dataset" directory, which is assumed to be one level above the script's directory
    dataset_dir = os.path.join(feature_dir, "..", "datasets")

    # Combine the dataset directory path with the specified file name to get the full file path
    file_path = os.path.join(dataset_dir, file_name)

    # Return the full path to the dataset file
    return file_path

def save_new_dataframe(dataset_path, df):
    # Save the DataFrame to the specified dataset file using a semicolon as the separator and excluding the index
    df.to_csv(dataset_path, sep=";", index=False)
