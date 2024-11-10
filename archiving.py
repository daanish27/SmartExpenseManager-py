from utils import monthly, yearly, current_month, budget_history, yearly_budget, prev_month, prev_budget_history

import csv
import os
import shutil
from datetime import datetime


def archive_monthly_to_yearly():
    """ARCHIVE THE MONTH'S BUDGET AND EXPENSE ENTRIES INTO THE YEARLY FILE FOR EACH, SEPARATED BY THE CURRENT MONTH YEAR HEADER"""
    try:
        # Read the stored month from the file
        with open(current_month, 'r', newline='') as file:
            month_id = file.read().strip()

    except FileNotFoundError:
        # If the file doesn't exist, proceed as if the month has changed
        month_id = datetime.now().strftime("%B %Y")
        with open(current_month, 'w', newline='') as file:
            file.write(month_id.upper())

    if not os.path.exists(monthly):
        print("No monthly data available to archive.")
        return

    try:
        flag = 1
        if os.path.getsize(yearly) == 0:
            flag = 0 # Flag to initialize the first set budget of the year

        # Read from monthly records file and write to yearly records file
        with open(monthly, 'r') as monthly_file, open(yearly, 'a', newline='') as yearly_file:
            monthly_reader = csv.reader(monthly_file)
            yearly_writer = csv.writer(yearly_file)

            # Add the month header to the yearly file
            yearly_writer.writerow(["###############################################################"])
            yearly_writer.writerow([f"{month_id}"])
            yearly_writer.writerow(["###############################################################"])

            # Copy each row from the monthly file to the yearly file
            for row in monthly_reader:
                yearly_writer.writerow(row)

        # Read from monthly budget file and write to yearly budget file
        with open(budget_history, 'r') as monthly_file, open(yearly_budget, 'a', newline='') as yearly_file:
            monthly_reader = csv.reader(monthly_file)
            yearly_writer = csv.writer(yearly_file)

            # Add the month header to the yearly file
            yearly_writer.writerow(["###############################################################"])
            yearly_writer.writerow([f"{month_id}"])
            yearly_writer.writerow(["###############################################################"])

            # Copy each row from the monthly file to the yearly file
            for row in monthly_reader:
                if flag == 0 and len(row) >= 4: # This ensures that only the first entry of the first month is considered the initial entry later for calculation
                    yearly_writer.writerow([row[1], row[2], row[3]])
                    flag = 1

                elif flag == 1 and len(row) >= 4:
                    yearly_writer.writerow([row[1], row[2], row[3]])

                else:
                    yearly_writer.writerow(row)

        print(f"Monthly entries successfully archived for {month_id}.")

    except IOError:
        print("An error occurred while trying to read/write the monthly/yearly files.")

def monthly_update():
    """TRANSFER MONTHLY EXPENSE AND BUDGET DATA FROM CURRENT MONTH TO PREVIOUS MONTH. EMPTY BOTH FILES FOR NEW ENTRIES"""
    try:
        # Copy the source file to the target file
        shutil.copyfile(monthly, prev_month)
        shutil.copyfile(budget_history, prev_budget_history)
        print(f"Copied contents from {monthly} to {prev_month}.")

        # Remove the original file
        with open(monthly, 'w') as file:
            file.write('')
        with open(budget_history, 'w') as file:
            file.write('')
        print("Records for this month have been refreshed!")

    except IOError as e:
        print(f"An error occurred: {e}")
