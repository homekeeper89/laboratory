from pydantic import BaseModel, ValidationError
from flask import abort


def validator(original_class):
    orig_init = original_class.__init__
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, **args):
        try:
            orig_init(self, **args)  # Call the original __init__
        except ValidationError as ve:
            print(ve)
            abort(400, ve.errors())

    original_class.__init__ = __init__  # Set the class' __init__ to the new one
    return original_class


@validator
class BaseRequestModel(BaseModel):
    pass
