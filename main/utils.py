def normalize_phone_number(phone_number):
    # Remove any non-digit characters from the phone number
    digits_only = ''.join(filter(str.isdigit, phone_number))

    if len(digits_only) != 12:
        raise ValueError(
            'Invalid phone number format. Valid phone number must contain country code (3 digits) and other 9 digits. 12 in total')

    return digits_only


def validate_data(first_name, last_name, username, phone_number, email, password):
    required_fields = {
        'first name': first_name,
        'last name': last_name,
        'email': email,
        'phone number': phone_number,
        'username': username,
        'password': password
    }

    for field_name, field_value in required_fields.items():
        if not field_value:
            raise ValueError(f'A {field_name} is required!')
