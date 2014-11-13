from Cura.Settings.Validators.IntValidator import IntValidator
from Cura.Settings.Validators.FloatValidator import FloatValidator
from Cura.Settings.Validators.ResultCodes import ResultCodes

## A setting object contains a (single) configuration setting.
# Settings have validators that check if the value is valid, but do not prevent invalid values!
# Settings have conditions that enable/disable this setting depending on other settings. (Ex: Dual-extrusion)

class Setting(object):    
    def __init__(self, key, default, type):
        self._key = key
        self._label = key
        self._tooltip = ''
        self._default_value = unicode(default)
        self._value = None
        self._machine = None
        self._type = type
        self._visible = True
        self._validator = None
        self._callbacks = [] #Callbacks trigged when the value is changed
        self._conditions = []
        self._parent_setting = None
        self._hide_if_all_children_visible = True
        self._copy_from_parent_function = lambda machine, value: value
        self._children = []

        if type == 'float':
            FloatValidator(self) # Validator sets itself as validator to this setting
        elif type == 'int':
            IntValidator(self) 
    
    def setValidator(self, validator):
        self._validator = validator
        
    def getValidator(self):
        return self._validator
    
    def setParent(self, setting):
        self._parent_setting = setting
    
    def addChild(self, setting):
        setting.setParent(self)
        self._children.append(setting)

    ## Recursively check it's children to see if the key matches.
    # \returns Setting if key match is found, None otherwise.
    def getSettingByKey(self, key):
        if self._key == key:
            return self
        for s in self._children:
            ret = s.getSettingByKey(key)
            if ret is not None:
                return ret
        return None

    def setMachine(self, machine):
        self._machine = machine

    def setVisible(self, visible):
        self._visible = visible
        return self
    
    def setDefaultValue(self, value):
        self._default_value = value
        return self

    def getDefaultValue(self):
        return self._default_value

    ## Check if the setting is visible. It can be that the setting visible is true, 
    #  but it still should be invisible as all it's children are visible (and the setting is thus not visible!).
    # \returns bool
    def isVisible(self):
        if not self._visible:
            return False
        if self._hide_if_all_children_visible and self.checkAllChildrenVisible():
            return False
        return True

    ## Check if all children are visible.
    # \returns True if all children are visible. False otherwise
    def checkAllChildrenVisible(self):
        if len(self._children) < 1:
            return False
        for child in self._children:
            if not child.isVisible()
                return False
        return True

    def setLabel(self, label):
        self._label = label
        
    def setTooltip(self, tooltip)
        self._tooltip = tooltip

    def setRange(self, min_value = None, max_value = None, min_value_warning = None, max_value_warning = None):
        if(self._validator = None):
            return
        validator.setRange(min_value, max_value, min_value_warning, max_value_warning)

    ## Sets the function used to copy data from parent
    # \param function
    def setCopyFromParentFunction(self, function):
        self._copy_from_parent_function = function

    def getLabel(self):
        return self._label

    def getTooltip(self):
        return self._tooltip

    def getKey(self):
        return self._key

    def getType(self):
        return self._type

    def getValue(self):
        if not self._visible:
            if self._copy_from_parent_function is not None and self._parent_setting is not None:
                self._value = str(self._copy_from_parent_function(self._machine, self._parent_setting.getValue()))
            else:
                return self._default_value
        if self._value is None:
            return self._default_value
        return self._value

    ## Set the value of this setting and call the registered callbacks.
    # \param value Value to be set.
    def setValue(self, value):
        if self._value != value:
            self._value = value
            self.validate()
            for callback in self._callbacks:
                callback()
    
    ## Add function to be called when value is changed.
    # \param function to be added.
    def addValueChangedCallback(self, callback):
        self._callbacks.append(callback)
    
    ## validate the value of this setting. 
    # \returns ResultCodes.succes if there is no validator or if validation is succesfull. Returns warning or error code otherwise.
    def validate(self):
        if(self._validator is not None):
            return self._validator.validate()
        else:
            return ResultCodes.succes

    def getAllChildren(self):
        all_children = []
        for s in self._children:
            all_children.extend(s)
            all_children.extend(s.getAllSettings())
        return all_children

    def getChildren(self):
        return self._children

    def __repr__(self):
        return '<Setting: %s>' % (self._key)