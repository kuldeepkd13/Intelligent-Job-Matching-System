from . import db


class SkillSet(db.Model):
    __tablename__ = 'skill_set.py'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)

    job_posting = db.relationship('JobPosting', backref='skill_sets')