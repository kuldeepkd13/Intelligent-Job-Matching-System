from . import db

class Application(db.Model):
    __tablename__ = 'Applications'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='Pending')
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)

    job_posting = db.relationship('JobPosting', backref='applications')