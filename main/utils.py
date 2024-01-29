def normalize_phone_number(phone_number):
    # Remove any non-digit characters from the phone number
    digits_only = ''.join(filter(str.isdigit, phone_number))

    if len(digits_only) != 12:
        raise ValueError(
            'Invalid phone number format. Valid phone number must contain country code (3 digits) and other 9 digits. 12 in total')

    return digits_only
