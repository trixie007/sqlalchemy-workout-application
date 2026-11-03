from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    ValidationError
)


# EXERCISE SCHEMA


class ExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    name = fields.Str(required=True)

    category = fields.Str(required=True)

    equipment_needed = fields.Bool(required=True)

    workouts = fields.Nested(
        "WorkoutSummarySchema",
        many=True,
        dump_only=True
    )

    @validates("name")
    def validate_name(self, value, **kwargs):

        if not value.strip():
            raise ValidationError("Exercise name cannot be blank.")

        if len(value.strip()) > 120:
            raise ValidationError("Exercise name is too long.")

    @validates("category")
    def validate_category(self, value, **kwargs):

        if not value.strip():
            raise ValidationError("Category cannot be blank.")

        if len(value.strip()) > 80:
            raise ValidationError("Category is too long.")


# WORKOUT SUMMARY SCHEMA


class WorkoutSummarySchema(Schema):

    id = fields.Int(dump_only=True)

    date = fields.Date()

    duration_minutes = fields.Int()

    notes = fields.Str(allow_none=True)



# WORKOUT-EXERCISE SCHEMA


class WorkoutExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)

    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(allow_none=True, load_default=None)

    sets = fields.Int(allow_none=True, load_default=None)

    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None
    )

    exercise = fields.Nested(
        ExerciseSchema(
            only=("id", "name", "category", "equipment_needed")
        ),
        dump_only=True
    )

    @validates_schema
    def validate_measurements(self, data, **kwargs):

        for field_name in ("reps", "sets", "duration_seconds"):

            value = data.get(field_name)

            if value is not None and value <= 0:
                raise ValidationError({
                    field_name: ["Must be a positive integer."]
                })

        if all(
            data.get(field_name) is None
            for field_name in ("reps", "sets", "duration_seconds")
        ):
            raise ValidationError({
                "_schema": [
                    "Provide at least one of reps, sets, or duration_seconds."
                ]
            })


# WORKOUT SCHEMA


class WorkoutSchema(Schema):

    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(required=True)

    notes = fields.Str(allow_none=True, load_default=None)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )

    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):

        if value <= 0:
            raise ValidationError(
                "Workout duration must be positive."
            )