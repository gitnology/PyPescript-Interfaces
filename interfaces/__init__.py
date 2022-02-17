import json
import logging
import pickle
from typing import Optional, Union

import jsonpickle
import typing


class Interface:

    def __init__(self, *args, unknown_allowed: bool = True, missing_fields_default_to_none=True,**kwargs):
        #iterate over interface vars and if they are not optional and they are missing from kwargs throw error.
        for interface_var in self.__class__.__annotations__:
            #Checks if field is optional, note this will probably fail if we start using Union fields.. TODO: Fix this later...
            if typing.get_origin(self.__class__.__annotations__[interface_var]) == typing.Union:
                if interface_var not in kwargs.keys():
                    logging.debug(f"{interface_var} not present in object")
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
                    logging.warning(
                        f"declared type of {var_declared_type} does not match type of {k} from {kwargs[k]}")
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
