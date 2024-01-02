from uuid import uuid4
from peewee import BooleanField, TextField, UUIDField

from db.index import BaseModel

class Alert(BaseModel):
    guild_id = TextField()
    streamer_id = TextField()
    alert_channel = TextField()
    alert_text = TextField()
    activated = BooleanField()
    is_streaming = BooleanField()
    uuid = UUIDField(primary_key=True, default=uuid4)

    class Meta:
        table_name = "alerts"