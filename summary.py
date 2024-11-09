import csv
import os
from utils import monthly, budget_history, yearly_budget, prev_month, yearly, fetch_most_recent_purchase

def summarize():
    if (os.path.getsize(yearly) == 0) and (os.path.getsize(monthly) == 0) and (os.path.getsize(yearly_budget) == 0) and (os.path.getsize(budget_history) == 0):
        print("No recent purchases found. Enter new expense to record\n\n")
        return None
    print("\n--- DISPLAY MENU ---")
    while True:
        choice = int(input(
            "\n\n\t(1) CHECK MOST RECENT PURCHASE\n"
            "\t(2) VIEW THIS MONTH'S RECORDS\n"
            "\t(3) VIEW YEARLY RECORDS\n"
            "\t(4) VIEW PREVIOUS MONTH RECORDS\n"
            "\t(5) VIEW THIS MONTH'S BUDGET HISTORY"
            "\n\n\t(6) EXIT\n"))

        # Most recent purchase
        if choice == 1:
            if os.path.getsize("data/most_recent_purchase.csv") == 0:
                print("No recent purchases recorded. \n")
            else:
                recent_purchase = fetch_most_recent_purchase()
                print(f"Most recent purchase:\n\tNAME: {recent_purchase.name}\tCATEGORY: {recent_purchase.category}\tAMOUNT: {recent_purchase.amount}\n\n")

        # This month's records
        elif choice == 2:
            if os.path.getsize(monthly) == 0:
                print("No purchases made for this month yet\n")
            else:
                print("PURCHASES FOR THE MONTH\n")
                with open(monthly, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        print(' | '.join(row))

        # Yearly records
        elif choice == 3:
            if os.path.getsize(yearly) == 0:
                print("No recent purchases found.\n\n")
            else:
                print("PURCHASE HISTORY:\n")
                with open(yearly, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    print("\t EXPENSES | CATEGORIES | AMOUNT")
                    for row in reader:
                        print(' | '.join(row))

        # Previous month's records
        elif choice == 4:
            if os.path.getsize(prev_month) == 0:
                print("No records found for last month\n")
            else:
                print("PURCHASES FOR THE MONTH\n")
                with open(prev_month, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        print(' | '.join(row))

        # This month's budget history
        elif choice == 5:
            if os.path.getsize(budget_history) == 0:
                print("No budget records found for this month\n")
            else:
                print("BUDGET HISTORY FOR THE MONTH\n")
                with open(budget_history, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        print(' '.join(row))

        elif choice == 6:
            return  # Exit the loop and function

        else:
            print("Invalid option, please try again.")


