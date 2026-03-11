from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response, render_template, redirect, url_for
from app.models import Account, User
from app.config.ext import db

account_bp = Blueprint('account', __name__, url_prefix='/accounts')


@account_bp.route('/', methods=['GET'])
def list_accounts():
    """
    Render accounts list page
    ---
    tags:
      - Account Web
    """
    accounts = Account.query.all()
    return render_template('accounts/index.html', accounts=accounts)

@account_bp.route('/create', methods=['GET', 'POST'])
def create_account_from_form():
    if request.method == 'POST':
        data = {
            'user_id': request.form.get('user_id'),
            'balance': request.form.get('balance', 0.0),
            'card_number': request.form.get('card_number')
        }
        new_account = Account.get_from_dto(data)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('account.list_accounts'))

    users = User.query.all()
    return render_template('accounts/create.html', users=users)

@account_bp.route('/api', methods=['GET'])
def get_all_accounts():
    """
    Get all accounts
    ---
    tags:
      - Account API
    responses:
      200:
        description: List of all bank accounts
        examples:
          application/json: [
            {
              "id": 1,
              "user_id": 1,
              "balance": 1500.50,
              "card_number": "1234567812345678"
            }
          ]
    """
    accounts = Account.query.all()
    return make_response(jsonify([a.put_into_dto() for a in accounts]), HTTPStatus.OK)


@account_bp.route('/api', methods=['POST'])
def create_account():
    """
    Create a new account
    ---
    tags:
      - Account API
    parameters:
      - in: body
        name: account
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
            balance:
              type: number
            card_number:
              type: string
          example:
            user_id: 1
            balance: 100.0
            card_number: "4444555566667777"
    responses:
      201:
        description: Account created
    """
    content = request.get_json()
    new_account = Account.get_from_dto(content)
    
    db.session.add(new_account)
    db.session.commit()
    return make_response(jsonify(new_account.put_into_dto()), HTTPStatus.CREATED)


@account_bp.route('/api/<int:acc_id>', methods=['GET'])
def get_account(acc_id: int):
    """
    Get account by id 
    ---
    tags:
      - Account API
    """
    account = Account.query.get(acc_id)
    if not account:
        return make_response(jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND)
    return make_response(jsonify(account.put_into_dto()), HTTPStatus.OK)


@account_bp.route('/api/<int:acc_id>', methods=['PUT'])
def update_account(acc_id: int):
    """
    Update account balance or card number
    ---
    tags:
      - Account API
    """
    account = Account.query.get(acc_id)
    if not account:
        return make_response(jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND)
    
    content = request.get_json()
    account.balance = content.get('balance', account.balance)
    account.card_number = content.get('card_number', account.card_number)
    
    db.session.commit()
    return make_response("Account updated", HTTPStatus.OK)


@account_bp.route('/api/<int:acc_id>', methods=['DELETE'])
def delete_account(acc_id: int):
    """
    Delete account
    ---
    tags:
      - Account API
    """
    account = Account.query.get(acc_id)
    if not account:
        return make_response(jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND)
    
    db.session.delete(account)
    db.session.commit()
    return make_response("Account deleted", HTTPStatus.OK)