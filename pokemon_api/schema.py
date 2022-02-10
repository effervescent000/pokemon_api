from . import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")


one_user_schema = UserSchema()


class NoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "content", "user_id", "pokemon_id", "private", "user")

    user = ma.Nested(one_user_schema)
