from marshmallow import Schema, fields


class JobSchema(Schema):
    job_id = fields.UUID()
    job_type = fields.String()
    company_name = fields.String()
    dept_allowed = fields.String()
    ctc = fields.Integer()
    location = fields.String()
    comp_address = fields.String()
    internship = fields.Boolean()
    job_desc = fields.String()
    placed_slab = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    extras = fields.String()


jobschema = JobSchema(many=True)
