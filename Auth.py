def user():
    print("\tUSER LOGIN")
    comp_name = input("Enter the name of Company : ")
    symbol = (input("Enter the symbol of the company : ")).upper()
    print("Select an option")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    time = int(input())

    if time == 1:
        daily_data(comp_name, symbol)
    
    elif time == 2:
        weekly_data(comp_name, symbol)

    elif time == 3:
        monthly_data(comp_name, symbol)
    
    else:
        int(input("Invalid option. Please enter again : "))
        



def company():
    print("\tCOMPANY LOGIN")
    comp_name = input("Enter the name of your company : ")
    symbol = input("Enter the symbol of your company : ")
    open_price = int(input("Enter the opening price of your stock : "))
    close_price = int(input("Enter the closing price of your stock : "))
    low_price = int(input("Enter the lowest price of your stock : "))
    high_price = int(input("Enter the highest price of your stock : "))
    vol = int(input("Enter the volume of the stock traded :  "))


def daily_data(company_name, symbol):
    print(".")

def weekly_data(company, symbol):
    print(".")

def monthly_data(company, symbol):
    print(".")

def main_menu():
    while True:
        print("\nMain Menu")
        print("USER")
        print("COMPANY")
        print("EXIT")
        type = (input("Select your login mode : ")).upper()


        if type == "USER":
            user()
        
        elif type == "COMPANY":
            company()

        elif type == "EXIT":
            print("Exiting the program")
            break

        else:
            print("Invalid choice. Enter again.")


if __name__ == "__main__":
    main_menu()
        

            
