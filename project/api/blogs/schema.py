from marshmallow import Schema, fields


class VerifyUser(Schema):
    """Schema for the end user verification"""

    username = fields.String(required=True)
    hashed_password = fields.String(required=True, data_key="password")


verify_user_schema = VerifyUser()
