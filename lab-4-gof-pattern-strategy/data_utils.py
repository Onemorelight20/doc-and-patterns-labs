import os
import csv
from faker import Faker
from constants import *


faker = Faker()

def generate_user_data(directory_name, num_rows, file_name):
    """Generate random user data and write to CSV file."""
    with open(os.path.join(directory_name, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('row_number', 'email', 'password_encoded', 'payer_cohort', 'first_name', 'last_name'))
        row_number = 1
        for _ in range(num_rows):
            email = faker.email() 
            email = email[:email.index('@')] + str(faker.random_number(digits=3)) + email[email.index('@'):]
            writer.writerow([
                row_number,
                email,
                faker.password(),
                faker.word(),
                faker.first_name(),
                faker.last_name()
            ])
            row_number += 1


def generate_data(directory_name=GENERATED_DATA_DIR):
    generate_user_data(directory_name, USER_DATA_ROWS_NUMBER, USER_DATA_FILE_NAME)


def delete_files(directory_name=GENERATED_DATA_DIR):
    """Delete CSV files."""
    for filename in os.listdir():
        file_path = os.path.join(directory_name, filename)
        os.remove(file_path)

def get_user_data_as_dict():
    data = []
    with open(os.path.join(GENERATED_DATA_DIR, USER_DATA_FILE_NAME), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

if __name__ == "__main__":
    os.makedirs(GENERATED_DATA_DIR, exist_ok=True)
    # delete_files()
    generate_data()
    # print(get_user_data_as_dict())
