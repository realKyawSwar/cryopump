import json
from pathlib import Path


here = Path(__file__).resolve().parents[3]
configPath = str(here) + "/config/"

with open(configPath+'config.json') as config_file:
    config = json.load(config_file)


in_operation = config['in_operation']
CRC = config['CRC']
register_dict = config['register_dict']
in_ope = {int(k): v for k, v in in_operation.items()}
# ope_list = []
# for k, v in in_ope.items():
#     for i in v:
#         ope_list.append([k, i])
# print(ope_list)
CRC = {int(k): v for k, v in CRC.items()}
for i in range(2):
    CRC[i] = {int(k): v for k, v in CRC[i].items()}
sample_cycles = config['sample_cycles']

# "42": [0.01, "I_out"],
# "26": [0.01, "Imod"],
# {0: {1: 'CRC1', 2: 'CRC1', 3: 'CRC1', 4: 'CRC2',
# 5: 'CRC2', 6: 'CRC2', 7: 'CRC3', 8: 'CRC3',
# 9: 'CRC4', 10: 'CRC4', 11: 'CRC4',
# 12: 'CRC5', 13: 'CRC5', 14: 'CRC5',
# 15: 'CRC6', 16: 'CRC6', 17: 'CRC7', 18:
# 'CRC7', 19: 'CRC7', 20: 'CRC8', 21: 'CRC8',
# 22: 'CRC8', 23: 'CRC9'}, 1: {1: 'CRC1', 2: 'CRC1',
# 3: 'CRC1', 4: 'CRC2', 5: 'CRC2', 6: 'CRC2',
# 7: 'CRC3', 8: 'CRC3', 9: 'CRC3', 10: 'CRC4',
# 11: 'CRC4', 12: 'CRC5', 13: 'CRC5', 14: 'CRC5',
# 15: 'CRC6', 16: 'CRC6', 17: 'CRC7', 18: 'CRC7',
# 19: 'CRC7', 20: 'CRC8', 21: 'CRC8', 22: 'CRC8',
# 23: 'CRC9', 24: 'CRC9'}}
# for line, chambers in in_operation.items():
#     in_operation[int(line)] = in_operation.pop(line)
