from utils import fetch_budget, current_month
from budget import set_budget
from expenses import get_expense
from summary import summarize
from categories import check_categories, modify_categories
from statistics import statistics, calculate_monthly_stats
from archiving import archive_monthly_to_yearly, monthly_update

import os
from datetime import datetime

print("\n\n\tE\tX\tP\tE\tN\tN\tS\tE\t\t\tT\tR\tA\tC\tK\tE\tR")

def main():
    # Get the current month as 'MONTH YEAR'
    month = datetime.now().strftime("%B %Y")  # Current month in 'MONTH YYYY' format

    # Check if current month file is empty, if so, write the current month
    if os.path.getsize(current_month) == 0:
        with open(current_month, 'w', newline='') as file:
            file.write(month)

    try:
        # Read the stored month from the file
        with open(current_month, 'r', newline='') as file:
            stored_month = file.read().strip()

    except FileNotFoundError:
        # If the file doesn't exist, proceed as if the month has changed
        stored_month = None

    # Check if the stored month is different from the current month
    if stored_month != month:
        # If months are different or file doesn't exist, perform updates
        print("\nMonth has elapsed. Archiving the month's RECORDS and displaying statistics\n")
        print("\nCALCULATING MONTHLY STATS\n")
        calculate_monthly_stats() # Calculate stats for the last month
        print("\nARCHIVING...\n") # Archive records
        archive_monthly_to_yearly() # Refresh monthly records
        print("\nUPDATING MONTHLY\n")
        monthly_update()
        with open(current_month, 'w', newline='') as file:
            file.write(month)

    check_categories() # Ensure categories are initialized

    # Infinite loop for user interaction until program exit
    while True:

        total_budget, current_budget = fetch_budget()
        print(f"\n\n\t\tTOTAL BUDGET FOR PERIOD: {total_budget}\t\t REMAINING BUDGET: {current_budget}")

        choice = int(input("\n\n\t\t\t\t\t\t\t\t------------------ENTRY------------------\n\n"
                           "\n\n1. SET BUDGET\t\t\t\t"
                           "2. ENTER EXPENSE\t\t\t\t"
                           "3. CATEGORIES\t\t\t\t\n\n\n"
                           "\t\t\t\t\t\t\t\t------------------EXPENSE ANALYSES------------------"
                           "\n\n4. VIEW EXPENSE SUMMARIES\t\t\t\t"
                           "5. VIEW EXPENSE STATISTICS\n"
                           "\n6. EXIT\n\n"))
        match choice:
            case 1:
                set_budget() # Set or update budget
            case 2:
                get_expense() # Add an expense entry
            case 3:
                modify_categories() # Modify category list
            case 4:
                summarize() # View summaries
            case 5:
                statistics() # View statistics
            case 6:
                print("Exiting the program.")
                return
            case _:
                choice = input("Invalid option. Did you want to EXIT instead?(y/n)\n")
                if choice == "y":
                    return

# Run main function if script is executed directly
if __name__ == "__main__":
    main()