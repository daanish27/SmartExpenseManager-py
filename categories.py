from utils import categories_file, categories


def check_categories():
    """CHECK IF LIST OF CATEGORIES HAS ENTRIES"""
    if not categories:
        print("CATEGORIES LIST EMPTY. ENTER AT LEAST ONE PURCHASE CATEGORY\n")
        add_category()

    return categories

def save_categories():
    """SAVE ENTRIES TO FILE FOR DATA PERSISTENCE BETWEEN SESSIONS"""
    with open(categories_file, "w") as file:
        file.writelines(f"{cat}\n" for cat in categories)

def modify_categories():
    """MAIN MENU FOR CATEGORY MANIPULATION"""
    while True:

        check_categories() # Ensure categories are initialized

        print("\n--- CATEGORIES MENU ---\n")
        choice = int(input(f"CURRENT CATEGORIES: {categories}\n\n"
                           "\t1. ENTER NEW CATEGORY\n"
                           "\t2. DELETE CATEGORY\n"
                           "\t3. MODIFY CATEGORY\n\n"
                           "\t4. EXIT\n"))

        if choice == 1:
            add_category()

        elif choice == 2:
            delete_category()

        elif choice == 3:
            modify_category()

        elif choice == 4:
            if not categories: # Check if categories list is empty before exiting
                print("Categories list empty. Please enter categories\n")
                add_category()
            return

def add_category():
    """ADD A CATEGORY/CATEGORIES"""
    add_cat = [] # Temporary list to hold new categories for display

    while True:

        new_category = input("\nCategory name: ").strip().upper()
        categories.append(new_category)
        add_cat.append(new_category)
        save_categories()  # Save categories to file after each addition

        choice = input("\nEnter more categories? (y/n): ").strip().lower()
        if choice == "n":
            print("\nNEW CATEGORIES ADDED:\n")
            for cat in add_cat:
                print(cat)
            break
        elif choice != "y":
            print("\nInvalid option. Exiting to MAIN MENU\n")
            return

def delete_category():
    """DELETE A CATEGORY"""
    del_category = input("Enter category name to delete: ").strip().upper()
    if del_category in categories:
        categories.remove(del_category)
        save_categories()  # Save categories to file after deletion
        print("CATEGORY REMOVED\n")
    else:
        print("Category does not exist\n")

def modify_category():
    """MODIFY A CATEGORY"""
    mod_category = input("Enter category name to modify: ").strip().upper()
    if mod_category in categories:
        new_category = input("Enter new category name: ").strip().upper()
        categories[categories.index(mod_category)] = new_category
        save_categories()  # Save updated categories to file
        print("CATEGORY MODIFIED\n")
    else:
        print("Category does not exist\n")
