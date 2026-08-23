from typing import NamedTuple, Optional


class Signpost(NamedTuple):
    title: str
    description: Optional[str] = None

    # Which alert template renders this signpost. Computed by SignpostParser
    # instead of comparing strings inside the template. See issue #11.
    kind: str = "generic"

    def to_json_serialisable(self):
        return {"title": self.title, "description": self.description, "kind": self.kind}

    @classmethod
    def from_json(cls, json):
        return cls(**json)
