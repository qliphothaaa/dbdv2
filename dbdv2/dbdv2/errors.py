class Error(Exception):

    
    """Base class for other exceptions"""
    pass

class TargetServerDownError(Error):
    """Raised when the target server down"""
    pass


class CookieExpiredError(Error):
    """Raised when the cookie expired"""
    pass

