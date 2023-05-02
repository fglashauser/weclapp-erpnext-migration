import config

class ERPNextHelper:
    """Helper class for ERPNext API.
    """
    def get_country_string(country : str) -> str:
        """Returns the ERPnext territory by a string
        
        Args:
            country (str): Country string
            
        Returns:
            str: ERPnext territory
        """
        return config.EN_COUNTRY_MAP.get(country.lower(), country)