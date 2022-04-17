import json

DEFAULT_CONFIG = {
    "token": "",
    "prefix": "<",
    "owner_id": 0
}

class ConfigCreation():
    
    def createDefaultConfig():
        with open("configuration.json", "w") as config:
            json.dump(DEFAULT_CONFIG, config, ensure_ascii=False,indent=4)
        config.close()