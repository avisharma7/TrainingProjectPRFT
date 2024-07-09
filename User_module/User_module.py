# main.py
from db_operations import fetch_companies_from_db
from analysis import analyze_company, compare_companies

def main():
    companies = fetch_companies_from_db()

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

if __name__ == '__main__':
    main()
