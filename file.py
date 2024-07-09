def user():
    comp_name = input("Enter the name of Company : ")
    symbol = input("Enter the symbol of the company : ")
    print("Select an option")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    time = int(input())

    if time == 1:
        daily_data(comp_name, symbol)
    
    if time == 2:
        weekly_data(comp_name, symbol)

    if time == 3:
        monthly_data(comp_name, symbol)
    
    else:
        int(input("Invalid option. Please enter again "))
    

def company():
    comp_name = input("Enter the name of your company.")
    symbol = input("Enter the symbol of your company.")
    open_price = int(input("Enter the opening price of your stock : "))
    close_price = int(input("Enter the closing price of your stock : "))
    low_price = int(input("Enter the lowest price of your stock : "))
    high_price = int(input("Enter the highest price of your stock : "))
    vol = int(input("Enter the volume of the stock traded"))


def daily_data(company_name, symbol):
    print(".")

def weekly_data(company, symbol):
    print(".")

def monthly_data(company, symbol):
    print(".")
    
    
    
    # while True:
    #     print("Main Menu")
    #     print("1) USER")
    #     print("2) COMPANY")
    #     print("Any other key to EXIT")

    #     try:
    #         type = int(input("Select your login mode : "))
    #     except ValueError:
    #         print("Exiting the program")
    #         break

    #     if type == 1:
    #         user()
    #     elif type == 2:
    #         company()
    #     else:
    #         print("Exiting the program")
    #         break
    
    
    
def user():
    while True:
        print("USER MENU")
        print("1) Register")
        print("2) Login")
        print("Any other key to go back to the main menu")
        action = input("Select an option : ")

        if action == '1':
            userAuth.user_register()
        elif action == '2':
            userAuth.user_login()
        else:
            break
    
def company():
    while True:
        print("COMPANY MENU")
        print("1) Register")
        print("2) Login")
        print("Any other key to go back to the main menu")
        action = input("Select an option : ")

        if action == '1':
            companyAuth.company_register()
        elif action == '2':
            companyAuth.company_login()
        else:
            break
