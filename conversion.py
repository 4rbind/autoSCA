import json
import csv
import os
import sys

# Aahai k ko jhilimili, aahai batti ko jhilimili
class style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    RESET = '\033[0m'

def convert_json_to_csv(json_file, csv_file):
    try:
        # Open the JSON file and load the data
        with open(json_file, 'r') as json_data:
            data = json.load(json_data)

        # Check if profiles exist and have control results
        if 'profiles' in data:
            profiles = data['profiles']
        else:
            print("No profiles found in JSON data.")
            return

        # Prepare a list to hold rows for CSV
        rows = []

        # Iterate through profiles and controls to extract data
        for profile in profiles:
            profile_name = profile.get('name', 'N/A')  # Extract profile name

            if 'controls' in profile:
                for control in profile['controls']:
                    control_id = control.get('id', 'N/A')
                    control_title = control.get('title', 'N/A')

                    if 'results' in control:
                        for result in control['results']:
                            result_status = result.get('status', 'N/A')
                            result_code_desc = result.get('code_desc', 'N/A')
                            result_run_time = result.get('run_time', 'N/A')
                            result_start_time = result.get('start_time', 'N/A')

                            # Append the row data for the CSV
                            rows.append({
                                'Profile': profile_name,
                                'Control ID': control_id,
                                'Control Title': control_title,
                                'Result Status': result_status,
                                'Code Description': result_code_desc,
                                'Run Time': result_run_time,
                                'Start Time': result_start_time,
                            })

        # If we have data to write to CSV, proceed
        if rows:
            # Open the CSV file for writing
            with open(csv_file, 'a', newline='') as csvfile:
                fieldnames = ['Profile', 'Control ID', 'Control Title', 'Result Status', 'Code Description', 'Run Time', 'Start Time']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the header and rows to the CSV
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)

            print(style.GREEN + f"CSV saved to:         {style.RESET}{csv_file}")
        else:
            print(style.RED + f"No control results found to write to CSV.")
    
    except json.JSONDecodeError as e:
        print(style.RED + f"Error decoding JSON: {e}")
    except Exception as e:
        print(style.RED + f"Unexpected error: {e}")

if __name__ == '__main__':
    # Check if correct number of arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python3 conversion.py <json_file> <csv_file>")
        sys.exit(1)

    # Get the input JSON file and output CSV file from command line arguments
    json_file = sys.argv[1]
    csv_file = sys.argv[2]

    # Convert JSON to CSV
    if os.path.exists(json_file):
        convert_json_to_csv(json_file, csv_file)
    else:
        print(style.RED + f"JSON file {json_file} not found.")

