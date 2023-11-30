
from datetime import datetime

from . import db


class JobPosting(db.Model):
    __tablename__ = 'job_posting'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Open')
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    hiring_manager_id = db.Column(db.Integer, db.ForeignKey('hiring_manager.id'), nullable=False)

    def get_hiring_manager(self):
        from models.hiring_manager import HiringManager
        return HiringManager.query.get(self.hiring_manager_id)