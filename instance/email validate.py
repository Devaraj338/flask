import re

def is_valid_email(email):
    # Define the regular expression pattern for a valid email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)
    
    # Return True if the email is valid, False otherwise
    return bool(match)

# Example usage:
email_to_validate = input()
if is_valid_email(email_to_validate):
    print(f"{email_to_validate} is a valid email address.")
else:
    print(f"{email_to_validate} is not a valid email address.")
