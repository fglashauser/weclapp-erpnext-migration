class ERPNextAPIData(dict):
    """Class to represent the data of a new enitity for a DocType in ERPNext.
    Used for creating or updating a child of a DocType with one step in a single API call.

    Args:
        dict (_type_): Inherits from dict to be able to store the data of the entity
    """
    def __init__(self, doctype : str, name : str, update_existing : bool = False, data : dict = None):
        """Creates a new instance of a ERPNext API-Data-Object
        
        Args:
            doctype (str): DocType of the child
            name (str): Name of the entity in the ERPNext database
            update_existing (bool, optional): Whether updates a entity if it exist or leave it. Defaults to False.
            data (dict, optional): Data to fill the entity with. Defaults to None.
        """
        super().__init__(data or {})
        self.doctype = doctype
        self.name = name
        self.update_existing = update_existing