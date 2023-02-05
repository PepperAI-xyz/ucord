import requests, os, json, threading, time, websocket
from .user import User
from .interaction import Interaction
from .guild import Guild

API_URL = "https://discord.com/api"

class Client:
    def __init__(self):
        self.token = None
        self.application_id = None
        self.commands = {}
        self.on_ready_ = None

    def get_guilds(self):
        guilds = []
        x = self.session.get(f"{API_URL}/users/@me/guilds")
        for guild in x.json():
            guilds.append(Guild(
                id=guild.get("id", None),
                name=guild.get("name", None),
                icon=guild.get("icon", None),
                owner=guild.get("owner", False),
                member_count=guild.get("member_count", 0),
                permissions=guild.get("permissions", 0)
            ))
        return guilds
        
    def set_token(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bot {self.token}"})

    def set_presence(self, presence):
        while not self.ws:
            pass
        
        self.ws.send(json.dumps({
            "op": 3,
            "d": {
                "since": None,
                "activities": [
                    {
                        "name": presence.activity,
                        "type": presence.type
                    }
                ],
                "status": presence.status,
                "afk": False
            }
        }))

    def slash_command(self, name, description, options=[]):
        threading.Thread(target=self._slash_register, args=(name, description, options)).start()
        def decorator(func):
            self.commands[name] = func
        return decorator

    def on_ready(self, func):
        self.on_ready_ = func

    def run(self, intents = 0):
        self.ws = websocket.create_connection("wss://gateway.discord.gg/?v=8&encoding=json")
        self.interval = json.loads(self.ws.recv())["d"]["heartbeat_interval"] / 1000
        self.ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "intents": intents,
                "properties": {
                    "$os": os.name,
                    "$browser": "Ucord v0.1",
                    "$device": "Ucord v0.1"
                }
            }
        }))
        threading.Thread(target=self._heartbeat).start()
        threading.Thread(target=self._websocket).start()

    def _slash_register(self, name, description, options=[]):
        while not self.application_id:
            pass
            
        if self.application_id:
            payload = {
                "name": name,
                "description": description,
                "options": options
            }
            self.session.post(f"{API_URL}/applications/{self.application_id}/commands", json=payload)

    def _heartbeat(self):
        while True:
            time.sleep(self.interval)
            self.ws.send(json.dumps({"op": 1, "d": None}))

    def _websocket(self):
        while True:
            data = json.loads(self.ws.recv())
            if not os.path.exists("cache.json"):
                open("cache.json", "w").write(json.dumps(data, indent=4))
                open("cache.json", "a").write("\n\n")
            else:
                open("cache.json", "a").write(json.dumps(data, indent=4))
                open("cache.json", "a").write("\n\n")
            if data["t"] == "READY":
                client = User(id=data["d"]["user"]["id"], username=data["d"]["user"]["username"], discriminator=data["d"]["user"]["discriminator"])
                self.application_id = data["d"]["user"]["id"]
                threading.Thread(target=self.on_ready_, args=(client,)).start()
            if data["t"] == "INTERACTION_CREATE":
                if data["d"]["type"] == 3:
                    return
                    
                author = User(
                    id=data["d"]["member"]["user"]["id"],
                    username=data["d"]["member"]["user"]["username"],
                    discriminator=data["d"]["member"]["user"]["discriminator"]
                )
                interaction = Interaction(
                    author=author,
                    id=data["d"]["id"],
                    token=data["d"]["token"],
                    name=data["d"]["data"]["name"],
                    options=data["d"]["data"].get("options", []),
                    channel_id=data["d"]["channel_id"],
                    guild_id=data["d"]["guild_id"],
                    application_id=data["d"]["application_id"],
                    type=data["d"]["type"]
                )
                if interaction.name in self.commands:
                    format_interactions = (interaction.options[i]["value"] for i in range(len(interaction.options)))
                    if len(interaction.options) == 0:
                        threading.Thread(target=self.commands[interaction.name], args=(interaction,)).start()
                    else:
                        threading.Thread(target=self.commands[interaction.name], args=(interaction, *format_interactions)).start()
                    interaction.options = []
    

        