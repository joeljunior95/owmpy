
class OWMException(Exception):
    """Base exception for OWMpy
    """
    pass

class GernericOWMException(OWMException):
    """ Exeption raised when a valid API Key is not informed
    """
    pass

class InvalidAPIKeyException(OWMException):
    """ Exeption raised when a valid API Key is not informed
    """
    pass

class SearchParamsException(OWMException):
    """ Exeption raised when a valid API Key is not informed
    """
    pass

class RequestLimitException(OWMException):
    """ Exeption raised when a valid API Key is not informed
    """
    pass

class OWMServerException(OWMException):
    """ Exeption raised when a valid API Key is not informed
    """
    pass