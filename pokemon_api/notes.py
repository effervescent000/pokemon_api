from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from .models import Note
from .schema import NoteSchema

from . import db

bp = Blueprint("note", __name__, url_prefix="/note")
one_note_schema = NoteSchema()
multi_note_schema = NoteSchema(many=True)


# GET endpoints


@bp.route("/get/<pokemon>", methods=["GET"])
def get_notes_by_pokemon(pokemon):
    notes = Note.query.filter_by(pokemon_id=pokemon).all()
    return jsonify(multi_note_schema.dump(notes))


# POST endpoints
@bp.route("/add", methods=["POST"])
@jwt_required()
def add_note():
    data = request.get_json()
    content = data.get("content")
    private = data.get("private")
    pokemon_id = data.get("pokemon")

    note = Note(pokemon_id=pokemon_id, content=content, private=private, user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    return jsonify(one_note_schema.dump(note))
