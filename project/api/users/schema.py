from marshmallow import Schema, fields


class VerifyUser(Schema):
    """Schema for getting user detials"""

    username = fields.String(required=True)


verify_user_schema = VerifyUser()
