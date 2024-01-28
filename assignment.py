import pandas as pd

def analyze_work_data(file_path):
    """Analyzes the Excel file and prints relevant employee information."""
    
    # Read Excel file using pandas
    df = pd.read_excel(file_path)

    # Assumptions:
    # - "Time" and "Time Out" columns contain datetime objects or strings convertible to datetimes.
    # - "Employee Name" and "Position ID" columns contain unique identifiers for each employee.

    # Find employees who have worked 7 consecutive days
    consecutive_days_employees = find_consecutive_days(df)
    print("\nEmployees who have worked 7 consecutive days:")
    print(consecutive_days_employees[['Employee Name', 'Position ID']])

    # Find employees with short breaks between shifts
    short_breaks_employees = find_short_breaks(df)
    print("\nEmployees with short breaks between shifts:")
    print(short_breaks_employees[['Employee Name', 'Position ID']])

    # Find employees with long shifts
    long_shifts_employees = find_long_shifts(df)
    print("\nEmployees with long shifts:")
    print(long_shifts_employees[['Employee Name', 'Position ID']])

def find_consecutive_days(df):
    # Assuming 'Time' column contains datetime objects or strings convertible to datetimes
    df['Date'] = pd.to_datetime(df['Time']).dt.date
    
    # Group by 'Employee Name', 'Position ID', and 'Date' to count consecutive days
    consecutive_days_employees = df.groupby(['Employee Name', 'Position ID', 'Date']).size().reset_index(name='ConsecutiveDays')
    
    # Filter employees who have worked 7 consecutive days
    consecutive_days_employees = consecutive_days_employees[consecutive_days_employees['ConsecutiveDays'] >= 7]
    
    return consecutive_days_employees

def find_short_breaks(df):
    # Assuming 'Time Out' column contains datetime objects or strings convertible to datetimes
    df['Time Out'] = pd.to_datetime(df['Time Out'])
    
    # Calculate time difference between shifts
    df['Time Difference'] = df.groupby(['Employee Name', 'Position ID'])['Time Out'].diff()
    
    # Filter employees with less than 10 hours between shifts but greater than 1 hour
    short_breaks_employees = df[(df['Time Difference'] > '1:00:00') & (df['Time Difference'] < '10:00:00')]
    
    return short_breaks_employees

def find_long_shifts(df):
    # Assuming 'Time' column contains datetime objects or strings convertible to datetimes
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Filter employees who have worked more than 14 hours in a single shift
    long_shifts_employees = df[df['Time'].dt.hour > 14]
    
    return long_shifts_employees

# Get file path from user input
file_path = input("Enter the file path: ")

# Analyze the file
analyze_work_data(file_path)
