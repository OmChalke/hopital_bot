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
date_str= input("enter date (YYYY-MM-DD): ")

searchdate= datetime.strptime(date_str, "%Y-%m-%d").date()

total = 0

for expense in expenses:
     
     if expense["date"] == searchdate:
          total += expense["amount"]
print(f"\nTotal spent on {searchdate}: { total}")

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

show_top_3_categories= input ("do you want  to see top 3 categories?: yes/no")
if show_top_3_categories=="yes":

    total_of_categories= {}

    for expense in expenses:
        category = expense["category"]
        total_of_categories[category]= total_of_categories.get(category,0) + expense["amount"]

    sort_categories= sorted(total_of_categories.items(), key= lambda x:x[1],reverse = True)

print("top 3 categories: ")
for i, (category,total) in enumerate(sort_categories[:3], start=1):
     print(f"{i}.{category} - {total}")


report= input ("do you want to generate report?: yes/no")
if report=="yes":
    month = input("Enter month for report (YYYY-MM): ")

    month_expenses = [exp for exp in expenses if exp["date"].strftime("%Y-%m") == month]
    total_month = sum(exp["amount"] for exp in month_expenses)

    total_of_categories= {}

    for expense in month_expenses:
        category = expense["category"]
        total_of_categories[category] = total_of_categories.get(category, 0) + expense["amount"]


    sort_categories= sorted(total_of_categories.items(), key= lambda x:x[1],reverse = True)

    month_name = datetime.strptime(month, "%Y-%m").strftime("%B %Y")
    filename = f"report_{month.replace('-', '_')}.txt"
    
    if month_expenses:
        most_expensive_in_month = max(month_expenses, key=lambda x: x["amount"])
    else:
        most_expensive_in_month = {"note": "N/A", "amount": 0}


    report_lines = [
        f"Expense Report - {month_name}",
        "------------------------------------",
        f" Total Spent: ₹{total_month}",
        " Top Categories:"
    ]

    for i, (cat, amt) in enumerate(sort_categories[:3], 1):
        report_lines.append(f"{i}. {cat} - ₹{amt}")


    report_lines.append(f" Most Expensive Item: {most_expensive_in_month['note']} - {most_expensive_in_month['amount']}")
    report_lines.append(f" Saved to file: {filename}")

    report_content = "\n".join(report_lines)
    print("\n" + report_content)



