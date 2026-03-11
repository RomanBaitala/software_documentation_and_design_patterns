from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response, render_template, redirect, url_for
from app.models import Transaction, Payment, Transfer, Account
from app.dal.repositories import transaction_repository
from app.bll.services import transaction_service
from app.config.ext import db

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction_bp.route('/', methods=['GET'])
def list_transactions():
    """
    Render transactions list page
    ---
    tags:
      - Transaction Web
    """
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return render_template('transactions/index.html', transactions=transactions)


@transaction_bp.route('/create', methods=['GET', 'POST'])
def create_transaction_from_form():
    """
    Render transactions add page
    ---
    tags:
      - Transaction Web
    """
    if request.method == 'POST':
        try:
          data = request.form
          tx_type = data.get('type')
          sender_id = int(data.get('sender_account_id'))
          receiver_id = int(data.get('receiver_account_id'))
          amount = float(data.get('amount'))

          if tx_type == 'payment':
              merchant_name = data.get('merchant_name', 'Unknown')
              transaction_service.make_payment(
                  sender_id=sender_id,
                  merchant_id=receiver_id,
                  amount=amount,
                  merchant_name=merchant_name
              )
          else:
              transaction_service.make_transfer(
                  sender_id=sender_id,
                  receiver_id=receiver_id,
                  amount=amount
              )

          return redirect(url_for('transaction.list_transactions'))

        except ValueError as e:
          return f"Помилка бізнес-логіки: {str(e)}", 400
        except Exception as e:
          return f"Помилка сервера: {str(e)}", 500

    accounts = Account.query.all()
    return render_template('transactions/create.html', accounts=accounts)


@transaction_bp.route('/api', methods=['GET'])
def get_all_transactions():
    """
    Get all transactions (including Payments and Transfers)
    ---
    tags:
      - Transaction API
    responses:
      200:
        description: List of all transactions with specific fields
    """
    transactions = Transaction.query.all()
    return make_response(jsonify([t.put_into_dto() for t in transactions]), HTTPStatus.OK)


@transaction_bp.route('/api/<int:tx_id>', methods=['GET'])
def get_transaction(tx_id: int):
    """
    Get transaction by id
    ---
    tags:
      - Transaction API
    responses:
      200:
        description: List of all transactions with specific fields
    """
    tx = Transaction.query.get(tx_id)
    if not tx:
        return make_response(jsonify({"error": "Transaction not found"}), HTTPStatus.NOT_FOUND)
    return make_response(jsonify(tx.put_into_dto()), HTTPStatus.OK)


@transaction_bp.route('/api', methods=['POST'])
def create_transaction():
    """
    Create a new transaction (Payment or Transfer)
    ---
    tags:
      - Transaction API
    parameters:
      - in: body
        name: transaction
        schema:
          type: object
          properties:
            type: {type: string, example: "payment"}
            sender_account_id: {type: integer}
            receiver_account_id: {type: integer}
            amount: {type: number}
            merchant_name: {type: string}
            category: {type: string}
    """
    content = request.get_json()
    try:
        new_tx = Transaction.get_from_dto(content)
        db.session.add(new_tx)
        db.session.commit()
        return make_response(jsonify(new_tx.put_into_dto()), HTTPStatus.CREATED)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST)