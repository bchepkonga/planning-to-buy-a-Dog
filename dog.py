import requests
import sqlite3

def fetch_breed_characteristics():
    url = "https://api.thedogapi.com/v1/breeds"
    response = requests.get(url)
    return response.json()

def create_database():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Create the table to store breed information
    c.execute('''
        CREATE TABLE IF NOT EXISTS breeds (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            characteristics TEXT
        )
    ''')

    conn.commit()
    conn.close()

def save_breed_characteristics_to_database():
    breeds = fetch_breed_characteristics()

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    for breed in breeds:
        name = breed.get("name")
        characteristics = breed.get("temperament")
        if name and characteristics:
            c.execute("INSERT OR IGNORE INTO breeds (name, characteristics) VALUES (?, ?)", (name, characteristics))

    conn.commit()
    conn.close()

def get_breed_characteristics(breed_size, dietary_needs):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT characteristics FROM breeds WHERE name LIKE ? AND characteristics LIKE ?", ('%'+breed_size+'%', '%'+dietary_needs+'%',))
    breed_characteristics = c.fetchone()

    conn.close()

    if breed_characteristics:
        return breed_characteristics[0]

    return None

def calculate_monthly_expenses(breed_size):
    # Calculate expected monthly expenses based on breed size
    # You can modify this function based on your actual expenses data
    expenses_per_size = {
        'small': 100,
        'medium': 150,
        'large': 200,
    }
    return expenses_per_size.get(breed_size, 0)

def display_guide():
    print("Planning to Have a Dog: A Comprehensive Guide to Welcoming Your New Furry Family Member")
    print("Best Dog Breeds Included - Expected Monthly Expenses Per Dog in Dollars\n")

    breed_size = input("Enter your preferred breed size (small, medium, or large): ").lower()
    dietary_needs = input("Enter your dog's dietary needs (e.g., hypoallergenic, special diet): ").lower()

    breed_characteristics = get_breed_characteristics(breed_size, dietary_needs)
    if breed_characteristics:
        print(f"\nBreed Characteristics: {breed_characteristics}\n")
    else:
        print("\nBreed characteristics not found for the given input.\n")

    monthly_expenses = calculate_monthly_expenses(breed_size)
    print(f"Estimated Monthly Expenses Per Dog: ${monthly_expenses}")

def main():
    create_database()  # Create or connect to the database
    save_breed_characteristics_to_database()  # Fetch breed characteristics and save to the database
    display_guide()

if __name__ == "__main__":
    main()
