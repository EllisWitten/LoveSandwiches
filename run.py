import gspread
from google.oauth2.service_account import Credentials

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
        print('Data should be six numbers, seperated by commas')
        print('Example: 21,63,54,26,85,49\n')

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


data = get_sales_data()
