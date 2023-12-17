import base64
import hashlib
import json
import os

from cryptography.fernet import Fernet

# File paths
PASSWORD_FILE = "passwords.json"
SALT_FILE = "salt.txt"


class PasswordManager:
    # Function for generating keys
    @classmethod
    def generate_key(cls, master_password, salt):
        # Generate a key that is 32 bytes (256 bits)
        key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000, dklen=32)
        return base64.urlsafe_b64encode(key)

    # Load or create salt
    @classmethod
    def load_or_create_salt(cls):
        if not os.path.exists(SALT_FILE):
            salt = os.urandom(16)
            with open(SALT_FILE, "wb") as file:
                file.write(salt)
            return salt, True  # Return True to indicate the salt was newly created
        with open(SALT_FILE, "rb") as file:
            return file.read(), False  # Return False to indicate existing salt

    # Encrypt data
    @classmethod
    def encrypt_data(cls, key, data):
        fernet = Fernet(key)
        return fernet.encrypt(data.encode())

    # Decrypt data
    @classmethod
    def decrypt_data(cls, key, encrypted_data):
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data).decode()

    # Load passwords
    @classmethod
    def load_passwords(cls, key):
        if not os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, "wb") as file:
                # Create the file with an empty dictionary as content
                encrypted_data = cls.encrypt_data(key, json.dumps({}, indent=4))
                file.write(encrypted_data)
            return {}

        with open(PASSWORD_FILE, "rb") as file:
            encrypted_data = file.read()
            decrypted_data = cls.decrypt_data(key, encrypted_data)
            return json.loads(decrypted_data)

    # Save passwords
    @classmethod
    def save_passwords(cls, key, passwords):
        with open(PASSWORD_FILE, "wb") as file:
            encrypted_data = cls.encrypt_data(key, json.dumps(passwords, indent=4))
            file.write(encrypted_data)

    # Add a password
    @classmethod
    def add_password(cls, key, service, email, login, password):
        passwords = cls.load_passwords(key)
        if service not in passwords:
            passwords[service] = []
        passwords[service].append({"email": email, "login": login, "password": password})
        cls.save_passwords(key, passwords)
        print(f"Password added for {service}")

    # Retrieve a password
    @classmethod
    def get_password(cls, key, service):
        passwords = cls.load_passwords(key)
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
    @classmethod
    def list_accounts(cls, key, service_filter=None):
        passwords = cls.load_passwords(key)
        for service, accounts in passwords.items():
            if service_filter and service_filter.lower() not in service.lower():
                continue
            print(f"Service: {service}")
            for account in accounts:
                print(f"  Email: {account['email']}, Login: {account['login']}")

    # Remove a password
    @classmethod
    def remove_password(cls, key, service):
        passwords = cls.load_passwords(key)
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

        cls.save_passwords(key, passwords)
