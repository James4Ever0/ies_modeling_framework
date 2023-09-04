# class DefaultDict
from collections import defaultdict

mDefaultDict = defaultdict(lambda: "default", a=1)

print(mDefaultDict["abc"])
print(mDefaultDict)