import requests
from .user import User

API_URL = "https://discord.com/api"

class Interaction:
    def __init__(self, author, token, channel_id, guild_id, name, options, id, application_id, type):
        self.author = author
        self.token = token
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.name = name
        self.options = options
        self.id = id
        self.application_id = application_id
        self.type = type

    def __repr__(self):
        return f"Ucord.Interaction(author={self.author}, token={self.token}, channel_id={self.channel_id}, guild_id={self.guild_id}, name={self.name}, options={self.options}, id={self.id}, application_id={self.application_id}, type={self.type})"

    def reply(self, content = None, embed = None, files = None, ephemeral = False, components = None):
        payload = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": [embed._to_dict()] if embed else [],
                "flags": 64 if ephemeral else 0,
                "components": [component._to_dict() for component in components] if components else []
            }
        }
        if files:
            files = {"file": open(files, "rb")}
            requests.post(f"{API_URL}/interactions/{self.id}/{self.token}/callback", json=payload)
            requests.patch(f"{API_URL}/webhooks/{self.application_id}/{self.token}/messages/@original", json=payload, files=files)
            return

        x = requests.post(f"{API_URL}/interactions/{self.id}/{self.token}/callback", json=payload, files=files)
        print(x.text)

    def edit(self, content = None, embed = None, files = None, components = None):
        payload = {
            "content": content,
            "embeds": [embed._to_dict()] if embed else [],
            "components": [component._to_dict() for component in components] if components else []
        }
        
        if files:
            files = {"file": open(files, "rb")}
            requests.patch(f"{API_URL}/webhooks/{self.application_id}/{self.token}/messages/@original", json=payload)
            requests.patch(f"{API_URL}/webhooks/{self.application_id}/{self.token}/messages/@original", json=payload, files=files)
            return

        requests.patch(f"{API_URL}/webhooks/{self.application_id}/{self.token}/messages/@original", json=payload, files=files)