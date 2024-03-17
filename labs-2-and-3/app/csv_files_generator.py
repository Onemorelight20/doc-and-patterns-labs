import os
import csv
from faker import Faker
from constants import *


faker = Faker()

def generate_user_data(directory_name, num_rows, file_name):
    """Generate random user data and write to CSV file."""
    with open(os.path.join(directory_name, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['email', 'password_encoded', 'payer_cohort', 'first_name', 'last_name'])
        for _ in range(num_rows):
            email = faker.email() 
            email = email[:email.index('@')] + str(faker.random_number(digits=3)) + email[email.index('@'):]
            writer.writerow([
                email,
                faker.password(),
                faker.word(),
                faker.first_name(),
                faker.last_name()
            ])

def generate_digital_product_data(directory_name, num_rows, file_name):
    """Generate random digital product data and write to CSV file."""
    with open(os.path.join(directory_name, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'description', 'price', 'encryption_key'])
        for _ in range(num_rows):
            writer.writerow([
                faker.word(),
                faker.text(),
                faker.random_number(digits=5),
                faker.uuid4()
            ])

def generate_physical_product_data(directory_name, num_rows, file_name):
    """Generate random physical product data and write to CSV file."""
    with open(os.path.join(directory_name, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'description', 'price', 'weight', 'amount_available'])
        for _ in range(num_rows):
            writer.writerow([
                faker.word(),
                faker.text(),
                faker.random_number(digits=5),
                faker.random_number(digits=3),
                faker.random_number(digits=2)
            ])

def generate_store_data(directory_name, num_rows, file_name):
    """Generate random store data and write to CSV file."""
    with open(os.path.join(directory_name, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['lon', 'lat', 'workers_amount', 'is_flagship', 'address_id'])
        for _ in range(num_rows):
            writer.writerow([
                faker.longitude(),
                faker.latitude(),
                faker.random_number(digits=2),
                faker.boolean(),
                faker.random_number(digits=4)
            ])

def generate_address_data(directory_name, num_rows, file_name):
    """Generate random address data and write to CSV file."""
    with open(os.path.join(directory_name, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['street', 'city', 'state', 'postal_code', 'country'])
        for _ in range(num_rows):
            writer.writerow([
                faker.street_address(),
                faker.city(),
                faker.state(),
                faker.postcode(),
                faker.country()
            ])


def generate_store_physical_product_data(directory_name, num_rows, num_stores, num_physical_products, file_name):
    """Generate random store-physical product data and write to CSV file."""
    data_to_insert = set()
    while len(data_to_insert) < num_rows:
        data_to_insert.add((faker.pyint(min_value=1, max_value=num_stores),
                faker.pyint(min_value=1, max_value=num_physical_products)))

    with open(os.path.join(directory_name, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['store_id', 'physical_product_id'])
        for store_id, physical_product_id in data_to_insert:
            writer.writerow([store_id, physical_product_id])


def generate_data(directory_name=GENERATED_DATA_DIR):
    """Generate data for all tables."""
    generate_user_data(directory_name, USER_DATA_ROWS_NUMBER, USER_DATA_FILE_NAME)
    generate_digital_product_data(directory_name, DIGITAL_PRODUCT_DATA_ROWS_NUMBER, DIGITAL_PRODUCT_DATA_FILE_NAME)
    generate_physical_product_data(directory_name, PHYSICAL_PRODUCT_DATA_ROWS_NUMBER, PHYSICAL_PRODUCT_DATA_FILE_NAME)
    generate_store_data(directory_name, STORE_DATA_ROWS_NUMBER, STORE_DATA_FILE_NAME)
    generate_address_data(directory_name, ADDRESS_DATA_ROWS_NUMBER, ADDRESS_DATA_FILE_NAME)
    generate_store_physical_product_data(directory_name=directory_name, 
                                         num_rows=STORES_PHYSICAL_PRODUCTS_DATA_ROWS_NUMBER, 
                                         num_stores=STORE_DATA_ROWS_NUMBER, 
                                         num_physical_products=PHYSICAL_PRODUCT_DATA_ROWS_NUMBER, 
                                         file_name=STORES_PHYSICAL_PRODUCTS_DATA_FILE_NAME)

def delete_files(directory_name=GENERATED_DATA_DIR):
    """Delete all CSV files."""
    for filename in os.listdir():
        file_path = os.path.join(directory_name, filename)
        os.remove(file_path)

if __name__ == "__main__":
    os.makedirs(GENERATED_DATA_DIR, exist_ok=True)
    # delete_files()
    generate_data()
