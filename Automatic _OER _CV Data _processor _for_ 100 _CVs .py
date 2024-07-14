import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

def open_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # Drop all columns with names containing 'Unnamed'
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        print("CSV file successfully loaded and unnamed columns removed:")
        print(df.head())
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file is not a valid CSV.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_values_to_csv(file_path, new_data):
    try:
        df = open_csv(file_path)  # Use open_csv to load the CSV and remove unnamed columns
        df1 = pd.DataFrame(new_data)
        # Ensure new DataFrame df1 has the same columns as the existing DataFrame df
        for col in df.columns:
            if col not in df1.columns:
                df1[col] = None
        # Append the new data to the existing DataFrame
        updated_df = pd.concat([df1, df], ignore_index=True)
        # Save the updated DataFrame back to the CSV file
        updated_df.to_csv(file_path, index=False)
        print("New values added to the CSV file:")
        print(updated_df.head())
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file is not a valid CSV.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_E_RHE_column(file_path):
    try:
        df = open_csv(file_path)  # Use open_csv to load the CSV and remove unnamed columns
        required_columns = ['Potential', 'NHE', 'Constant', 'pH', 'Current', 'R']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Error: The required column '{col}' does not exist in the CSV file.")
        # Fill NaNs with the first available value for NHE, pH, Constant, R, and Area
        df['NHE'] = df['NHE'].fillna(method='ffill')
        df['pH'] = df['pH'].fillna(method='ffill')
        df['Constant'] = df['Constant'].fillna(method='ffill')
        df['R'] = df['R'].fillna(method='ffill')
        df['Area (cm^2)'] = df['Area (cm^2)'].fillna(method='ffill')
        # Calculate E(RHE)
        df['E(RHE)'] = df['Potential'] + df['NHE'] + df['Constant'] * df['pH'] - (df['Current'] * df['R'])
        # Rearrange columns to move E(RHE) after Current
        columns = df.columns.tolist()
        columns.remove('E(RHE)')
        columns.insert(columns.index('Current') + 1, 'E(RHE)')
        df = df[columns]
        # Save the DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
        print("E(RHE) column added to the CSV file:")
        print(df.head())
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file is not a valid CSV.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_current_density_column(file_path):
    try:
        df = open_csv(file_path)  # Use open_csv to load the CSV and remove unnamed columns
        required_columns = ['Current', 'Area (cm^2)']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Error: The required column '{col}' does not exist in the CSV file.")
        # Calculate Current Density
        df['Current Density'] = df['Current'] / df['Area (cm^2)']
        # Rearrange columns to move 'Current Density' after 'E(RHE)'
        columns = df.columns.tolist()
        columns.remove('Current Density')
        columns.insert(columns.index('E(RHE)') + 1, 'Current Density')
        df = df[columns]
        df.to_csv(file_path, index=False)
        print('Current Density column added to the CSV file:')
        print(df.head())
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file is not a valid CSV.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def inspect_columns(file_path):
    try:
        df = open_csv(file_path)  # Use open_csv to load the CSV and remove unnamed columns
        print("Columns in the CSV file:")
        print(df.columns)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file is not a valid CSV.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def parse_data(input_file, portion_size):
    """
    Parses data from input_file and splits it into portions.

    Args:
    input_file (str): Path to the input file containing the data.
    portion_size (int): Number of lines per portion.

    Returns:
    list: List of data portions.
    """
    with open(input_file, 'r') as file:
        data = file.readlines()
    # Split data into portions
    portions = [data[i:i + portion_size] for i in range(0, len(data), portion_size)]
    return portions

def write_to_csv(portions, output_prefix):
    """
    Writes portions of data into CSV files with headers "Potential" and "Current", shifting data down by one row.

    Args:
    portions (list): List of data portions.
    output_prefix (str): Path prefix where the output CSV files will be saved.
    """
    try:
        os.makedirs(output_prefix, exist_ok=True)  # Create output directory if it doesn't exist
        for idx, portion in enumerate(portions):
            output_file = os.path.join(output_prefix, f"output_part_{idx + 1}.csv")
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write headers
                writer.writerow(['Potential', 'Current'])  # Header line
                # Write data shifted down by one row
                for i in range(1, len(portion)):
                    line = portion[i].strip().split(',')
                    numeric_data = [convert_to_numeric(cell) for cell in line]
                    writer.writerow(numeric_data)
        print(f"Data successfully written to {len(portions)} CSV files in {output_prefix}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def convert_to_numeric(value):
    """
    Convert a string to a numeric value if possible.

    Args:
    value (str): The string value to convert.

    Returns:
    int/float/str: The numeric value or the original string if conversion is not possible.
    """
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        return value

def process_all_csv_files(directory, input_file_path):
    """
    Processes all CSV files in a directory, adding new values, E(RHE), Current Density.

    Args:
    directory (str): Directory path containing CSV files.
    input_file_path (str): Path to the input CSV file containing raw data.
    """
    try:
        # Parse the input CSV file into portions
        portions = parse_data(input_file_path, portion_size=2401)
        # Write portions to CSV files in the specified directory
        write_to_csv(portions, directory)
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                print(f"Processing file: {file_path}")
                # Inspect columns to check for correct column names
                inspect_columns(file_path)
                # New data to be added (as a dictionary)
                new_data = {
                    'NHE': [0.0385],
                    'pH': [13],
                    'Constant': [0.059],
                    'Area (cm^2)': [3.85E-02],
                    'R': [8.2]
                }
                # Add new values to the CSV file
                add_values_to_csv(file_path, new_data)
                # Add the E(RHE) column to the CSV file
                add_E_RHE_column(file_path)
                # Add Current Density Column to CSV file
                add_current_density_column(file_path)
                print(f"Finished processing file: {file_path}\n")
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def extract_data_from_csv(directory):
    """
    Extracts 'E(RHE)' and 'Current Density' from all CSV files in a directory.

    Args:
    directory (str): Path to the directory containing CSV files.

    Returns:
    dict: Dictionary where keys are filenames and values are DataFrames containing 'E(RHE)' and 'Current Density'.
    """
    dataframes = {}
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    # Sort files by numerical order in filenames
    csv_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    # Loop through sorted files
    for filename in csv_files:
        filepath = os.path.join(directory, filename)
        # Read CSV file into a DataFrame
        df = open_csv(filepath)  # Use open_csv to load the CSV and remove unnamed columns
        # Extract 'E(RHE)' and 'Current Density' columns if they exist
        if 'E(RHE)' in df.columns and 'Current Density' in df.columns:
            extracted_data = df[['E(RHE)', 'Current Density']]
            dataframes[filename] = extracted_data
    return dataframes

def save_to_excel(dataframes, output_excel_file):
    """
    Saves multiple DataFrames to an Excel file, each DataFrame in a separate sheet.

    Args:
    dataframes (dict): Dictionary of DataFrames to save, with keys as sheet names.
    output_excel_file (str): Path to the output Excel file.
    """
    with pd.ExcelWriter(output_excel_file) as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Data successfully saved to {output_excel_file}")

# Usage example
if __name__ == "__main__":
    input_file_path = #Enter directroy to where your CSV is 
    output_directory = #Enter the dicrectroy where you want your data to be saved to 
    output_excel_file = # Enter where you want the combined excel file to be keep this portiuon of the cod --> '\combined_data.xlsx'

    # Process all CSV files in the directory
    process_all_csv_files(output_directory, input_file_path)

    # Extract data from CSV files in the specified directory
    extracted_data = extract_data_from_csv(output_directory)

    # Save extracted data to an Excel file with each CSV as a new sheet
    save_to_excel(extracted_data, output_excel_file)
