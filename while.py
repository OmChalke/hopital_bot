from datetime import datetime

expenses=[]

while True:
    try:
        date_str= input("enter date (YYYY-MM-DD): ")
        date= datetime.strptime(date_str, "%Y-%m-%d").date()

        noOfTimes= int(input("how many expenses do you want to add: "))
        for i in range(noOfTimes):
                print(f"adding expenses {i+1}")
                amount= float(input("enter amount: "))
                category= input("enter category: ")
                note= input("enter note: ")

                expenses.append({
                    "date": date,
                    "amount":amount,
                    "category":category,
                    "note": note
                })

        addMoreDate=input("do you want to add one more date? (yes/no):")
        if addMoreDate != "yes":
            break           
                        
    except ValueError:
        print("invalid info")

print("expense added: ", expenses)

totalexpense= input("do you want see the total expense of the day (yes/no): ")
if totalexpense == "yes":
    date_str= input("enter date (YYYY-MM-DD): ")
    searchdate= datetime.strptime(date_str, "%Y-%m-%d").date()
    total = 0
    for expense in expenses:
        if expense["date"] == searchdate:
            total += expense["amount"]
    print(f"\nTotal spent on {searchdate}: {total}")

monthtotal = input("\nDo you want to see total expense of a month? (yes/no): ")
if monthtotal== "yes":
    month= input("Enter month (YYYY-MM): ")
    totalmonth = 0
    for expense in expenses:
        if expense["date"].strftime("%Y-%m") == month:
            totalmonth += expense["amount"]
    print(f"Total spent in {month}: {totalmonth}")

mostExp= input("do you want to see most expensive item: (yes/no)")
if mostExp=="yes":
    if expenses:
        most_expensive = expenses[0]
        for expense in expenses:
            if expense["amount"] > most_expensive["amount"]:
                most_expensive = expense

        print("\n Most Expensive Expense:")
        print(f"Date: {most_expensive['date']}")
        print(f"Amount: ₹{most_expensive['amount']}")
        print(f"Category: {most_expensive['category']}")
        print(f"Note: {most_expensive['note']}")
    else:
        print("No expenses found.")

show_top_3_categories = input("do you want to see top 3 categories?: yes/no")
if show_top_3_categories == "yes":
    if expenses:
        total_of_categories = {}
        for expense in expenses:
            category = expense["category"]
            total_of_categories[category] = total_of_categories.get(category, 0) + expense["amount"]

        sort_categories = sorted(total_of_categories.items(), key=lambda x:x[1], reverse=True)

        print("top 3 categories: ")
        for i, (category, total) in enumerate(sort_categories[:3], start=1):
            print(f"{i}. {category} - ₹{total}")
    else:
        print("No expenses found.")