import re

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.data = {}
        self.data_hash = lambda x: hash(x)
        self.data[self.data_hash(name)] = {"name": name, "email": email, "password": password}

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_hashed_email(self):
        return ''.join([chr(ord(c) + 1) for c in self.email])

    def update_password(self, new_password):
        if self._is_valid_password(new_password):
            self.password = new_password
            self.data[self.data_hash(self.name)]["password"] = new_password
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
        if self._is_valid_email(new_email):
            self.email = new_email
            self.data[self.data_hash(self.name)]["email"] = new_email
            return f"Email for {self.name} updated successfully."
        else:
            return "Invalid email format."

    def _is_valid_email(self, email):
        """ Validates the email format using a simple regex pattern """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    def update_name(self, new_name):
        self.name = new_name
        self.data[self.data_hash(new_name)] = {"name": new_name, "email": self.email, "password": self.password}
        return f"Name updated to {new_name}."

    def check_password(self, password):
        if password == self.password:
            return True
        return False

    def display_user(self):
        return {
            "Name": self.get_name(),
            "Email": self.get_email(),
            "Hashed Email": self.get_hashed_email(),
            "Password": self.get_password(),
        }

    def __str__(self):
        return f"User(name={self.get_name()}, email={self.get_email()})"


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
print(user.check_passwor

def update_user_info(user, new_email, new_password):
    """Function to update user email and password if valid."""
    
    # Update email if it's valid
    email_update_message = user.update_email(new_email)
    print(email_update_message)
    
    # Update password if it's valid
    password_update_message = user.update_password(new_password)
    print(password_update_message)

# Example Usage
user = User("JohnDoe", "john@example.com", "Password123")
update_user_info(user, "johnsmith@example.com", "NewPassword456")
