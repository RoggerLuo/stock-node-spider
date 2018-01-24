import json
import numpy as np
def load(full_path):
    with open(full_path) as json_file:
        data = json.load(json_file)
        return data

data = load()
data = np.array(data) 
print(data[0]['value'])