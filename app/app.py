from flask import Flask, request, jsonify
from datetime import datetime , date
from models.job_seeker import db, JobSeeker
from models.job_posting import db , JobPosting
from models.hiring_manager import db, HiringManager
from models.application import db , Application
from models.skill_set import db , SkillSet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bkkjobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/job_seekers', methods=['GET'])
def get_job_seekers():
    job_seekers = JobSeeker.query.all()
    response_data = [
        {
            'id': job_seeker.id,
            'name': job_seeker.name,
            'status': job_seeker.status,
            'skills': job_seeker.skills,
            'experience': job_seeker.experience,
            'bio': job_seeker.bio,
            'availability': str(job_seeker.availability) if job_seeker.availability else None
        }
        for job_seeker in job_seekers
    ]
    return jsonify(response_data)

@app.route('/job_seekers/<int:id>', methods=['GET'])
def get_job_seeker_by_id(id):
    job_seeker = JobSeeker.query.get(id)
    if job_seeker:
        return jsonify({
            'id': job_seeker.id,
            'name': job_seeker.name,
            'status': job_seeker.status,
            'skills': job_seeker.skills,
            'experience': job_seeker.experience,
            'bio': job_seeker.bio,
            'availability': str(job_seeker.availability) if job_seeker.availability else None
        })
    return jsonify({'error': 'Job Seeker not found'}), 404


