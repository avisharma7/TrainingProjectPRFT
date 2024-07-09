from data.conn import mydb, mycursor
from controllers.user.analysis import analyze_company, compare_companies

def user_analysis():
    mycursor.execute('SELECT symbol, name FROM companies')
    companies = {symbol: name for symbol, name in mycursor.fetchall()}

    while True:
        print("Menu:")
        print("1. Analyze one company")
        print("2. Compare two companies")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Please choose a company from the list below:")
            for symbol, name in companies.items():
                print(f"{symbol}: {name}")
            company_symbol = input("Enter the symbol of the company you want to analyze: ").lower()

            if company_symbol in companies:
                analyze_company(company_symbol, companies[company_symbol])
            else:
                print("Invalid company symbol. Please try again.")

        elif choice == '2':
            print("Please choose two companies from the list below:")
            for symbol, name in companies.items():
                print(f"{symbol}: {name}")
            symbol1 = input("Enter the symbol of the first company: ").lower()
            symbol2 = input("Enter the symbol of the second company: ").lower()

            if symbol1 in companies and symbol2 in companies:
                compare_companies(symbol1, symbol2, companies)
            else:
                print("Invalid company symbol(s). Please try again.")

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")