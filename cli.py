import argparse
import getpass
from manager import PasswordManager


class CLI:
    def __init__(self):
        self.manager = PasswordManager()
        self.parser = argparse.ArgumentParser(description="CLI Password Manager")
        self._setup_parser()

    def _setup_parser(self):
        subparsers = self.parser.add_subparsers(dest='command')

        # Add command
        parser_add = subparsers.add_parser('add', help='Add a new password')
        parser_add.add_argument('service', type=str, help='Service name')
        parser_add.add_argument('email', type=str, help='Email associated with the service')
        parser_add.add_argument('login', type=str, help='Login name')
        parser_add.add_argument('password', type=str, help='Password')

        # Get command
        parser_get = subparsers.add_parser('get', help='Retrieve a password')
        parser_get.add_argument('service', type=str, help='Service name')

        # List command
        parser_list = subparsers.add_parser('list', help='List all services')
        parser_list.add_argument('--filter', type=str, help='Filter service by name', default='')

        # Remove command
        parser_remove = subparsers.add_parser('remove', help='Remove a password')
        parser_remove.add_argument('service', type=str, help='Service name')

    def run(self):
        salt, is_new_salt = self.manager.load_or_create_salt()

        if is_new_salt:
            print("No existing data found. Please create a new master password.")
            master_password = getpass.getpass("Create new master password: ")
        else:
            master_password = getpass.getpass("Enter your master password: ")

        key = self.manager.generate_key(master_password, salt)

        args = self.parser.parse_args()
        if args.command == 'add':
            self.manager.add_password(key, args.service, args.email, args.login, args.password)
            print(f"Password added for {args.service}")
        elif args.command == 'get':
            account_info = self.manager.get_password(key, args.service)
            if isinstance(account_info, dict):
                print(f"Email: {account_info['email']}, Login: {account_info['login']}, "
                      f"Password: {account_info['password']}")
            else:
                print(account_info)
        elif args.command == 'list':
            self.manager.list_accounts(key, args.filter)
        elif args.command == 'remove':
            self.manager.remove_password(key, args.service)
        else:
            print("Invalid action or no action specified")
