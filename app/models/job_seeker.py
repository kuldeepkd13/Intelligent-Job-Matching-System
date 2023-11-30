from . import db

class JobSeeker(db.Model):
    __tablename__ = 'job_seeker'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=True)
    skills = db.Column(db.String(100))
    
    EXPERIENCE_CHOICES = ['Entry Level', 'Mid Level', 'Senior']
    experience = db.Column(db.String(20), nullable=False, default='Entry Level')
    
    bio = db.Column(db.Text)
    availability = db.Column(db.Date)

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
