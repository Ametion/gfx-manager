import getpass

import cryptography.fernet

from passwords.service import (
    load_or_create_salt,
    generate_key,
    save_passwords,
    load_passwords,
    add_password,
    get_password,
    list_accounts,
    remove_password
)


def main():
    salt, is_new_salt = load_or_create_salt()
    key = None
    max_attempts = 3
    attempts = 0

    if is_new_salt:
        print("No existing data found. Please create a new master password.")
        master_password = getpass.getpass("Create new master password: ")
        key = generate_key(master_password, salt)
        save_passwords(key, {})
    else:
        while attempts < max_attempts:
            try:
                master_password = getpass.getpass("Your master password: ")
                key = generate_key(master_password, salt)
                load_passwords(key)
                break
            except cryptography.fernet.InvalidToken:
                attempts += 1
                print(f"Invalid master password. {max_attempts - attempts} attempts left.")

        if attempts == max_attempts:
            print("Maximum attempts reached. Exiting...")
            return

    if key is None:
        print("Resetting data. Please create a new master password.")
        master_password = input("Create new master password: ")
        key = generate_key(master_password, salt)
        save_passwords(key, {})

    while True:
        action = input("Choose action (add, get, list, remove, quit): ").lower()
        if action == "quit":
            break
        elif action == "add":
            service = input("Enter service name: ")
            email = input("Enter email: ")
            login = input("Enter login: ")
            password = input("Enter password: ")
            add_password(key, service, email, login, password)
        elif action == "get":
            service = input("Enter service name: ")
            account_info = get_password(key, service)
            if isinstance(account_info, dict):
                print(
                    f"Email: {account_info['email']}, Login: {account_info['login']}, "
                    f"Password: {account_info['password']}")
            else:
                print(account_info)
        elif action == "list":
            service_filter = input("Enter service filter (optional): ")
            list_accounts(key, service_filter)
        elif action == "remove":
            service = input("Enter service name: ")
            remove_password(key, service)
        else:
            print("Invalid action")


if __name__ == "__main__":
    main()
