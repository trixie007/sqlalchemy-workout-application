from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

#entities
class exercise(db.Model):
    __tablename__ = 'exercise'
    
    #constaints
    __table_args__ = (db.UniqueConstraint('name', name='unique_exercise_name'),)


    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100) )
    category=db.Column(db.String(100) )
    equipment=db.Column(db.String(100))

    #relationships
    workoutExercises = db.relationship('workoutExercises', back_populates='exercise', lazy=True)
    workout = db.relationship('workout', secondary='workout_exercises', back_populates='exercises', lazy=True)

    #validation

    @validates('name')
    def validate_name(self, key, name):
        if not value or not name.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value.strip()
    

class workout(db.Model):
    __tablename__ = "workout"

    __table_args__ = (db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),)


    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    workoutExercises = db.relationship('workoutExercises', back_populates='workout', lazy=True)
    exercises = db.relationship('exercise', secondary='workout_exercises', back_populates='workout', lazy=True)

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError('Workout duration must be greater than zero.')

        return value



class workoutExercises(db.Model):
    __tablename__ = "workout_exercises"
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)


    workout = db.relationship('workout', back_populates='workoutExercises', lazy=True)
    exercise = db.relationship('exercise', back_populates='workoutExercises', lazy=True)




















                            