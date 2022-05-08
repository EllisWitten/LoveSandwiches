import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, seperated by commas.')
        print('Example: 21,63,54,26,85,49.\n')

        data_str = input('Enter your data here:')
        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('Data is valid')
            break

    return sales_data


def validate_data(values):
    """
    Converts all the data values can be converted into integers.
    Checks that there are 6 numbers.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
        return False
    return True

def calculate_surplus_data(sales_row):
    """
    Compare slaes with stock and calculate surplus data
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []

    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(data,worksheet):
    """
    Takes a list of integers and a worksheet name and
    updates the appropriate worksheet.
    """
    print(f'Updating {worksheet.capitalize()} worksheet...\n')
    spec_worksheet = SHEET.worksheet(worksheet)
    spec_worksheet.append_row(data)
    print(f'{worksheet.capitalize()} worksheet updated successfully.\n')
def get_last_five_entries():
    """
    collects columns of sata from the sales sheet,
    collecting the last 5 entries for each sandwich
    """
    sales =  SHEET.worksheet('sales')
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    print('Calculating stock data...')
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average *1.1
        new_stock_data.append(round(stock_num))
    print('Stock data calculated succesfully')

    return new_stock_data
def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    get_last_five_entries()
    sales_columns = get_last_five_entries()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')

print('Welcome to Love Sandwiches Data Automation.\n')
main()