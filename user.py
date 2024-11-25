import re
import bcrypt
from hashlib import sha256

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)
        self.data = {}
        self._store_user_data()

    def _store_user_data(self):
        """ Helper method to store user data """
        self.data[self._hash_name(self.name)] = {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    def _hash_name(self, name):
        """ Simple hash function for name, to avoid collisions """
        return sha256(name.encode('utf-8')).hexdigest()

    def _hash_password(self, password):
        """ Hash the password using bcrypt for secure storage """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def _check_password(self, password, hashed_password):
        """ Check if the provided password matches the hashed password """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_hashed_email(self):
        """ Return a hashed version of the email using sha256 for simplicity """
        return sha256(self.email.encode('utf-8')).hexdigest()

    def update_password(self, new_password):
        """ Update password if it meets strength requirements """
        if self._is_valid_password(new_password):
            self.password = self._hash_password(new_password)
            self.data[self._hash_name(self.name)]["password"] = self.password
            return f"Password for {self.name} updated successfully."
        else:
            return "Password does not meet strength requirements."

    def _is_valid_password(self, password):
        """ Validates that the password is at least 8 characters, contains at least one number, and one uppercase letter """
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        return True

    def update_email(self, new_email):
        """ Update email if it's valid """
        if self._is_valid_email(new_email):
            self.email = new_email
            self.data[self._hash_name(self.name)]["email"] = self.email
            return f"Email for {self.name} updated successfully."
        else:
            return "Invalid email format."

    def _is_valid_email(self, email):
        """ Validates the email format using a regex pattern """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    def update_name(self, new_name):
        """ Update user's name and ensure it's reflected in stored data """
        self.name = new_name
        self._store_user_data()
        return f"Name updated to {new_name}."

    def check_password(self, password):
        """ Check if the password matches the stored hashed password """
        return self._check_password(password, self.password)

    def display_user(self):
        """ Return a dictionary representation of the user """
        return {
            "Name": self.get_name(),
            "Email": self.get_email(),
            "Hashed Email": self.get_hashed_email(),
            "Password": self.password.decode('utf-8')  # For clarity, but don't store plain password in production
        }

    def __repr__(self):
        """ Provide a clear representation of the user object """
        return f"User(name={self.get_name()}, email={self.get_email()})"

    def __str__(self):
        """ Human-readable string representation """
        return f"User: {self.get_name()} ({self.get_email()})"


# Example Usage
user = User("JohnDoe", "john@example.com", "Password123")
print(user.display_user())  # Display user details

# Update user password
print(user.update_password("NewPassword456"))  # Valid password
print(user.update_password("short"))  # Invalid password

# Update user email
print(user.update_email("newemail@example.com"))  # Valid email
print(user.update_email("invalid-email"))  # Invalid email

# Update user name
print(user.update_name("JohnSmith"))

# Check user password
print(user.check_password("Password123"))  # False
print(user.check_password("NewPassword456"))  # True
