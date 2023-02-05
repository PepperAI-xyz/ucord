class User:
    def __init__(self, id, username, discriminator):
        self.id = id
        self.username = username
        self.discriminator = discriminator
        self.user = f"{self.username}#{self.discriminator}"

    def __repr__(self):
        return f"Ucord.User(id={self.id}, username={self.username}, discriminator={self.discriminator}, user={self.user})"