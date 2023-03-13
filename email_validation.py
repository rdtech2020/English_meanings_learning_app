import re
import requests


class ExtraFunc:
    def __init__(self, email_str):
        self.email_str = email_str
        self.key = '' #insert your key

    def is_valid_email(self):
        # Check if the email address matches the pattern of a valid email address
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.email_str):
            return False
        else:
            url = f'https://api.zerobounce.net/v2/validate?api_key={self.key}&email={self.email_str}'
            response = requests.get(url)

            if response.ok:
                result = response.json()
                if result['status'] == 'valid':
                    return True
                else:
                    return False
            else:
                return f'Request failed with status code {response.status_code}: {response.text}'
