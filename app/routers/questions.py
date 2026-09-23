from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.orm import selectinload

from app.models import db, Question, Category
from app.schemas.questions import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    QuestionsList,
)

questions_bp = Blueprint(
    "questions",
    __name__,
    url_prefix="/questions",
)

def _get_question_or_404(question_id: int):
    # Оптимизированный запрос с подгрузкой категории
    question = db.session.scalar(
        db.select(Question)
        .where(Question.id == question_id)
        .options(selectinload(Question.category))
    )
    if question is None:
        return None, (
            jsonify({"error": f"Question with id={question_id} not found"}),
            404,
        )
    return question, None


@questions_bp.route("", methods=["GET"])
def get_questions():
    """GET /questions: возвращает вопросы с информацией о категориях."""
    questions = db.session.scalars(
        db.select(Question).options(selectinload(Question.category))
    ).all()
    result = QuestionsList.dump_python(questions)
    return jsonify(result), 200


@questions_bp.route("", methods=["POST"])
def create_question():
    """POST /questions: позволяет указывать категорию при создании вопроса."""
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    try:
        question_in = QuestionCreate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({
            "error": "Validation error",
            "details": exc.errors(),
        }), 422

    # Проверяем реальное существование категории в БД
    if question_in.category_id is not None:
        category = db.session.get(Category, question_in.category_id)
        if not category:
            return jsonify({"error": f"Category with id={question_in.category_id} does not exist"}), 400

    question = Question(
        text=question_in.text,
        category_id=question_in.category_id
    )
    db.session.add(question)
    db.session.commit()

    return jsonify(
        QuestionResponse.model_validate(question).model_dump()
    ), 201


@questions_bp.route("/<int:question_id>", methods=["GET"])
def get_question(question_id: int):
    question, error = _get_question_or_404(question_id)
    if error:
        return error
    return jsonify(QuestionResponse.model_validate(question).model_dump()), 200


@questions_bp.route("/<int:question_id>", methods=["PUT"])
def update_question(question_id: int):
    question, error = _get_question_or_404(question_id)
    if error:
        return error

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    try:
        question_in = QuestionUpdate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({
            "error": "Validation error",
            "details": exc.errors(),
        }), 422

    if question_in.category_id is not None:
        category = db.session.get(Category, question_in.category_id)
        if not category:
            return jsonify({"error": f"Category with id={question_in.category_id} does not exist"}), 400

    if question_in.text is not None:
        question.text = question_in.text
    question.category_id = question_in.category_id

    db.session.commit()
    return jsonify(QuestionResponse.model_validate(question).model_dump()), 200


@questions_bp.route("/<int:question_id>", methods=["DELETE"])
def delete_question(question_id: int):
    question, error = _get_question_or_404(question_id)
    if error:
        return error

    db.session.delete(question)
    db.session.commit()
    return "", 204
