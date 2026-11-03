#!/usr/bin/env python3

from datetime import date, timedelta

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():

    # Create tables if they do not exist
    db.create_all()

    # Clear existing records
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

   
    # CREATE EXERCISES


    push_up = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False
    )

    squat = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=False
    )

    treadmill = Exercise(
        name="Treadmill Run",
        category="Cardio",
        equipment_needed=True
    )

  
    # CREATE WORKOUTS
    

    workout_one = Workout(
        date=date.today(),
        duration_minutes=45,
        notes="Full body strength training"
    )

    workout_two = Workout(
        date=date.today() - timedelta(days=1),
        duration_minutes=30,
        notes="Cardio training"
    )

    # Add exercises and workouts
    db.session.add_all([
        push_up,
        squat,
        treadmill,
        workout_one,
        workout_two
    ])

    db.session.flush()

  
    # CONNECT EXERCISES TO WORKOUTS
   

    first_association = WorkoutExercise(
        workout=workout_one,
        exercise=push_up,
        reps=12,
        sets=3
    )

    second_association = WorkoutExercise(
        workout=workout_one,
        exercise=squat,
        reps=10,
        sets=4
    )

    third_association = WorkoutExercise(
        workout=workout_two,
        exercise=treadmill,
        duration_seconds=900
    )

    db.session.add_all([
        first_association,
        second_association,
        third_association
    ])

    db.session.commit()

    print("Database seeded successfully!")

    print("Exercises:", Exercise.query.count())

    print("Workouts:", Workout.query.count())

    print("Workout exercises:", WorkoutExercise.query.count())