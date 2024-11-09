import csv
import os
from purchase import Purchase
from datetime import datetime
from utils import categories, budget, fetch_budget, monthly, display_frequent_purchases, select_frequent_purchase

def get_expense():

    """GET EXPENSES EITHER FROM AUTOFILL OR MANUAL ENTRY. THESE DEDUCT FROM THE CURRENT BUDGET AND WRITE TO MOST RECENT PURCHASE FILE. RECORD TO FILES FUNCTION IS CALLED"""
    # Check for frequently purchased items for easy entry
    auto_fill = select_frequent_purchase()

    # If user has chosen automatic entry of a frequent purchase
    if auto_fill:
        expense_name, purchase_category, expense_amount = auto_fill
        n_purchase = Purchase(expense_name.upper(), purchase_category.upper(), expense_amount)

        try:
            # Update budget values after expense
            total, current = fetch_budget()
            with open(budget, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                current = current - expense_amount
                writer.writerow([total, current])
        except IOError:
            print("Error writing to budget file.\n")
            return None

        # Get date and time of the purchase
        today = datetime.now().date()
        n_current_time = datetime.now().time()
        print(f"date = {today}, time = {n_current_time}\n")

        # Save the purchase to the most recent purchases file
        try:
            with open("data/most_recent_purchase.csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["NAME", "CATEGORY", "AMOUNT", "TIME"])
                writer.writerow([n_purchase.name, n_purchase.category, n_purchase.amount, n_current_time])
        except IOError:
            print("Error writing to the most recent purchases file.")
            return None

        # Record to monthly records with date grouping
        record_purchase(n_purchase, today, n_current_time)

        return

    # Manual expense entry if no auto-fill selected
    else:
        try:
            # User inputs expense name
            expense_name = input("\n\t\t\t\t\t --------- EXPENSE ENTRY --------- \n\nEnter NAME OF EXPENSE\n (or enter 'exit' to cancel): \n").strip()
            if expense_name.lower() == 'exit':
                return None

            # Enter expense amount and ensure it's within the budget
            try:
                while True:
                    expense_amount = float(input("Enter AMOUNT\n (or enter 'exit' to cancel): \n"))
                    total, current = fetch_budget()
                    if current - expense_amount < 0:
                        choice = input(f"Current budget INR{current} about to be exceeded by purchase amount INR{expense_amount} by INR{current - expense_amount}. Continue(c) or (r)re-enter?\n")
                        if choice.lower() == "c":
                            break  # Proceed despite budget warning
                        elif choice.lower() == "r":
                            continue  # Re-enter expense amount
                        else:
                            print("Invalid choice. Please enter 'c' or 'r'\n")
                    break

            except ValueError:
                print("Invalid amount entered. Please enter a numeric value.")
                return None

            # Select expense category from predefined categories
            print("Select a category:\n")
            for i, cat in enumerate(categories):
                print(f"{i + 1}. {cat}\n")

            try:
                category_input = int(input("CATEGORY [1-5] (or 'exit' to cancel): \n")) - 1
                purchase_category = categories[category_input]
            except (ValueError, IndexError):
                print("Invalid category selection. Please enter a number between 1 and 5.\n")
                return None

            # Confirm expense details before recording
            confirm = input(
                f"\nExpense is {expense_name.upper()} in category {purchase_category.upper()} for INR {expense_amount}. Confirm? (y/n)\n").lower()

            if confirm == "y":
                # Record purchase to file if confirmed
                n_purchase = Purchase(expense_name.upper(), purchase_category.upper(), expense_amount)

                try:
                    # Update budget file after confirming expense
                    with open(budget, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        current = current - expense_amount
                        writer.writerow([total, current])
                except IOError:
                    print("Error writing to budget file.")
                    return None

                # Get date and time of the purchase
                today = datetime.now().date()
                n_current_time = datetime.now().time()
                print(f"date = {today}, time = {n_current_time}\n")

                # Save the purchase to the most recent purchases file
                try:
                    with open("data/most_recent_purchase.csv", 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["NAME", "CATEGORY", "AMOUNT", "TIME"])
                        writer.writerow([n_purchase.name, n_purchase.category, n_purchase.amount, n_current_time])
                except IOError:
                    print("Error writing to the most recent purchases file.")
                    return None

                # Record to monthly with date grouping
                record_purchase(n_purchase, today, n_current_time)

                return

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

def record_purchase(recent_purchase, today, t):
    """PURCHASES ARE RECORDED TO THE MONTHLY FILE"""
    flag = 0 # To check if today's date header is already present

    # If monthly records exist and have data
    if monthly and os.path.getsize(monthly)>0:

        with open(monthly, 'r', newline = '') as csvfile:

            csvfile.seek(0)
            reader = csv.reader(csvfile)

            for row in reader:
                if row and row[0] == str(today):
                    flag = 1

        # Append new entry under today's date if it already exists
        with open(monthly, 'a', newline='') as csvfile:

            csvfile.seek(0)
            writer = csv.writer(csvfile)

            if flag == 0:
                writer.writerow(["---------------------------------------------------------------"])
                writer.writerow([today]) # Write date header

            writer.writerow([recent_purchase.name, recent_purchase.category, recent_purchase.amount, t])

        print(f"\nEXPENSE RECORDED:\n\n\tNAME = {recent_purchase.name}\tCATEGORY = {recent_purchase.category}\tAMOUNT = {recent_purchase.amount}\n\n\t\tDATE = {today}\t\tTIME = {t}")


    else:

        # Create a new monthly file with date header if it doesn't exist
        with open(monthly, 'w', newline='') as csvfile:

            writer = csv.writer(csvfile)
            writer.writerow([today])
            writer.writerow([recent_purchase.name, recent_purchase.category, recent_purchase.amount, t])
