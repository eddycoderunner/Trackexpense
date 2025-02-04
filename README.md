# Trackexpense

import datetime

def add_expense(expense_records):
    try:
        amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid input. Please enter a numeric value for the expense.")
        return

    now = datetime.datetime.now()
    expense_records.append({
        "datetime": now,
        "amount": amount
    })
    print(f"Expense of {amount} recorded on {now.strftime('%Y-%m-%d %H:%M:%S')}")

def total_expense_for_day(expense_records, day=None):
    if day is None:
        day = datetime.date.today()

    total = sum(
        record['amount']
        for record in expense_records
        if record['datetime'].date() == day   
    )
    return total

def main():
    expense_records = []

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add an expense")
        print("2. Show total expense for the day")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            add_expense(expense_records)
        elif choice == "2":
            today = datetime.date.today()
            total = total_expense_for_day(expense_records, today)
            print(f"\nTotal expense for {today}: {total}")
        elif choice == "3":
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
