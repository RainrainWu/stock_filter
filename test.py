import re

STR_1 = "($0.49) (06/30/2019)"
STR_2 = "$0.49 (06/30/2019)"
STR_3 = "$2.84"
LIST = [STR_1, STR_2, STR_3]

pattern = re.compile("[0-9]+[\.]*[0-9]*")

for STR in LIST:
    match = pattern.search(STR)
    print(match.group(0))
