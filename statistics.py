import os
from utils import budget_history, yearly, yearly_budget, fetch_budget

from collections import defaultdict
import csv
from utils import monthly, display_frequent_purchases_yearly, display_frequent_purchases

def statistics():
    """MAIN MENU FOR STATISTICS"""
    while True:
        print("\n\n\t--- STATISTICS MENU ---")
        choice = int(input("\n\n\t1. DISPLAY EXPENSE STATISTICS FOR THIS MONTH"
                           "\n\t2. DISPLAY EXPENSE STATISTICS FOR THE YEAR"
                           "\n\n\t3. EXIT\n\n"))

        if choice == 1:
            # Check if monthly records exist and contain data
            if os.path.getsize(monthly) == 0:
                print("No purchases made for this month yet\n")
            else:
                calculate_monthly_stats() # Calculate and display monthly stats

        elif choice == 2:
            # Check if yearly records exist and contain data
            if os.path.getsize(yearly) == 0:
                print("No purchases made for this month yet\n")
            else:
                calculate_yearly_stats() # Calculate and display yearly stats

        elif choice == 3:
            print("Exiting Statistics Menu.")
            return # Exit the statistics menu

        else:
            print("Invalid option. Please try again.")

def calculate_monthly_stats():
    """CALCULATE STATS FOR THE MONTH. DISPLAY TOTAL SPENT BY CATEGORY AND BY DATE AND SUMMARIZE MONTH WITH TOTAL BUDGET, TOTAL SPENT, AND NET SPEND. DISPLAY ITEMS SPENT ON BY CATEGORY. DISPLAY FREQUENT PURCHASES."""
    # Dictionaries to hold monthly data and budget
    monthly_data = defaultdict(lambda: defaultdict(lambda: {'total':0, 'item': []})) # Create a three layer dictionary with month = {"date1" = {'total' = 0, 'item' = []}, "date2" = {'total' = 0, 'item' = []}, ... }
    purchase_date = None # The date of the purchase
    budget_data = defaultdict(int) # Create a date-wise dictionary with total spent for that date with budget_data = {"date1" = 0.0, "date2" = 0.0, ... }
    current_date = None # The date for iteration
    monthly_total = 0 #Total spent for the month

    print("\nParsing budget data for the month...\n")

    # If budget history is empty, use default budget values
    if os.path.getsize(budget_history) == 0:
        initial_budget, current_budget = fetch_budget()

    try:
        # Read and process budget data from budget history file
        with open (budget_history, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if row and '---------------------------------------------------------------' in row:
                    continue # Skip delimiter rows
                if row and len(row) == 1:
                    purchase_date = row[0] # Capture the date for the entry
                if row and len(row) >= 3:
                    if row[0] == '*':# Initial budget entry
                        initial_budget = float(row[1])
                        budget_data[purchase_date] += float(row[3])
                    else: # subsequent budget entry
                        budget_data[purchase_date] += float(row[2])

    except FileNotFoundError:
        print("Budget data not available. Please refresh budget and/or enter income \n")
        return

    print("\n Retrieving and processing entries for the month...\n")

    try:
        # Read and process monthly records for expense data
        with open(monthly, 'r', newline='') as csvfile:

            reader = csv.reader(csvfile)
            try:
                for row in reader:
                    if row and '---------------------------------------------------------------' in row:
                        continue# Skip delimiter rows

                    elif len(row) == 1:
                        current_date = row[0] # Date of expense

                    elif len(row) >= 3:
                        # Process each expense entry, summing totals by category, append expenses to a list sorted by category
                        print(f"\nProcessing entry for {current_date}...\n")
                        name, category, amount = row[0], row[1], float(row[2])
                        monthly_data[current_date][category]['total'] += amount
                        monthly_data[current_date][category]['item'].append(name)
                        monthly_total += amount

            except ValueError:
                print("\n Invalid date encountered. Skipping\n")

    except FileNotFoundError:
        print("Monthly records either have been reset or file is empty. Visit summaries for prior statistics\n")

    print("\nDAY-WISE FOR THIS MONTH:\n")
    # Display statistics by day for each category
    for current_date, categories in monthly_data.items():
        print(f"\t\t\t\t\t\t----DATE: {current_date}----\n")
        date_total = sum(cat['total'] for cat in categories.values()) # Sum the total expenditure or that date across all items and categories

        for category_name, data in categories.items():
            item_list = ', '.join(data['item']) # Append all the items per category to a list
            print(f"\t\t\t{category_name}:{data['total']}\t\tITEM EXPENSES : {item_list}") # Display the total and items by category

        print(f"\nTOTAL SPENT FOR THE DAY: {date_total}")
        if current_date in budget_data.keys():
            print(f"TOTAL INCOME FOR THE DAY: {budget_data[current_date]}")

        net_spend = budget_data[current_date] - date_total

        print(f"\nNET SPEND = {net_spend}\n\n")

    print("\nOVERALL STATISTICS FOR THE MONTH:\n")

    # Calculate and display overall monthly statistics
    b_total = calculate_month(monthly_data, budget_data) # Call function to calculate statistics for the entire month
    initial_budget += b_total # Total budget for the month

    print(f"\n\t Total spent for this month: {monthly_total}, Initial/Total budget: {initial_budget}")
    net = initial_budget - monthly_total
    print(f"\t\t\t\tNET SAVED FOR THE MONTH = {net}\n\n")

    # Display frequent purchases in the monthly summary
    display_frequent_purchases()

def calculate_month(monthly_data, budget_data):

    category_totals = defaultdict(float)
    budget_totals = 0

    for date, categories in monthly_data.items(): # Calculate the total for the month by category
        for category, data in categories.items():
            category_totals[category] += data['total']

    print("CATEGORY\t | \tTOTAL")
    for category, total in category_totals.items():
        print(f"{category}\t|\t{total}") # Display the total for the month by category

    for total in budget_data.values():
        budget_totals += total

    return budget_totals # Total income for the month

def calculate_yearly_stats():

    # Data structure to hold daily, monthly, and yearly data
    yearly_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'total': 0, 'items': []}))) # Create a 4 layer dictionary with year = {'month 1' : {"date1" = {'total' = 0, 'item' = []}, "date2" = {'total' = 0, 'item' = []}, ... }, 'month 2' : {"date1" = {'total' = 0, 'item' = []}, "date2" = {'total' = 0, 'item' = []}, ... }, ... }
    monthly_totals = defaultdict(float)
    yearly_total = 0.0
    budget_data = defaultdict(lambda: defaultdict(float)) # Create a two layer month-wise dictionary with total spent for that date with budget_data = {'month 1' : {"date1" = 0.0, "date2" = 0.0, ... }, 'month 2' : {"date1" = 0.0, "date2" = 0.0, ... }}
    initial_budget = 0.0

    # Parse budget data from the budget history file
    print("\nParsing budget data for the year...\n")
    try:
        if os.path.getsize(yearly_budget) == 0:
            initial_budget, current_budget = fetch_budget()
        with open(yearly_budget, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            current_date = None
            current_month = None

            for row in reader:

                if row and ('---------------------------------------------------------------' in row or "###############################################################" in row):
                    continue  # Skip lines with delimiters

                if row and len(row) == 1:  # Assuming it's a month or date
                    entry = row[0].strip()
                    if "-" not in entry:
                        current_month = entry  # Assign as month
                        print(f"THIS BETTER WORK BUDGET MONTH{current_month}")
                    else:
                        current_date = entry  # Assign as date
                        print(f"THIS BETTER WORK BUDGET DATE{current_date}")

                if row and len(row) >= 3:  # Actual data row
                    try:
                        if row[0] == '*':
                            initial_budget += float(row[1])
                            budget_data[current_month][current_date] = 0.0
                        else:
                            budget_data[current_month][current_date] += float(row[2])
                    except ValueError:
                        print("Invalid budget data. Skipping row.")

    except FileNotFoundError:
        print("Budget data not available. Please refresh budget or enter income.\n")
        return

    # Parse yearly expenses data
    print("\nRetrieving and processing entries for the year...\n")
    try:
        with open(yearly, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            current_date = None
            current_month = None

            for row in reader:
                if row and (
                        '---------------------------------------------------------------' in row or "###############################################################" in row):
                    continue  # Skip lines with delimiters

                if row and len(row) == 1:  # Assuming it's a month or date
                    entry = row[0].strip()
                    if "-" not in entry:
                        current_month = entry  # Assign as month
                        print(f"THIS BETTER WORK BUDGET MONTH{current_month}")
                    else:
                        current_date = entry  # Assign as date
                        print(f"THIS BETTER WORK BUDGET DATE{current_date}")

                if row and len(row) >= 3:
                    name, category, amount = row[0], row[1], float(row[2])
                    yearly_data[current_month][current_date][category]['total'] += amount
                    yearly_data[current_month][current_date][category]['items'].append(name)
                    monthly_totals[current_month] += amount
                    yearly_total += amount

    except FileNotFoundError:
        print("Yearly records are missing or the file is empty.\n")
        return

    # Day-wise and month-wise summary
    print("\nDAY-WISE AND MONTH-WISE SUMMARY FOR THE YEAR:\n")
    for month, days in yearly_data.items():
        print(f"\n########################################################################### MONTH: {month} ###########################################################################\n")
        month_total = 0

        for day, categories in days.items():
            print(f"\t\t\t\t\t\t----DATE: {day}----\n")
            day_total = 0

            for category_name, data in categories.items():
                items_list = ', '.join(data['items'])
                print(f"\t\t\t{category_name}: {data['total']} | Items: {items_list}")
                day_total += data['total']

            print(f"\n\t\t\tTotal Spent for {day}: {day_total:.2f}")
            print(f"\t\t\tincome for today: {budget_data[month][day]}")

            income = budget_data[month][day]
            net_spend = income - day_total
            print(f"\n\t\t\tNet Spend for {day}: {net_spend:.2f}\n")

            month_total += day_total

        print(f"\n\nTOTAL SPENT FOR THIS MONTH: {month_total:.2f}")
        print(f"INCOME FOR THE MONTH: {sum(budget_data[month][day] for day in days)}\n")

    # Yearly Summary
    print("\nYEARLY SUMMARY STATISTICS:\n")
    initial_budget += calculate_year(yearly_data, budget_data)
    yearly_net = initial_budget - yearly_total

    print(f"\nTotal Spent for the Year: INR {yearly_total:.2f}")
    print(f"Total Income for the Year: INR {initial_budget:.2f}")
    print(f"Net Saved for the Year: {yearly_net:.2f}\n")

    display_frequent_purchases_yearly()

def calculate_year(yearly_data, budget_data):
    """ Helper function to calculate category-wise yearly totals. """
    category_totals = defaultdict(float)
    budget_totals = 0.0

    for month, days in yearly_data.items():
        for day, categories in days.items():
            for category, data in categories.items():
                category_totals[category] += data['total']

    print("\nCATEGORY-WISE TOTAL FOR THE YEAR:\n")
    for category, total in category_totals.items():
        print(f"\t\t\t{category} | INR {total:.2f}")

    for month, day in budget_data.items():
        for total in day.values():
         budget_totals += total

    return budget_totals

