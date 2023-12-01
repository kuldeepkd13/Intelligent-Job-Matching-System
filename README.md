# Intelligent-Job-Matching-System

## Description
The Intelligent Job Matching System is a Flask-based backend application designed to facilitate seamless job matching between Job Seekers and Job Postings. It provides robust CRUD operations for managing Job Seeker profiles, Job Postings, Applications, Skill Sets, and Hiring Managers. The system emphasizes efficient database integration to enhance the accuracy and effectiveness of the job-matching process.



## ER Diagram

## Entity: Job Seeker

| Field          | Type            | Description              |
| -------------- | --------------- | ------------------------ |
| id (PK)        | Integer         | Primary Key              |
| name           | Text            | Name of the job seeker   |
| status         | Boolean         | Status of the job seeker |
| skills         | Text            | Skills possessed         |
| experience     | Enum            | Experience level         |
| bio            | Text            | Bio of the job seeker    |
| availability   | Date            | Availability date        |

---

## Entity: Job Posting

| Field           | Type            | Description                   |
| --------------- | --------------- | ----------------------------- |
| id (PK)         | Integer         | Primary Key                   |
| title           | Text            | Title of the job posting      |
| status          | Text            | Status of the job posting     |
| start_date      | Date            | Start date of the job posting |
| end_date        | Date            | End date of the job posting   |
| hiring_manager_id | FK (Job Posting) | Foreign Key to Hiring Manager |

---

## Entity: Application

| Field           | Type            | Description                 |
| --------------- | --------------- | --------------------------- |
| id (PK)         | Integer         | Primary Key                 |
| status          | Text            | Status of the application   |
| job_posting_id  | FK (Job Posting) | Foreign Key to Job Posting   |

---

## Entity: Skill Set

| Field           | Type            | Description                 |
| --------------- | --------------- | --------------------------- |
| id (PK)         | Integer         | Primary Key                 |
| name            | Text            | Name of the skill set        |
| job_posting_id  | FK (Job Posting) | Foreign Key to Job Posting   |

---

## Entity: Hiring Manager

| Field           | Type            | Description              |
| --------------- | --------------- | ------------------------ |
| id (PK)         | Integer         | Primary Key              |
| name            | Text            | Name of the hiring manager|




## API Endpoints

### Job Seekers

- GET /job_seekers: Get all Job Seekers.
- GET /job_seekers/int:id: Get Job Seeker by ID.
- POST /job_seekers: Create a new Job Seeker.
- PUT /job_seekers/int:id: Update Job Seeker by ID.
- DELETE /job_seekers/int:id: Delete Job Seeker by ID.


### Hiring Managers
- POST /hiring_managers: Create a new Hiring Manager.
- GET /hiring_managers: Get all Hiring Managers.

### Job Postings
- POST /job_postings: Create a new Job Posting.
- GET /job_postings: Get all Job Postings.
- GET /job_postings/int:id: Get Job Posting by ID.
- PUT /job_postings/int:id: Update Job Posting by ID.
- DELETE /job_postings/int:id: Delete Job Posting by ID.

### Applications
- GET /applications: Get all Applications.
- GET /applications/int:id: Get Application by ID.
- POST /applications: Create a new Application.
- PUT /applications/int:id: Update Application by ID.
- DELETE /applications/int:id: Delete Application by ID.

### Skill Sets
- GET /skill_sets: Get all Skill Sets.
- GET /skill_sets/int:id: Get Skill Set by ID.
- POST /skill_sets: Create a new Skill Set.
- PUT /skill_sets/int:id: Update Skill Set by ID.
- DELETE /skill_sets/int:id: Delete Skill Set by ID.


## Setup and Running Instructions
- Clone the Repository:
  -  https://github.com/kuldeepkd13/Intelligent-Job-Matching-System.git

- Create Virtual Environment:
   - python -m venv venv


- Activate Virtual Environment:
  - source venv/Scripts/activate


- Install Dependencies:
   - pip install -r requirements.txt


-  Run the Application: 
    - cd app
    - python app.py

-  Access API Endpoints:

   -  Open your web browser or API testing tool.
   - Use the provided API endpoints to interact with the Intelligent Job Matching System.

-  Deactivate Virtual Environment:
   - deactivate

