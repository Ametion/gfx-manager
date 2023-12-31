
# Password Manager CLI

A simple and secure command-line password manager written in Python. This application allows you to securely store, retrieve, list, and remove your passwords.

## Features

- Secure password storage with encryption.
- Add, retrieve, list, and remove passwords.
- Command-line interface for easy use.

## Prerequisites

- Python 3.x installed on your system.
- `pip` for installing Python packages.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Ametion/gfx-manager.git
   ```

2. Navigate to the downloaded directory:

   ```bash
   cd gfx-manager
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   This will install necessary packages as specified in `requirements.txt`.

## Usage

Run the program using Python from the command line:

```bash
python main.py [command]
```

### Available Commands

- `add`: Add a new password.
- `get`: Retrieve an existing password.
- `list`: List all saved services and their credentials.
- `remove`: Remove an existing password.

#### Examples:

- Add a password:

  ```bash
  python main.py add [service] [email] [login] [password]
  ```

- Get a password:

  ```bash
  python main.py get [service]
  ```

- List passwords:

  ```bash
  python main.py list
  ```

  Optional: filter by service name:

  ```bash
  python main.py list --filter [service name]
  ```

- Remove a password:

  ```bash
  python main.py remove [service]
  ```

### Security

On first use, you will be prompted to create a master password. This password is used to generate an encryption key for securing your data. Remember this master password, as it is required to access your stored passwords.

### Data Storage

Passwords are stored in an encrypted file (`passwords.json`) in the same directory as the application.

### I Hope you will like it :)