@app.route('/job_seekers', methods=['POST'])
def create_job_seeker():
    data = request.get_json()

    # Convert 'availability' string to Python date object
    if 'availability' in data and data['availability']:
        data['availability'] = datetime.strptime(data['availability'], '%Y-%m-%d').date()

    try:
        job_seeker = JobSeeker(**data)
        db.session.add(job_seeker)
        db.session.commit()
        return jsonify({
            'id': job_seeker.id,
            'name': job_seeker.name,
            'status': job_seeker.status,
            'skills': job_seeker.skills,
            'experience': job_seeker.experience,
            'bio': job_seeker.bio,
            'availability': str(job_seeker.availability) if job_seeker.availability else None
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/job_seekers/<int:id>', methods=['GET'])
def get_job_seeker(id):
    job_seeker = JobSeeker.query.get(id)
    if job_seeker:
        return jsonify(vars(job_seeker))
    return jsonify({'error': 'Job Seeker not found'}), 404

@app.route('/job_seekers/<int:id>', methods=['PUT'])
def update_job_seeker(id):
    job_seeker = JobSeeker.query.get(id)
    if not job_seeker:
        return jsonify({'error': 'Job Seeker not found'}), 404

    data = request.get_json()

    if 'availability' in data and data['availability']:
        data['availability'] = datetime.strptime(data['availability'], '%Y-%m-%d').date()

    try:
        job_seeker.update(data)

        db.session.commit()

        return jsonify({
            'id': job_seeker.id,
            'name': job_seeker.name,
            'status': job_seeker.status,
            'skills': job_seeker.skills,
            'experience': job_seeker.experience,
            'bio': job_seeker.bio,
            'availability': str(job_seeker.availability) if job_seeker.availability else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/job_seekers/<int:id>', methods=['DELETE'])
def delete_job_seeker(id):
    job_seeker = JobSeeker.query.get(id)
    if not job_seeker:
        return jsonify({'error': 'Job Seeker not found'}), 404

    db.session.delete(job_seeker)
    db.session.commit()
    return jsonify({'message': 'Job Seeker deleted successfully'})



def serialize_hiring_manager(hiring_manager):
    return {
        'id': hiring_manager.id,
        'name': hiring_manager.name,
        
    }

# hiring manager
@app.route('/hiring_managers', methods=['POST'])
def create_hiring_manager():
    data = request.get_json()
    hiring_manager = HiringManager(**data)

    db.session.add(hiring_manager)
    db.session.commit()

    return jsonify(serialize_hiring_manager(hiring_manager)), 201


# GET all hiring managers
@app.route('/hiring_managers', methods=['GET'])
def get_all_hiring_managers():
    hiring_managers = HiringManager.query.all()
    return jsonify([serialize_hiring_manager(manager) for manager in hiring_managers])

# job posting
def serialize_job_posting(job_posting):
    return {
        'id': job_posting.id,
        'title': job_posting.title,
        'status': job_posting.status,
        'start_date': str(job_posting.start_date) if job_posting.start_date else None,
        'end_date': str(job_posting.end_date) if job_posting.end_date else None,
        'hiring_manager_id': job_posting.hiring_manager_id,
    }

@app.route('/job_postings', methods=['POST'])
def create_job_posting():
    data = request.get_json()

    hiring_manager_id = data.get('hiring_manager_id')
    hiring_manager = HiringManager.query.get(hiring_manager_id)

    if not hiring_manager:
        return jsonify({'error': 'Hiring Manager not found'}), 404

    try:
        start_date_str = data.get('start_date', datetime.utcnow().strftime('%Y-%m-%d'))
        end_date_str = data.get('end_date')

        # Convert date strings to Python date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        job_posting = JobPosting(
            title=data.get('title'),
            status=data.get('status', 'Open'),
            start_date=start_date,
            end_date=end_date,
            hiring_manager_id=hiring_manager_id
        )

        db.session.add(job_posting)
        db.session.commit()

        return jsonify(serialize_job_posting(job_posting)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all job postings
@app.route('/job_postings', methods=['GET'])
def get_job_postings():
    job_postings = JobPosting.query.all()
    return jsonify([serialize_job_posting(job) for job in job_postings])

# Get job posting by ID
@app.route('/job_postings/<int:id>', methods=['GET'])
def get_job_posting(id):
    job_posting = JobPosting.query.get(id)
    if job_posting:
        return jsonify(serialize_job_posting(job_posting))
    return jsonify({'error': 'Job Posting not found'}), 404

# Update job posting by ID
@app.route('/job_postings/<int:id>', methods=['PUT'])
def update_job_posting(id):
    job_posting = JobPosting.query.get(id)

    if not job_posting:
        return jsonify({'error': 'Job Posting not found'}), 404

    try:
        data = request.get_json()

        # Update job posting fields
        for key, value in data.items():
            # Convert date strings to Python date objects
            if key in ['start_date', 'end_date'] and value:
                data[key] = datetime.strptime(value, '%Y-%m-%d').date()

            setattr(job_posting, key, data[key])

        db.session.commit()

        return jsonify(serialize_job_posting(job_posting))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete job posting by ID
@app.route('/job_postings/<int:id>', methods=['DELETE'])
def delete_job_posting(id):
    job_posting = JobPosting.query.get(id)

    if not job_posting:
        return jsonify({'error': 'Job Posting not found'}), 404

    db.session.delete(job_posting)
    db.session.commit()

    return jsonify({'message': 'Job Posting deleted successfully'})


# Application 

def serialize_application(application):
    return {
        'id': application.id,
        'status': application.status,
        'job_posting_id': application.job_posting_id,
        'job_posting_title': application.job_posting.title,
    }


@app.route('/applications', methods=['GET'])
def get_applications():
    applications = Application.query.all()
    return jsonify([serialize_application(application) for application in applications])

@app.route('/applications/<int:id>', methods=['GET'])
def get_application(id):
    application = Application.query.get(id)
    if application:
        return jsonify(serialize_application(application))
    return jsonify({'error': 'Application not found'}), 404

@app.route('/applications', methods=['POST'])
def create_application():
    data = request.get_json()

    job_posting_id = data.get('job_posting_id')
    job_posting = JobPosting.query.get(job_posting_id)

    if not job_posting:
        return jsonify({'error': 'Job Posting not found'}), 404

    try:
        application = Application(
            status=data.get('status', 'Pending'),
            job_posting_id=job_posting_id
        )

        db.session.add(application)
        db.session.commit()

        return jsonify(serialize_application(application)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/applications/<int:id>', methods=['PUT'])
def update_application(id):
    application = Application.query.get(id)

    if not application:
        return jsonify({'error': 'Application not found'}), 404

    try:
        data = request.get_json()

        # Update application fields
        for key, value in data.items():
            setattr(application, key, value)

        db.session.commit()

        return jsonify(serialize_application(application))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/applications/<int:id>', methods=['DELETE'])
def delete_application(id):
    application = Application.query.get(id)

    if not application:
        return jsonify({'error': 'Application not found'}), 404

    db.session.delete(application)
    db.session.commit()

    return jsonify({'message': 'Application deleted successfully'})


# skil_set

def serialize_skill_set(skill_set):
    return {
        'id': skill_set.id,
        'name': skill_set.name,
        'job_posting_id': skill_set.job_posting_id,
        'job_posting_title': skill_set.job_posting.title,
    }


@app.route('/skill_sets', methods=['GET'])
def get_skill_sets():
    skill_sets = SkillSet.query.all()
    return jsonify([serialize_skill_set(skill_set) for skill_set in skill_sets])

@app.route('/skill_sets/<int:id>', methods=['GET'])
def get_skill_set(id):
    skill_set = SkillSet.query.get(id)
    if skill_set:
        return jsonify(serialize_skill_set(skill_set))
    return jsonify({'error': 'Skill Set not found'}), 404

@app.route('/skill_sets', methods=['POST'])
def create_skill_set():
    data = request.get_json()

    job_posting_id = data.get('job_posting_id')
    job_posting = JobPosting.query.get(job_posting_id)

    if not job_posting:
        return jsonify({'error': 'Job Posting not found'}), 404

    try:
        skill_set = SkillSet(
            name=data.get('name'),
            job_posting_id=job_posting_id
        )

        db.session.add(skill_set)
        db.session.commit()

        return jsonify(serialize_skill_set(skill_set)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/skill_sets/<int:id>', methods=['PUT'])
def update_skill_set(id):
    skill_set = SkillSet.query.get(id)

    if not skill_set:
        return jsonify({'error': 'Skill Set not found'}), 404

    try:
        data = request.get_json()

        # Update skill set fields
        for key, value in data.items():
            setattr(skill_set, key, value)

        db.session.commit()

        return jsonify(serialize_skill_set(skill_set))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/skill_sets/<int:id>', methods=['DELETE'])
def delete_skill_set(id):
    skill_set = SkillSet.query.get(id)

    if not skill_set:
        return jsonify({'error': 'Skill Set not found'}), 404

    db.session.delete(skill_set)
    db.session.commit()

    return jsonify({'message': 'Skill Set deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)



