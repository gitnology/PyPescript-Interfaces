ES Pypescript Interface lib, for strongly typing objects (like typescript) in python.



usage: 

To use, create a new class and make the shape of the object you want, use the typing library to annotate types, 
then pass in the expanded dict of it (from a request or whatever)

by default unknown kwargs are ignored, this can be configured by passing in unknown_allowed=False as shown in a later example

Optional fields are also supported and default to None.

Mismatching types will flag errors.



```python
import Interface

class YourClassHere(Interface):
	example_str: str
    example_list:List
    example_optional: Optional[str]
    


example_dict = {"example_str":"foo","example_list": ["foo"],"other_values_to_ignore":"bar"}
ych = YourClassHere(**example_dict)
print(ych.example_str) # blah

```

#To fail if provided unknown values:

```python
class YourClassHere(Interface):
	example_str: str
    


example_dict = {"example_str":"foo"}
ych = YourClassHere(**example_dict,unknown_allowed=False)
print(ych.example_str) # blah


``` 

	
 
 