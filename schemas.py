from marshmallow import Schema, fields


class UserLogin(Schema):
    username = fields.String(load_only=True)
    password = fields.String(load_only=True)

class NewUser(UserLogin):
    favorite_quote = fields.String(load_only=True)
    
class UserData(Schema):
    username = fields.String(dump_only=True)
    favorite_quote = fields.String(dumpy_only=True)