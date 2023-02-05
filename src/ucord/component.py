class Component:
    def __init__(self, type):
        self.type = type
        self.components = []

    def __repr__(self):
        return f"Ucord.Component(type={self.type}, components={self.components})"

    def _to_dict(self):
        return {
            "type": self.type,
            "components": [component._to_dict() for component in self.components] if self.components else []
        }

    def add_component(self, component):
        self.components.append(component)

    def add_components(self, *components):
        self.components.extend(components)

class ActionRow(Component):
    def __init__(self):
        super().__init__(1)

    def __repr__(self):
        return f"Ucord.ActionRow(components={self.components})"

    def _to_dict(self):
        return {
            "type": self.type,
            "components": [component._to_dict() for component in self.components] if self.components else []
        }

class Button:
    def __init__(self, style, label, custom_id = None, url = None, disabled = False):
        self.style = style
        self.label = label
        self.custom_id = custom_id
        self.url = url
        self.disabled = disabled

    def __repr__(self):
        return f"Ucord.Button(style={self.style}, label={self.label}, custom_id={self.custom_id}, url={self.url}, disabled={self.disabled})"

    def _to_dict(self):
        return {
            "type": 2,
            "style": self.style,
            "label": self.label,
            "custom_id": self.custom_id,
            "url": self.url,
            "disabled": self.disabled
        }