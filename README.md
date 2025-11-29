# SMART EXPENSE MANAGER with Python

## Overview
The **Expense Tracker** project is a comprehensive Python-based tool for managing and analyzing personal or business expenses. It offers functionalities to set and update budgets, record expenses by category, view monthly and yearly summaries, and archive past records.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Project Structure](#project-structure)
4. [Modules Overview](#modules-overview)
5. [Functions Reference](#functions-reference)
6. [Contributing](#contributing)

## Installation

### Clone the Repository:
```bash
git clone https://github.com/daanish27/SmartExpenseManager-py.git
```
### Navigate to Project Directory:
```bash
cd SmartExpenseManager-py
```
### Install Dependencies:
Ensure that Python and the required libraries are installed.
```bash
pip install -r requirements.txt
```

## Usage
Run the program:
```bash
python main.py
```

Follow the interactive prompts to set budgets, record expenses, view statistics, and manage categories.

## Project Structure

- main.py: The entry point of the application. It handles the main menu and interaction flow.

- budget.py: Manages budget-related functions.

- expenses.py: Records new expenses and updates existing ones.

- categories.py: Manages expense categories.

- statistics.py: Provides monthly and yearly expense summaries and statistics.

- archiving.py: Archives monthly records to yearly data.

- utils.py: Contains utility functions and constants, such as file paths and frequently used operations.

## Modules Overview

### 1. main.py
Central script for user interaction and monthly checks.

main(): Runs the main expense tracker menu, checks for month updates, and calls functions based on user choice.

### 2. budget.py
Manages the budget, including setting, updating, and recording it.

set_budget(): Sets or modifies the budget based on user input.

### 3. expenses.py
   Records and manages expense entries.

get_expense(): Collects details of a new expense and records it.
record_purchase(recent_purchase, today, t): Saves the purchase data with timestamps.

### 4. categories.py
Allows users to manage categories for expense classification.

check_categories(): Ensures categories exist before usage.
modify_categories(): Menu for adding, modifying, or deleting categories.

### 5. statistics.py
Provides statistical summaries of expenses.

calculate_monthly_stats(): Aggregates and displays monthly expense data.
calculate_yearly_stats(): Aggregates and displays yearly expense data.

### 6. archiving.py
Archives monthly data to yearly records.

archive_monthly_to_yearly(): Moves monthly records to yearly archives.
monthly_update(): Prepares for a new month by resetting monthly files.

### 7. utils.py
Utility functions for file handling and reusable components.

fetch_budget(): Retrieves the most recent budget values.
display_frequent_purchases(): Displays the most frequent monthly purchases by category.
select_frequent_purchase(): Allows users to autofill a frequent purchase.

## Functions Reference

### main.py
main(): Main program loop displaying menu options and calling corresponding functions.

### budget.py
set_budget(): Prompts user to set or add to the budget, then writes the data to budget files.

### expenses.py
get_expense(): Main function for entering a new expense. It validates user inputs, fetches the current budget, and updates the budget.
record_purchase(recent_purchase, today, t): Records an expense entry into the monthly record, with date grouping.

### categories.py
check_categories(): Verifies the existence of categories and prompts the user to add categories if none exist.
modify_categories(): Menu-driven function for managing categories, allowing additions, deletions, and modifications.

### statistics.py
calculate_monthly_stats(): Parses monthly data and displays expenses by date and category with income and net spend information.
calculate_yearly_stats(): Aggregates and displays yearly statistics, including frequent yearly purchases.

### archiving.py
archive_monthly_to_yearly(): Copies monthly records into yearly archives, adding a month identifier.
monthly_update(): Backs up and clears monthly records to prepare for the new month.

### utils.py
fetch_budget(): Retrieves the last known budget values.
display_frequent_purchases(): Shows top recurring purchases within a month.
select_frequent_purchase(): Automates filling of common purchases from a category.
get_top_frequent_purchases_yearly(): Analyzes yearly data to list the most frequent purchases by category.

## Contributing

If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request with a description of your changes.

## Thank you for contributing!
