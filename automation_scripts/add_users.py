# import urllib.request
# import pandas as pd
# from sqlalchemy import update
#
# from project import db
# from project.api.jobs import Job
#
#
# def update_job_status(url, job_id):
#     datafile = urllib.request.urlopen(url)
#     df = pd.read_excel(datafile)
#     for row in df[1:]:
#         print("abc")
#     #     update_job = update(Job).values(data).where(Job.job_id == job_id)
#     #     db.session.execute(update_job)
#     # db.session.commit()
