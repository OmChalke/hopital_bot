# Predefined subjects (you can change these)
# subjects = ["Math", "Science", "English"]

# Initialize an empty dictionary to store student data
students = {}

# Function to calculate grade based on average marks
def calculate_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 75:
        return 'B'
    elif average >= 50:
        return 'C'
    else:
        return 'D'

# Input the number of students
num_students = int(input("Enter number of students: "))

# Collect data for each student
for i in range(num_students):
    print(f"\nStudent {i+1}:")
    name = input("Enter student name: ")
    math=int(input("Enter the number of marks in maths: "))
    Science=int(input("Enter the number of marks in Sci: "))
    English=int(input("Enter the number of marks in Eng: "))
    # for subject in subjects:
    #     mark = float(input(f"Enter marks for {subject}: "))
    #     marks[subject] = mark
    
    # Calculate average
    average = (math+Science+English)//3
    print("avg marks ", average)
    
    # Determine grade
    grade =calculate_grade(average)
    print("grade ",grade)
    
    students[name]={
        'name': name,
        'math': math,
        'science': Science,
        'english': English
    }
    
    for student
    # Store student data
    # students[name] = {
    #     'marks': marks,
    #     'average': average,
    #     'grade': grade
    # }

# print("\nStudent Performance Report:")

# for name, data in students.items():
#     print(f"\nStudent Name: {name}")
  
    
#     for subject, mark in data['marks'].items():
#         print(f"{subject}: {mark}")
    
#     print(f"\nAverage Marks: {data['average']:.2f}")
#     print(f"Grade: {data['grade']}")


