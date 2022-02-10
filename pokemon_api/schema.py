from . import ma


class NoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "content", "user_id", "pokemon_id", "private")


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")
