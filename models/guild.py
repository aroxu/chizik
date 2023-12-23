from uuid import uuid4
from sqlalchemy import Column, Text, Boolean
from db.index import DB


class Guild(DB().Base):
    __tablename__ = "guilds"
    guild_id = Column(Text)
    streamer_id = Column(Text)
    alert_channel = Column(Text)
    alert_text = Column(Text)
    activated = Column(Boolean)
    is_streaming = Column(Boolean)
    uuid = Column(Text, primary_key=True)

    def __init__(self, guild_id, streamer_id, alert_channel, alert_text, activated, is_streaming=None, uuid=""):
        if uuid == "":
            uuid = str(uuid4())
        self.guild_id = guild_id
        self.streamer_id = streamer_id
        self.alert_channel = alert_channel
        self.alert_text = alert_text
        self.activated = activated
        self.is_streaming = is_streaming
        self.uuid = uuid
