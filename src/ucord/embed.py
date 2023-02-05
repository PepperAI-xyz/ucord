class Embed:
    def __init__(self, title = None, description = None, url = None, color = None, timestamp = None, footer = None, image = None, thumbnail = None, author = None):
        self.title = title
        self.description = description
        self.url = url
        self.color = color
        self.timestamp = timestamp
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.author = author
        self.fields = []
        self.attachments = []
    
    def __repr__(self):
        return f"Ucord.Embed(title={self.title}, description={self.description}, url={self.url}, color={self.color}, timestamp={self.timestamp}, footer={self.footer}, image={self.image}, thumbnail={self.thumbnail}, author={self.author}, fields={self.fields})"

    def _to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "color": self.color,
            "timestamp": self.timestamp,
            "footer": self.footer,
            "image": self.image,
            "thumbnail": self.thumbnail,
            "author": self.author,
            "fields": self.fields,
            "attachments": self.attachments
        }

    def add_field(self, name, value, inline = False):
        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })

    def set_footer(self, text, icon_url = None):
        self.footer = {
            "text": text,
            "icon_url": icon_url
        }

    def set_image(self, url):
        self.image = {
            "url": url
        }

    def set_thumbnail(self, url):
        self.thumbnail = {
            "url": url
        }