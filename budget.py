from utils import fetch_budget, budget, budget_history
from datetime import datetime

import csv
import os

print("\n--- SET/REFRESH BUDGET ---\n\n")
def set_budget():

    """SET NEW BUDGET OR ADD AMOUNT TO EXISTING BUDGET"""
    total_budget, current_budget = fetch_budget()  # Fetch the current budget values
    print(f"Current Budget: INR {current_budget}")

    while True:
        try:
        # Choose to replace or add to the current budget
            choice = input("Do you want to (r)eplace and refresh budget or (a)dd to the budget? (r/a): \n\n or enter exit to go back \n\n").lower()

            if choice == 'exit':
                print("\nExiting to the main menu...\n")
                return

            if choice.lower() == 'r':
                add_amount = float(input("Enter the new budget amount: \n"))
                total_budget = current_budget = add_amount
                break

            elif choice.lower() == 'a':
                add_amount = float(input("Enter the amount to add: \n"))
                current_budget += add_amount
                prev_total_budget = total_budget # Prev total budget value is stored to check difference with refreshed value
                total_budget += add_amount
                break

            else:
                print("\nINVALID CHOICE ENTERED. ENTER EITHER 'a' OR 'r' \n")
                # Record the updated budget in the file

        except ValueError:
            print("Invalid input. Please enter a valid number for the budget amount.")

    # Write updated budget to file
    with open(budget, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([total_budget, current_budget])

    # Append budget history if history file exists
    today = datetime.now().date()
    flag = 0 # Flag to check if today's entry exists

    # For subsequent budget entries in the month
    if os.path.exists(budget_history):

        with open(budget_history, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if not row or "------------------------" in row:
                    continue
                if len(row) == 1 and row[0] == str(today):
                    flag = 1
                    break

        with open(budget_history, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if flag == 0:
                writer.writerow(["---------------------------------------------------------------"])
                writer.writerow([today])

            if choice.lower() == 'r':
                difference = add_amount - prev_total_budget
                writer.writerow([total_budget, current_budget, difference])

            else:
                writer.writerow([total_budget, current_budget, add_amount])

    # For the first budget entry of the month, denoted by using *
    else:
        with (open(budget_history, 'w', newline='') as csvfile):
            writer = csv.writer(csvfile)
            writer.writerow(["---------------------------------------------------------------"])
            writer.writerow([today])

            if choice.lower() == 'r':
                difference = add_amount - total_budget
                add_amount - total_budget
                writer.writerow(['*',total_budget, current_budget, difference])

            else:
                writer.writerow(['*',total_budget, current_budget, add_amount])

    print(f"\nTotal Budget: INR {total_budget}")
    print(f"Updated Budget: INR {current_budget}\n")