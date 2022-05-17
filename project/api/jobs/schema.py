from marshmallow import Schema, fields


class JobSchema(Schema):
    job_id = fields.UUID()
    job_type = fields.String()
    job_role = fields.String()
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
    jd_link = fields.String()
    extras = fields.String()


class JobDescription(Schema):
    job_id = fields.UUID()




jobdescriptionschema = JobDescription()
jobschema = JobSchema(many=True)
