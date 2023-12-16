import base64
import hashlib
import json
import os

from cryptography.fernet import Fernet

from passwords import SALT_FILE, PASSWORD_FILE


def generate_key(master_password, salt):
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
    return base64.urlsafe_b64encode(key)


# Load or create salt
def load_or_create_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as file:
            file.write(salt)
        return salt, True  # Return True to indicate the salt was newly created
    with open(SALT_FILE, "rb") as file:
        return file.read(), False  # Return False to indicate existing salt


# Encrypt data
def encrypt_data(key, data):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


# Decrypt data
def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()


# Load passwords
def load_passwords(key):
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "wb") as file:
            # Create the file with an empty dictionary as content
            encrypted_data = encrypt_data(key, json.dumps({}, indent=4))
            file.write(encrypted_data)
        return {}

    with open(PASSWORD_FILE, "rb") as file:
        encrypted_data = file.read()
        decrypted_data = decrypt_data(key, encrypted_data)
        return json.loads(decrypted_data)


# Save passwords
def save_passwords(key, passwords):
    with open(PASSWORD_FILE, "wb") as file:
        encrypted_data = encrypt_data(key, json.dumps(passwords, indent=4))
        file.write(encrypted_data)


# Add a password
def add_password(key, service, email, login, password):
    passwords = load_passwords(key)
    if service not in passwords:
        passwords[service] = []
    passwords[service].append({"email": email, "login": login, "password": password})
    save_passwords(key, passwords)
    print(f"Password added for {service}")


# Retrieve a password
def get_password(key, service):
    passwords = load_passwords(key)
    accounts = passwords.get(service, [])

    if not accounts:
        return "No password found for this service"

    for idx, account in enumerate(accounts):
        print(f"{idx + 1}: Email: {account['email']}, Login: {account['login']}")

    if len(accounts) > 1:
        selected = int(input("Choose the account number: ")) - 1
        if 0 <= selected < len(accounts):
            return accounts[selected]
        else:
            return "Invalid account number"
    return accounts[0]


# List all accounts
def list_accounts(key, service_filter=None):
    passwords = load_passwords(key)
    for service, accounts in passwords.items():
        if service_filter and service_filter.lower() not in service.lower():
            continue
        print(f"Service: {service}")
        for account in accounts:
            print(f"  Email: {account['email']}, Login: {account['login']}")


# Remove a password
def remove_password(key, service):
    passwords = load_passwords(key)
    if service not in passwords:
        print("Service not found.")
        return

    accounts = passwords[service]
    if not accounts:
        print("No accounts found for this service.")
        return

    # List accounts
    for idx, account in enumerate(accounts, start=1):
        print(f"{idx}: {account['email']} - {account['login']}")

    # Add option to remove all
    print(f"{len(accounts) + 1}: Remove all accounts for this service")
    print(f"{len(accounts) + 2}: Quit")

    try:
        choice = int(input("Choose an account to remove (or remove all): "))
        if choice == len(accounts) + 1:
            del passwords[service]
            print("All accounts for this service have been removed.")
        elif choice == len(accounts) + 2:
            print("Quited")
        elif 1 <= choice <= len(accounts):
            selected_account = accounts.pop(choice - 1)
            print(f"Removed account: {selected_account['email']} - {selected_account['login']}")
        else:
            print("Invalid choice")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    save_passwords(key, passwords)
