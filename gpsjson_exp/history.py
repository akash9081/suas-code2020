import json
with open('gps_cor.json') as p:
	data2 = json.load(p)
print(json.dumps(data2, indent = 4, sort_keys=True))
data2
data2["JTT"]["track"]
data2["JTT"]
data2["JTT"][1]
data2["JTT"][0]
data2["JTT"][0]["track"]
data2["JTT"][0]["track"]["segments"][1]
data2["JTT"][0]["track"]["segments"][1][0]
corr=data2["JTT"][0]["track"]["segments"][1]
corr[0]
corr[1]
for i in corr:
	print('north : ',i[1])
	print('east  : ',i[0])
	print(':)')
import readline
readline.write_history_file('history.txt')
