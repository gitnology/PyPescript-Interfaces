import json
import logging
import pickle
from typing import Optional, Union

import jsonpickle
import typing
import re
import importlib


class Interface:
    __isinterface__ = True

    def __init__(self, *args, unknown_allowed: bool = True, missing_fields_default_to_none=False,**kwargs):
        #iterate over interface vars and if they are not optional and they are missing from kwargs throw error.
        for interface_var in self.__class__.__annotations__:
            #Checks if field is optional, note this will probably fail if we start using Union fields.. TODO: Fix this later...
            if typing.get_origin(self.__class__.__annotations__[interface_var]) == typing.Union:
                if interface_var not in kwargs.keys():
                    # logging.debug(f"{interface_var} not present in object")
                    if missing_fields_default_to_none:
                        self.__setattr__(interface_var,None)
            else:
                if interface_var not in kwargs.keys():
                    raise TypeError(f"{interface_var} not found in kwargs, make field {interface_var} Optional[] or pass in value when instanciating {self.__class__}.")
        #iterate over keyword args and look if they are in the interface (child) class
        for k in kwargs.keys():
            if k in self.__class__.__annotations__:
                var_declared_type = self.__class__.__annotations__.get(k)
                #warn if type mismatch between declared type and kwarg type
                if var_declared_type != type(kwargs[k]):
                    pass
                    # logging.warning(
                    #     f"declared type of {var_declared_type} does not match type of {k} from {kwargs[k]}")
                parent_type = re.split(r'\[|\]', str(self.__class__.__annotations__.get(k)))
                nested_interface_class = None
                #check for nested_interfaces, if so instantiate them as object in the same way. Account for list type.
                for num,child_type in enumerate(parent_type):
                    try:
                        if child_type.startswith("<class "):
                            #ugly hack .. sometimes it presents as <class and sometimes it doesn't..
                            child_type = child_type[8:-2]
                        child_type_split = child_type.split(".")
                        #import module so we can evaluate whether it has the reserved __isinterface__== True to determine if it is a nested interface
                        child_type_class = getattr(importlib.import_module(".".join(child_type_split[:-1])),child_type_split[-1])
                        if getattr(child_type_class,"__isinterface__"):
                            if parent_type[num-1].lower() == "typing.list":
                                #if nested list[interface]
                                nested_interface_class = [child_type_class(**x) for x in kwargs[k]]
                            else:
                                #if nested interface
                                nested_interface_class =  child_type_class(**kwargs[k])
                    except:
                        pass
                if nested_interface_class:
                    self.__setattr__(k, nested_interface_class)
                else:
                    self.__setattr__(k, kwargs[k])
            else:
                #if not unknown_allowed any unknown kwargs raise an exception
                if not unknown_allowed:
                    raise AttributeError

    def to_dict(self):
        return json.loads(jsonpickle.encode(self, unpicklable=False))

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_binary(self,protocol=pickle.HIGHEST_PROTOCOL):
        return pickle.dumps(self,protocol=protocol)