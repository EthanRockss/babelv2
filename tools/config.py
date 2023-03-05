import os
import json
import discord

DEFAULT_CONFIG = {
    "token": "",
    "owner_id": 0,
	"project_id": "",
	"zone": "",
	"instance_name": "",
	"server_pass": "",
	"gac_path": "",
	"primary_guild": 0,
	"rcon": {
		"password": "",
		"port": 0
	}
}

def createconfig():
    if not os.path.exists("configuration.json"):
        with open("configuration.json", "w", encoding="utf-8") as config:
            json.dump(DEFAULT_CONFIG, config, ensure_ascii=False, indent=4)
            message = "Created config file, fill it out."
    else:
        message = "Config file already exists"
    print(message)

class Config:
    def loadconfig(key:str="11111111"):
        """10000000: token\n01000000: owner_id\n00100000: project\n00010000: zone\n00001000: server_pass\n00000100: instance\n00000010: PRIMARY_GUILD\n00000001: rconconf"""
        with open("configuration.json", "r") as config:
            data = json.load(config)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = data["gac_path"]
            token = data["token"]
            owner_id = data["owner_id"]
            project = data["project_id"]
            zone = data["zone"]
            server_pass = data["server_pass"]
            instance = data["instance_name"]
            PRIMARY_GUILD = discord.Object(id=data["primary_guild"])
            rconconf = data["rcon"]
        config.close()
        vars = (token, owner_id, project, zone, server_pass, instance, PRIMARY_GUILD, rconconf)
        results = ()
        for n, i in enumerate(key):
            if i == "1":
                results = results + (vars[n],)
        return results