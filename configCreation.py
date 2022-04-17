import json
from os.path import exists

class ConfigCreation():

    def createConfig(name: str, payload: json, cog: bool = False):
        if cog == True:
            if exists("Cogs/Configs/{}.json".format(name)) == False:
                with open("Cogs/Configs/{}.json".format(name), "w") as config:
                    json.dump(payload, config, ensure_ascii=False, indent=4)
                config.close()
        elif cog == False:
            if exists("{}.json".format(name)) == False:
                with open("{}.json".format(name), "w") as config:
                    json.dump(payload, config, ensure_ascii=False, indent=4)
                config.close()