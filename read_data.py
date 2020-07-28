import json
from data import goals, teachers

lst = [goals, teachers]

with open("data.json", "w") as f:
    json.dump(lst, f)
f.close


