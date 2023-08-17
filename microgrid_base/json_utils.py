from log_utils import logger_print

import json

# it's json-like object, not json serializable object!


def jsonWalk(jsonObj, location=[]):
    # this is not tuple. better convert it first?
    # mlocation = copy.deepcopy(location)
    if type(jsonObj) == dict:
        for key in jsonObj:
            content = jsonObj[key]
            if type(content) not in [dict, list, tuple]:
                yield location + [key], content
            else:
                # you really ok with this?
                for mkey, mcontent in jsonWalk(content, location + [key]):
                    yield mkey, mcontent
    elif type(jsonObj) in [
        list,
        tuple,
    ]:  # this is not pure JSON. we only have list and dicts.
        for key, content in enumerate(jsonObj):
            # content = jsonObj[key]
            if type(content) not in [dict, list, tuple]:
                yield location + [key], content
            else:
                for mkey, mcontent in jsonWalk(content, location + [key]):
                    yield mkey, mcontent
    else:
        raise Exception("Not a JSON compatible object: {}".format(type(jsonObj)))


def jsonWalk2(jsonObj):
    jsonObj = jsonify(jsonObj)
    return jsonWalk(jsonObj)


def jsonLocate(jsonObj, location=[]):
    # logger_print("object:",jsonObj)
    # logger_print("location:",location)
    if location != []:
        # try:
        return jsonLocate(jsonObj[location[0]], location[1:])
        # except:
        #     breakpoint()
    return jsonObj


def jsonUpdate(jsonObj, location=[], update_content=None):
    if location != []:
        if type(jsonObj) == dict:
            target = {
                location[0]: jsonUpdate(
                    jsonObj[location[0]],
                    location=location[1:],
                    update_content=update_content,
                )
            }
            # logger_print("keys:", location)
            # logger_print("JSONOBJ:", jsonObj)
            # logger_print("update target:", target)
            jsonObj.update(target)
            return jsonObj
        elif type(jsonObj) == list:
            target = jsonUpdate(
                jsonObj[location[0]],
                location=location[1:],
                update_content=update_content,
            )
            # logger_print("keys:", location)
            # logger_print("JSONOBJ:", jsonObj)
            # logger_print("override target:", target)
            jsonObj[location[0]] = target
            return jsonObj
        else:
            raise Exception("Unsupported JSON update target type:", type(jsonObj))
    return update_content


def jsonDeleteObject(jsonObj, location: list):
    assert len(location) > 0
    obj = jsonObj
    # logger_print(location, obj)
    for key in location[:-1]:
        obj = obj[key]
    del obj[location[-1]]
    return jsonObj


# how to reload module directly, so we can include this function as well?
import typing

# what the fuck is going on here?
# ImportError: cannot import name 'jsonDeleteAllinstances' from 'lazero.utils.json' (/root/Desktop/works/lazero/lazero/utils/json.py)
# how to reload module actually, making from <module> import <object> work?


def jsonDeleteAllInstances(
    jsonObj, isInstance: typing.Callable[[typing.Any], bool], copy=True
):
    if copy:
        jsonObj2 = jsonObj.copy()
    else:
        jsonObj2 = jsonObj
    candidates = []
    for key, value in jsonWalk(jsonObj2):
        if isInstance(value):
            # delete that thing! but how to delete these things once for all?
            candidates.append(key)
    candidates.sort(key=lambda x: -x[-1] if type(x[-1]) == int else 1)
    for candidate in candidates:
        jsonObj2 = jsonDeleteObject(jsonObj, candidate)
    return jsonObj2


def jsonTupleToList(jsonObj2, copy=True):
    if copy:
        jsonObj = jsonObj2.copy()
    else:
        jsonObj = jsonObj2
    candidates = []
    for key, value in jsonWalk(jsonObj):
        if type(value) == tuple:
            candidates.append(key)
    for candidate in candidates:
        data = jsonLocate(jsonObj, candidate)
        data = list(data)
        jsonObj = jsonUpdate(jsonObj, candidate, data)
    return jsonObj


def jsonify(
    jsonObj, copy=True, refine=False, isInstance=lambda obj: obj == ...
):  # remove ellipsis
    jsonObj2 = jsonTupleToList(jsonObj, copy=copy)
    jsonObj2 = jsonDeleteAllInstances(jsonObj2, isInstance, copy=copy)
    if refine:
        return json.loads(json.dumps(jsonObj2))
    else:
        return jsonObj2


#### NEW FUNCTIONS ####

import copy


def jsonApply(jsonObj, *funcs):
    jsonObj2 = copy.deepcopy(jsonObj)
    for location, content in jsonWalk(jsonObj):
        for func in funcs:
            content = func(location, content)
        jsonUpdate(jsonObj2, location, content)
    return jsonObj2
