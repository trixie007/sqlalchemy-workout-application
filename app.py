from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)


# Initialize schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


# Helper function for error responses
def error_response(message, status_code):
    return jsonify({"error": message}), status_code


# Ensure request contains a JSON object
def read_json():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValidationError({
            "_schema": ["Request body must be a JSON object."]
        })

    return data


# HOME ROUTE
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Workout Tracking API"
    })



# WORKOUT ENDPOINTS


# GET all workouts
@app.route("/workouts", methods=["GET"])
def get_workouts():

    workouts = Workout.query.all()

    return jsonify(workouts_schema.dump(workouts)), 200


# GET one workout
@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):

    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error_response("Workout not found", 404)

    return jsonify(workout_schema.dump(workout)), 200


# CREATE workout
@app.route("/workouts", methods=["POST"])
def create_workout():

    try:
        data = workout_schema.load(read_json())

        workout = Workout(
            date=data["date"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes")
        )

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response("Invalid workout data", 400)


# DELETE workout
@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):

    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error_response("Workout not found", 404)

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully"
    }), 200



# EXERCISE ENDPOINTS


# GET all exercises
@app.route("/exercises", methods=["GET"])
def get_exercises():

    exercises = Exercise.query.all()

    return jsonify(exercises_schema.dump(exercises)), 200


# GET one exercise
@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):

    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error_response("Exercise not found", 404)

    return jsonify(exercise_schema.dump(exercise)), 200


# CREATE exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():

    try:
        data = exercise_schema.load(read_json())

        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data["equipment_needed"]
        )

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response(
            "An exercise with that name may already exist",
            400
        )


# DELETE exercise
@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):

    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error_response("Exercise not found", 404)

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully"
    }), 200



# WORKOUT-EXERCISE ENDPOINT


# ADD exercise to workout
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error_response("Workout not found", 404)

    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error_response("Exercise not found", 404)

    try:
        data = workout_exercise_schema.load(read_json())

        workout_exercise = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(
            workout_exercise_schema.dump(workout_exercise)
        ), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return error_response("Invalid workout exercise data", 400)


# ==========================================
# ERROR HANDLER
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return error_response("Resource not found", 404)


# RUN APPLICATION
if __name__ == "__main__":
    app.run(port=5555, debug=True)