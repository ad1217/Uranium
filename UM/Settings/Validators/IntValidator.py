# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from UM.Settings.Validators.Validator import Validator
from UM.Settings.Validators.ResultCodes import ResultCodes

## Validates if a setting is within two possible ranges (error range & warning range) and if setting is integer.
class IntValidator(Validator):
    def __init__(self, setting, min_value = None, max_value = None, min_value_warning = None, max_value_warning = None):
        super(IntValidator,self).__init__(setting)   
        self._min_value = min_value
        self._max_value = max_value
        self._min_value_warning = min_value_warning
        self._max_value_warning = max_value_warning
        
        
    def setRange(self, min_value = None, max_value = None, min_value_warning = None , max_value_warning = None):
        self._min_value = min_value
        self._max_value = max_value
        self._min_value_warning = min_value_warning
        self._max_value_warning = max_value_warning
    
    ## Validate the setting. 
    # \returns result Returns value as defined in ResultCodes.py
    # \returns message Message providing more detail about warning / error (if any)
    def validate(self, value):
        try:
            return self._checkRange(int(value), self._min_value, self._max_value, self._min_value_warning, self._max_value_warning)
        except (ValueError, SyntaxError, TypeError, NameError):
            return ResultCodes.not_valid_error
