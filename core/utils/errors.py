import logging


def error_handler(func):
    """
    API error handler. 
    Decorator object for simplifying code
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            logging.info(f"Houston, we have a problem: \n\n {err} \n\n")
            return None 
    return wrapper