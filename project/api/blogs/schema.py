from marshmallow import Schema, fields


class BlogSchema(Schema):
    """Schema for the end user verification"""
    blog_id = fields.String()
    time = fields.String()
    username = fields.String()
    title = fields.String()
    content = fields.String()


blog_schema = BlogSchema(many=True)
