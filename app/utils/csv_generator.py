import csv
import random
import os

def generate_csv_data(filename="data.csv", row_count=1000):
    fieldnames = [
        'user_name', 'user_surname', 'user_tax_id', 'user_email', 'user_password', # User
        'acc_balance', 'acc_card_number',                                        # Account
        'tx_type', 'tx_amount', 'tx_merchant_name', 'tx_category'                 # Transaction/Payment
    ]

    names = ["Ivan", "Petro", "Olena", "Maria", "Andriy", "Svitlana", "Dmitro"]
    surnames = ["Ivanov", "Petrenko", "Kovalenko", "Bondar", "Tkachenko", "Shevchenko"]
    categories = ["Food", "Transport", "Utilities", "Entertainment", "Health"]
    merchants = ["Silpo", "ATB", "Uber", "Kyivstar", "Apteka24", "Netflix"]

    users_pool = []
    for i in range(100):
        users_pool.append({
            'name': random.choice(names),
            'surname': random.choice(surnames),
            'tax_id': f"{1000000000 + i}",
            'email': f"user{i}@example.com",
            'password': f"pbkdf2:sha256:260000$hashed_pass_{i}"
        })

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(row_count):
            user = random.choice(users_pool)
            tx_type = random.choice(['transfer', 'payment'])
            card_number = f"4441{i:012d}"
            
            row = {
                # User data
                'user_name': user['name'],
                'user_surname': user['surname'],
                'user_tax_id': user['tax_id'],
                'user_email': user['email'],
                'user_password': user['password'],
                
                # Account data
                'acc_balance': round(random.uniform(500.0, 100000.0), 2),
                'acc_card_number': card_number,
                
                # Transaction data
                'tx_type': tx_type,
                'tx_amount': round(random.uniform(10.0, 5000.0), 2),
                'tx_merchant_name': random.choice(merchants) if tx_type == 'payment' else None,
                'tx_category': random.choice(categories) if tx_type == 'payment' else None
            }
            writer.writerow(row)

    print(f"Файл '{filename}' згенеровано: {row_count} рядків.")

if __name__ == "__main__":
    generate_csv_data("data.csv", 1000)