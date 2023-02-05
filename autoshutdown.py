import pickle
import json
from os import environ
from googleapiclient import discovery
from rcon.source import Client as rcon

with open("configuration.json", "r") as config: 
	data = json.load(config)
	try:
		project = data["project_id"]
		zone = data["zone"]
		instance = data["instance_name"]
		environ["GOOGLE_APPLICATION_CREDENTIALS"] = data["gac_path"]
		rconconf = data["rcon"]
	except:
		print("failed to load config please run main.py before running this script.")
		exit()

port = rconconf["port"]
password = rconconf["password"]

service = discovery.build("compute", "v1")
try:
	server_ip = service.instances().get(project=project, zone=zone, instance=instance).execute()["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
except KeyError:
	print("Server seems to be offline or unreachable")
	exit()
	
try:
	with open("prev_check.pk", "rb") as fi:
		prev_check = pickle.load(fi)
	fi.close()
except:
	with open("prev_check.pk", "w+b") as fi:
		pickle.dump(False, fi)
	fi.close()
	prev_check = False

with rcon(server_ip, port, passwd=password) as connection:
		response = connection.run('playerlist')
		if response.count("\n") == 0:
			zero_players = True
		else:
			zero_players = False
		

if prev_check == True and zero_players == True:
	service.instances().stop(project=project, zone=zone, instance=instance).execute()
	zero_players = False
	with open("prev_check.pk", "wb") as fi:
		pickle.dump(zero_players, fi)
	fi.close()
else:
	with open("prev_check.pk", "wb") as fi:
		pickle.dump(zero_players, fi)
	fi.close()