from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response, render_template, redirect, url_for
from app.models.user import User
from app.config.ext import db

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def list_users():
    """
    Render users list page
    ---
    tags:
      - User Web
    responses:
      200:
        description: HTML page with users table
    """
    users = User.query.all()
    return render_template('users/index.html', users=users)


@user_bp.route('/api', methods=['GET'])
def get_all_users():
    """
    Get all users
    ---
    tags:
      - User API
    responses:
      200:
        description: List of users
        examples:
          application/json: [
            {
              "id": 1,
              "name": "Ivan",
              "surname": "Ivanov",
              "email": "ivan@example.com",
              "tax_id": "1234567890"
            }
          ]
    """
    users = User.query.all()
    return make_response(jsonify([u.put_into_dto() for u in users]), HTTPStatus.OK)


@user_bp.route('/api', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - User API
    consumes:
      - application/json
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            surname:
              type: string
            email:
              type: string
            password:
              type: string
            tax_id:
              type: string
          required:
            - name
            - email
            - password
          example:
            name: "Oleg"
            surname: "Petrenko"
            email: "oleg@mail.com"
            password: "securepassword123"
            tax_id: "9876543210"
    responses:
      201:
        description: User created
    """
    content = request.get_json()
    new_user = User(
        name=content.get('name'),
        surname=content.get('surname'),
        email=content.get('email'),
        password=content.get('password'),
        tax_id=content.get('tax_id')
    )
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(new_user.put_into_dto()), HTTPStatus.CREATED)


@user_bp.route('/api/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """
    Get a user by ID
    ---
    tags:
      - User API
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: User found
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if user is None:
        return make_response(jsonify({"error": "User not found"}), HTTPStatus.NOT_FOUND)
    return make_response(jsonify(user.put_into_dto()), HTTPStatus.OK)


@user_bp.route('/api/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    """
    Update a user by ID
    ---
    tags:
      - User API
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
      - in: body
        name: user
        schema:
          type: object
          properties:
            name:
              type: string
            surname:
              type: string
    responses:
      200:
        description: User updated
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if user is None:
        return make_response(jsonify({"error": "User not found"}), HTTPStatus.NOT_FOUND)
    
    content = request.get_json()
    user.name = content.get('name', user.name)
    user.surname = content.get('surname', user.surname)
    user.email = content.get('email', user.email)
    
    db.session.commit()
    return make_response("User updated", HTTPStatus.OK)


@user_bp.route('/api/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    """
    Delete a user by ID
    ---
    tags:
      - User API
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: User deleted
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if user is None:
        return make_response(jsonify({"error": "User not found"}), HTTPStatus.NOT_FOUND)
    
    db.session.delete(user)
    db.session.commit()
    return make_response("User deleted", HTTPStatus.OK)