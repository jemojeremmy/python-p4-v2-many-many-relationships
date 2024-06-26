from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy.orm import relationship

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Association Table for Employee-Meeting Many-to-Many Relationship
employee_meeting_association = Table('employee_meeting_association', db.Model.metadata,
                                     db.Column('employee_id', db.Integer, db.ForeignKey('employees.id')),
                                     db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'))
                                     )

# Association Table for Employee-Project Many-to-Many Relationship
employee_project_association = Table('employee_project_association', db.Model.metadata,
                                     db.Column('employee_id', db.Integer, db.ForeignKey('employees.id')),
                                     db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
                                     )


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)

    meetings = db.relationship('Meeting', secondary=employee_meeting_association, back_populates='attendees')
    projects = db.relationship('Project', secondary=employee_project_association, back_populates='assigned_to')

    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    scheduled_time = db.Column(db.DateTime)
    location = db.Column(db.String)

    attendees = db.relationship('Employee', secondary=employee_meeting_association, back_populates='meetings')

    def __repr__(self):
        return f'<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    budget = db.Column(db.Integer)

    assigned_to = db.relationship('Employee', secondary=employee_project_association, back_populates='projects')

    def __repr__(self):
        return f'<Project {self.id}, {self.title}, {self.budget}>'
