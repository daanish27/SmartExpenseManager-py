import csv
import os
from purchase import Purchase
from collections import defaultdict, Counter

#Most recent expense data = most_recent_purchase.csv
monthly = os.path.join("data", "monthly_records.csv") # Current month expense data
prev_month = os.path.join("data", "previous_month.csv") # Previous month expense data
yearly = os.path.join("data", "yearly_records.csv" ) #Aggregated year-wise expense data

budget = os.path.join("data", "budget.csv") # Current budget data
budget_history = os.path.join("data", "budget_history.csv") # Current month budget and income history
prev_budget_history = os.path.join("data", "prev_month_budget.csv") # Previous month budget and income history
yearly_budget = os.path.join("data", "yearly_budget.csv") # Aggregated year-wise budget and income data

current_month = os.path.join("data", "current_month.txt") # The current month and year as MONTH YEAR to check for elapsed month

categories_file = os.path.join("data/categories.txt") # Persistent categories list
def load_categories():
    """OPEN AND READ CATEGORIES FILE TO LOAD INTO A LIST"""
    try:
        with open(categories_file, "r") as file:
            categories = [line.strip() for line in file]
    except FileNotFoundError:
        categories = []
    return categories
categories = load_categories() # Store categories in file to a list for access

def fetch_most_recent_purchase():
    """FETCH THE LAST RECORDED PURCHASE"""
    if not os.path.exists("data/most_recent_purchase.csv"):
        print("No recent purchases found.\n")
        return None
    with open("data/most_recent_purchase.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        row = next(reader, None)
        return Purchase(row[0], row[1], float(row[2])) if row else "No purchases have been recorded over this period \n" # Return name, category, amount

def fetch_budget():
    """FETCH THE TOTAL AND CURRENT BUDGET"""
    try:
        with open(budget, 'r', newline='') as csvfile:

            reader = list(csv.reader(csvfile))
            if not reader:
                print("\nNo entries found. Setting default Budget Values (INR 0)\n")
                return 0,0
            row = list(reader[0])
            return float(row[0]), float(row[1]) # Return budget amount or 0 if empty

    except FileNotFoundError:
        print("No budget data available. Default budget Values (INR 0) set\n")
        return 0,0

def display_frequent_purchases():
    """GET MOST FREQUENT PURCHASES OVER THE MONTH, STORE IN A DEFAULTDICT DICTIONARY AND RETURN"""
    if (os.path.getsize(monthly) == 0) or (os.path.getsize(monthly) == 0):
        return None
    print("\nMost Frequent Purchases by Category:\n")
    records = defaultdict(Counter)

    # Read monthly records and count occurrences
    if os.path.exists(monthly):
        with open(monthly, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if len(row) >= 3:
                    name, category = row[0].strip(), row[1].strip()
                    records[category][name] += 1

    # Display top items in each category
    for i, category in enumerate(categories):

        frequent_items = records[category].most_common(3)
        if not frequent_items:
            continue

        print(f"\nCategory: {category}")
        for idx, (name, count) in enumerate(frequent_items, start=1):
            if name is None:
                continue
            else:
                print(f"{idx}. {name} (purchased {count} times)")

    return records

def select_frequent_purchase():
    """FUNCTION TO DISPLAY MOST FREQUENT PURCHASES AND GIVE THE USER THE ABILITY TO AUTOFILL"""
    records = display_frequent_purchases()
    if records is None:
        return None
    choice = input("\nWould you like to enter a frequently purchased item automatically? (y/n): ").strip().lower()
    if choice != 'y':
        return None

    # Ask user to choose category for autofill
    print("\nSelect a category for auto-fill:")
    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat}")
    try:
        cat_choice = int(input("Enter category number: ")) - 1
        selected_category = categories[cat_choice]

        # Show most frequent items in selected category
        frequent_items = records[selected_category].most_common(3)

        # If no items purchased frequently under this category
        if not frequent_items:
            print("No frequent purchases found for this category.")
            return None

        # Autofill selection
        print("\nSelect an item to auto-fill:")
        for idx, (name, count) in enumerate(frequent_items, start=1):
            print(f"{idx}. {name} (purchased {count} times)")

        item_choice = int(input("Enter item number: ")) - 1

        if item_choice < 0 or item_choice >= len(frequent_items):
            print("Invalid choice. Returning to manual entry.")
            return None

        selected_name = frequent_items[item_choice][0]

        # Loop to enter purchase amount and check when the expense amount exceeds current budget
        while True:
            selected_amount = float(input("Enter purchase amount\n"))
            total, current = fetch_budget()

            # Check when the expense amount exceeds current budget
            if current - selected_amount < 0:
                choice = input(
                    f"Current budget INR{current} about to be exceeded by purchase amount INR{selected_amount} by INR{current - selected_amount}. Continue(c) or (r)re-enter?\n")
                if choice.lower() == "c":
                    break  # Proceed despite budget warning
                elif choice.lower() == "r":
                    continue  # Re-enter expense amount
                else:
                    print("Invalid choice. Please enter 'c' or 'r'\n")

            # If amount does not exceed current budget
            else:
                break

        # Confirm before proceeding with selected item
        confirm = input(
            f"\nConfirm auto-fill for {selected_name} in {selected_category} for INR {selected_amount}? (y/n): ").strip().lower()
        if confirm == 'y':
            return selected_name, selected_category, selected_amount
        else:
            print("Auto-fill canceled. Returning to manual entry.")
            return None

    except ValueError:
        print("Invalid value")
        return None

    except IndexError:
        print("Index out of range.")
        return None

def get_top_frequent_purchases_yearly():
    """GET MOST FREQUENT PURCHASES OVER THE YEAR, STORED IN A DEFAULTDICT AND RETURN"""
    # Dictionary to store purchase counts for each category
    category_counts = defaultdict(Counter)

    if not os.path.exists(yearly) or os.path.getsize(yearly) == 0:
        return {}

    try:
        with open(yearly, 'r') as yearly_file:
            reader = csv.reader(yearly_file)

            for row in reader:
                # Skip header rows or incomplete data
                if len(row) < 3 or row[0].startswith("---") or row[0].startswith("#"):
                    continue

                name, category, amount = row[0].strip(), row[1].strip(), row[2].strip()

                try:
                    amount = float(amount)
                    # Use (name, amount) tuple as key to track frequencies
                    category_counts[category][(name, amount)] += 1
                except ValueError:
                    continue  # Skip rows where amount conversion fails

        # Retrieve top 5 most frequent purchases for each category
        top_frequent_purchases = defaultdict()
        for category, items in category_counts.items():
            # Sort items by frequency in descending order and get top 5
            top_items = items.most_common(10)
            top_frequent_purchases[category] = [(name, amount, count) for (name, amount), count in top_items]

        return top_frequent_purchases

    except IOError:
        print("An error occurred while trying to read the yearly file.")
        return {}

def display_frequent_purchases_yearly():
    """DISPLAY THE MOST FREQUENT PURCHASES FOR THE YEAR"""
    frequent_yearly = get_top_frequent_purchases_yearly()
    if not frequent_yearly:
        print("No yearly data available for analysis.")
        return
    print("MOST FREQUENT PURCHASES FOR THE YEAR:\n\n")
    for i, category in enumerate(categories):
        if category not in frequent_yearly or not frequent_yearly[category]:
            continue
        print(f"\nCategory: {category}")
        for idx, (name, amount, count) in enumerate(frequent_yearly[category], start = 1):
            if name is None:
                continue
            else:
                print(f"{idx}. {name} - INR {amount} (purchased {count} times)")