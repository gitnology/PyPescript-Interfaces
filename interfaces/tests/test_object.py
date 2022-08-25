from typing import List, Dict, Optional

import pytest

from interfaces import Interface

class VideoObject(Interface):
    name: str
    age: int
    the_list: List[str]
    the_dict: Dict[int,str]
    the_test: Optional[str]


class VideoObjectNonOptional(Interface):
    name: str
    age: int
    the_list: List[str]
    the_dict: Dict[int, str]
    the_test: Optional[str]
    more_test: str

class NestedObject(Interface):
    test: str
    video_obj: VideoObject

class TestObject:

    def test_object_unknown_allowed_is_true(self):
        example_dict = {"name": "bob", "age": 10,"ignore":"true", "the_list": ["1","2","3"], "the_dict":{1:"a",2:"b"}}
        v = VideoObject(**example_dict)
        assert v.name == "bob"
        assert type(v.age) == int
        assert v.the_list == ["1","2","3"]
        assert type(v.the_list) == list
        assert v.the_dict == {1:"a", 2:"b"}
        assert type(v.the_dict) == dict
        with pytest.raises(AttributeError):
            v.ignore

    def test_object_unknown_allowed_is_false(self):
        example_dict = {"name": "bob", "age": 10,"ignore":"false","the_list": ["1","2","3"], "the_dict":{1:"a",2:"b"}}
        with pytest.raises(AttributeError):
            v = VideoObject(**example_dict,unknown_allowed=False)

    def test_object_optional_fields(self):
        example_dict = {"name": "bob", "age": 10,"the_list": ["1","2","3"],"the_test":"blah", "the_dict":{1:"a",2:"b"}}
        v = VideoObject(**example_dict, unknown_allowed=False)
        assert v.the_test == "blah"

    def test_object_optional_fields_default_none(self):
        example_dict = {"name": "bob", "age": 10, "the_list": ["1", "2", "3"],
                        "the_dict": {1: "a", 2: "b"}}
        v = VideoObject(**example_dict, unknown_allowed=False,missing_fields_default_to_none=True)
        assert v.the_test == None

    def test_object_non_optional_fields(self):
        example_dict = {"name": "bob", "age": 10, "ignore": "false"}
        #missing fields
        with pytest.raises(TypeError):
            v = VideoObjectNonOptional(**example_dict, unknown_allowed=False)


    def test_object_to_dict(self):
        example_dict = {"name": "bob", "age": 10,"the_list": ["1","2","3"],"the_test":"blah", "the_dict":{1:"a",2:"b"}}
        v = VideoObject(**example_dict, unknown_allowed=False)
        assert v.to_dict() == {'name': 'bob', 'age': 10, 'the_list': ['1', '2', '3'], 'the_test': 'blah', 'the_dict': {'1': 'a', '2': 'b'}}

    def test_object_to_dict_missing_fields_default_to_none(self):
        example_dict = {"name": "bob", "age": 10, "the_list": ["1", "2", "3"],
                        "the_dict": {1: "a", 2: "b"}}
        v = VideoObject(**example_dict,missing_fields_default_to_none=False)
        assert v.to_dict() == {'name': 'bob', 'age': 10, 'the_list': ['1', '2', '3'],
                               'the_dict': {'1': 'a', '2': 'b'}}

    def test_object_to_json(self):
        example_dict = {"name": "bob", "age": 10, "the_list": ["1", "2", "3"], "the_test": "blah",
                        "the_dict": {1: "a", 2: "b"}}
        v = VideoObject(**example_dict, unknown_allowed=False)
        assert v.to_json() == '{"name": "bob", "age": 10, "the_list": ["1", "2", "3"], "the_test": "blah", "the_dict": {"1": "a", "2": "b"}}'

    def test_object_to_binary(self):
        example_dict = {"name": "bob", "age": 10, "the_list": ["1", "2", "3"], "the_test": "blah",
                        "the_dict": {1: "a", 2: "b"}}
        v = VideoObject(**example_dict, unknown_allowed=False)
        assert v.to_binary()

    def test_nested(self):
        example_dict = {"name": "bob", "age": 10, "the_list": ["1", "2", "3"],
                        "the_dict": {1: "a", 2: "b"}}
        top_level_dict = {"test":"string", "video_obj": example_dict}
        nobj = NestedObject(**top_level_dict)
        nobj.video_obj.name == 'bob'
        nobj.test == 'string'
