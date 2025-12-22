# schema_registry.py

SCHEMA = {
    "marks": {
        "description": "Marks obtained by a student in a subject",
        "columns": {
            "student_id": "Unique student identifier",
            "subject_id": "id of the subject in which the student obtained marks",
            "marks": "Marks obtained by the student in the subject"
        }
    },
    "subjects": {
        "description": "Subjects available",
        "columns": {
            "subject_id": "Unique subject identifier",
            "subject": "Name of the subject"
        }
    },
    "students": {
        "description": "Students available",
        "columns": {
            "student_id": "Unique student identifier",
            "name": "Name of the student"
        }
    }
}

ENTITY_KEYS = {
    "students": "student_id",
    "subjects": "subject_id"
}


JOINS = {
    ("marks", "student_id"): ("students", "student_id"),
    ("marks", "subject_id"): ("subjects", "subject_id")
}
