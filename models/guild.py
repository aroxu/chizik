from uuid import uuid4
from peewee import BooleanField, TextField

from db.index import DB, BaseModel

class Guild(BaseModel):
    guild_id = TextField()
    streamer_id = TextField()
    alert_channel = TextField()
    alert_text = TextField()
    activated = BooleanField()
    is_streaming = BooleanField()
    uuid = TextField(primary_key=True, default=str(uuid4()))

    class Meta:
        db_table = "guilds"