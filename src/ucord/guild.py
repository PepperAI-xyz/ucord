class Guild:
    def __init__(self, id, name, icon, owner, member_count, permissions):
        self.id = id
        self.name = name
        self.icon = icon
        self.owner = owner
        self.member_count = member_count
        self.permissions = permissions

    def __repr__(self):
        return f"Guild(id={self.id}, name={self.name}, icon={self.icon}, owner={self.owner}, member_count={self.member_count}, permissions={self.permissions})"