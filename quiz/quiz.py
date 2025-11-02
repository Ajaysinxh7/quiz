import os, random, datetime

def register():
    print("=== Registration ===")
    enroll = input("Enter Enrollment Number: ")
    pwd = input("Enter Password: ")
    name = input("Enter Full Name: ")
    email = input("Enter Email: ")
    branch = input("Enter Branch: ")
    year = input("Enter Year: ")
    contact = input("Enter Contact: ")
    with open("users.txt", "a") as f:
        f.write(f"{enroll},{pwd},{name},{email},{branch},{year},{contact}\n")
    print("Registration Successful")

def login():
    print("=== Login ===")
    enroll = input("Enter Enrollment Number: ")
    pwd = input("Enter Password: ")
    if enroll == "admin" and pwd == "admin":
        admin_menu()
        return
    if not os.path.exists("users.txt"):
        print("No users found.")
        return
    with open("users.txt", "r") as f:
        for line in f:
            data = line.strip().split(",")
            if len(data) >= 2 and data[0] == enroll and data[1] == pwd:
                print(f"Welcome {data[2]}")
                quiz_menu(enroll)
                return
    print("Invalid credentials")

def admin_menu():
    while True:
        print("=== ADMIN MENU ===")
        print("1. View All Users  2. View Scores  3. Exit")
        ch = input("Enter choice: ")
        if ch == "1":
            if os.path.exists("users.txt"):
                print(open("users.txt").read())
            else:
                print("No users yet")
        elif ch == "2":
            if os.path.exists("scores.txt"):
                print(open("scores.txt").read())
            else:
                print("No scores yet")
        elif ch == "3":
            break
        else:
            print("Invalid choice")

def quiz_menu(enroll):
    while True:
        print("=== QUIZ MENU ===")
        print("1. Attempt Quiz  2. View Score  3. Profile  4. Update Profile  5. Logout")
        ch = input("Enter choice: ")
        if ch == "1":
            attempt_quiz(enroll)
        elif ch == "2":
            show_score(enroll)
        elif ch == "3":
            show_profile(enroll)
        elif ch == "4":
            update_profile(enroll)
        elif ch == "5":
            break
        else:
            print("Invalid choice")

def attempt_quiz(enroll):
    print("Choose Category:")
    print("1. DSA")
    print("2. DBMS")
    print("3. PYTHON")
    ch = input("Enter choice (1-3): ")
    if ch == "1":
        cat = "dsa"
    elif ch == "2":
        cat = "dbms"
    elif ch == "3":
        cat = "python"
    else:
        print("Invalid choice.")
    if not os.path.exists("quizzes.txt"):
        print("Quizzes file not found")
        return

    # Parse quizzes.txt
    with open("quizzes.txt", "r") as f:
        content = f.read()
    quizzes = {}
    current_cat = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('[CATEGORY:'):
            current_cat = line[len("[CATEGORY:"):].strip("] \n").lower()
            quizzes[current_cat] = []
        elif current_cat and '|' in line:
            parts = line.split('|')
            if len(parts) == 6:
                quizzes[current_cat].append(parts)

    if cat not in quizzes:
        print("Category not found")
        return
    questions = quizzes[cat]
    if not questions:
        print("No questions found")
        return

    random.shuffle(questions)
    score = 0
    total = min(10, len(questions))
    for i in range(total):
        q = questions[i]
        print(f"Q{i+1}. {q[0]}")
        for j in range(1, 5):
            print(f"{j}. {q[j]}")
        ans = input("Your answer (1-4): ")
        if ans.isdigit() and 1 <= int(ans) <= 4 and q[int(ans)] == q[5]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer: {q[5]}")
    with open("scores.txt", "a") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{enroll},{cat},{score}/{total},{now}\n")
    print(f"Your Score: {score}/{total}")

def show_score(enroll):
    found = False
    if not os.path.exists("scores.txt"):
        print("No scores found")
        return
    with open("scores.txt", "r") as f:
        for line in f:
            data = line.strip().split(",")
            if len(data) >= 4 and data[0] == enroll:
                print(f"Category: {data[1]}  Score: {data[2]}  Time: {data[3]}")
                found = True
    if not found:
        print("No scores available")

def show_profile(enroll):
    if not os.path.exists("users.txt"):
        print("No users registered yet.")
        return
    with open("users.txt", "r") as f:
        for line in f:
            data = line.strip().split(",")
            if data[0] == enroll:
                print(f"Enrollment: {data[0]}  Name: {data[2]}  Email: {data[3]}  Branch: {data[4]}  Year: {data[5]}  Contact: {data[6]}")
                return
    print("Profile not found")

def update_profile(enroll):
    if not os.path.exists("users.txt"):
        print("No users found.")
        return
    lines = []
    with open("users.txt", "r") as f:
        lines = f.readlines()
    with open("users.txt", "w") as f:
        for line in lines:
            data = line.strip().split(",")
            if data[0] == enroll:
                data[2] = input("Enter new name: ")
                data[3] = input("Enter new email: ")
                data[4] = input("Enter new branch: ")
                data[5] = input("Enter new year: ")
                data[6] = input("Enter new contact: ")
                f.write(",".join(data) + "\n")
            else:
                f.write(line)
    print("Profile Updated")

def main():
    while True:
        print("=== MAIN MENU ===")
        print("1. Registration  2. Login  3. Exit")
        ch = input("Enter choice: ")
        if ch == "1":
            register()
        elif ch == "2":
            login()
        elif ch == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

main()
