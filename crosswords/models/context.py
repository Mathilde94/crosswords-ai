from pydantic import BaseModel


class CrosswordContext(BaseModel):
    title: str
    section: str
    extracts: str

    def serialize(self):
        return {"title": self.title, "section": self.section, "extracts": self.extracts}

    @staticmethod
    def from_serialized(data: dict):
        return CrosswordContext(
            title=data["title"], section=data["section"], extracts=data["extracts"]
        )
