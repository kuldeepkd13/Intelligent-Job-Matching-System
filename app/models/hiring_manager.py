from . import db

class HiringManager(db.Model):
    __tablename__ = 'hiring_manager'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def get_job_postings(self):
        from models.job_posting import JobPosting
        return JobPosting.query.filter_by(hiring_manager_id=self.id).all()