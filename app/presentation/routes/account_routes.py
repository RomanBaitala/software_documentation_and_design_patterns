from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response, render_template, redirect, url_for
from app.bll.services import account_services, user_service, transaction_service
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
    accounts = account_services.get_all_accounts()
    return render_template('accounts/index.html', accounts=accounts)

@account_bp.route('/create', methods=['GET', 'POST'])
def create_account_from_form():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        card_number = request.form.get('card_number')

        try:
            account_services.open_account(user_id=user_id, card_number=card_number)
            return redirect(url_for('user.list_users'))
        except Exception:
            return "Помилка бази даних", 400

    users = user_service.get_all_users()
    return render_template('accounts/create.html', users=users)

@account_bp.route('/deposit/<int:account_id>', methods=['GET', 'POST'])
def deposit_money(account_id):
    account = account_services.get_account_by_id(account_id)
    
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        try:
            transaction_service.make_deposit(account_id, amount)
            return redirect(url_for('account.list_accounts'))
        except Exception as e:
            return f"Помилка при поповненні: {str(e)}", 400

    return render_template('accounts/deposit.html', account=account)

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
    accounts = account_services.get_all_accounts()
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
    user_id = content.get('user_id')
    card_number = content.get('card_number')
    
    new_account = account_services.open_account(user_id=user_id, card_number=card_number)
    
    return make_response(jsonify(new_account.put_into_dto()), HTTPStatus.CREATED)


@account_bp.route('/api/<int:acc_id>', methods=['GET'])
def get_account(acc_id: int):
    """
    Get account by id 
    ---
    tags:
      - Account API
    """
    account = account_services.get_account_by_id(acc_id)
    if not account:
        return make_response(jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND)
    return make_response(jsonify(account.put_into_dto()), HTTPStatus.OK)


@account_bp.route('/api/<int:acc_id>', methods=['DELETE'])
def delete_account(acc_id: int):
    """
    Delete account
    ---
    tags:
      - Account API
    """
    try:
        if account_services.delete_account(acc_id):
            return make_response("Account deleted", HTTPStatus.OK)
        return make_response(jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND)
    except Exception:
        return make_response('Error during account deletion', HTTPStatus.INTERNAL_SERVER_ERROR)