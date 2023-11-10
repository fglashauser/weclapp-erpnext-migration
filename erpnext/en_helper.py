import config
import re
import config
from datetime import datetime

class ERPNextHelper:
    """Helper class for ERPNext API.
    """
    @staticmethod
    def get_country_string(country : str) -> str:
        """Returns the ERPnext territory by a string
        
        Args:
            country (str): Country string
            
        Returns:
            str: ERPnext territory
        """
        return config.EN_COUNTRY_MAP.get(country.lower(), country)
    
    @staticmethod
    def standardize_phone_number(number: str, default_country_code: str = config.EN_DEFAULT_PHONE_COUNTRY_CODE) -> str:
        """Standardizes a phone number.

        Args:
            number (str): Phone number to standardize
            default_country_code (str, optional): Default country code (without leading +) to use if none is given. Defaults to config.EN_DEFAULT_PHONE_COUNTRY_CODE.

        Returns:
            str: Standardized phone number
        """
        # Remove all non-numeric characters except the + sign
        cleaned_number = re.sub(r'\D', '', number)

        # Check if there is already a country code
        # If not, add the default one
        if cleaned_number.startswith('00'):
            cleaned_number = f"+{cleaned_number[2:]}"
        elif cleaned_number.startswith('0'):
            cleaned_number = f"+{default_country_code}{cleaned_number[1:]}"
        elif cleaned_number:
            cleaned_number = f"+{cleaned_number}"

        return cleaned_number
    
    @staticmethod
    def get_date_from_weclapp_ts(timestamp: int) -> str:
        """Returns a date string from a WeClapp timestamp.

        Args:
            timestamp (int): WeClapp timestamp

        Returns:
            str: Date string
        """
        return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")