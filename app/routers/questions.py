from flask import Blueprint


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('', methods=['GET'])
def get_questions():
    pass

@questions_bp.route('', methods=['POST'])
def create_question():
    pass

@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    pass

@questions_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_question(id):
    pass

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    pass