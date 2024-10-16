def menu():
    print("[1] Option 1")
    print("[2] Option 2")
    print("[3] Option 3")
    print("[0] Exit the program.")

def option3():
    print("Option 3 has been called using a function!")

menu()
option = int(input("Enter your option..."))

while option != 0:
    if option == 1:
        print("Option 1 has been called!")
    elif option == 2:
        print("Option 2 has been called!")
    elif option == 3:
        option3()
    else:
        print("Invalid option!")

    print()
    menu()
    option = int(input("Enter your option..."))

print("thanks for using this program, goodbye!")