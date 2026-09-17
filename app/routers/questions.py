from flask import Blueprint, jsonify, request
from sqlalchemy import select
from app.models import Question, db
from app.schemas.questions import QuestionRead, QuestionCreate, QuestionsList, QuestionUpdate
from pydantic import ValidationError

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


# @questions_bp.route('', methods=['GET'])
# def get_questions():
#     """Получение списка всех вопросов."""
#     questions = db.session.scalars(select(Question))
#     result = [QuestionRead.model_validate(q).model_dump() for q in questions]
#     return jsonify(result), 200

@questions_bp.route('', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов."""
    questions = db.session.scalars(select(Question))
    result = QuestionsList.dump_python(QuestionsList.validate_python(questions))
    return jsonify(result), 200

@questions_bp.route('', methods=['POST'])
def create_question():
    """Создание вопроса."""
    try:
        data = request.get_json()
        question = QuestionCreate.model_validate(data)

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422

    question = Question(text=question.text)
    db.session.add(question)
    db.session.commit()

    return jsonify(QuestionRead.model_validate(question).model_dump()), 201





@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = db.session.get(Question, id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    db.session.delete(question)
    db.session.commit()
    return "", 204

@questions_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_question(id):
    question = db.session.get(Question, id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    payload = request.get_json(silent=True) or {}
    try:
        q = QuestionUpdate.model_validate(payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422
    question.text = q.text
    db.session.commit()
    return jsonify(QuestionRead.model_validate(question).model_dump()), 200

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    question = db.session.get(Question, id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    return jsonify(QuestionRead.model_validate(question).model_dump()), 200
