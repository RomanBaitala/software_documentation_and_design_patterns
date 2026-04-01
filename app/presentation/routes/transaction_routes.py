from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response, render_template, redirect, url_for
from app.models import Transaction, Payment, Transfer, Account
from app.bll.services import transaction_service, account_services
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
    transactions = transaction_service.get_all_transactions()
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

    accounts = account_services.get_all_accounts()
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
    transactions = transaction_service.get_all_transactions()
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
    tx = transaction_service.get_transaction_by_id(tx_id)
    if not tx:
        return make_response(jsonify({"error": "Transaction not found"}), HTTPStatus.NOT_FOUND)
    return make_response(jsonify(tx.put_into_dto()), HTTPStatus.OK)


@transaction_bp.route('/api', methods=['POST'])
def create_transaction():
    """
    Create a new transaction (Payment or Transfer) via BLL
    ---
    tags:
      - Transaction API
    parameters:
      - in: body
        name: transaction
        schema:
          type: object
          required: [type, sender_account_id, amount]
          properties:
            type: {type: string, example: "transfer", enum: ["payment", "transfer", "deposit"]}
            sender_account_id: {type: integer}
            receiver_account_id: {type: integer}
            amount: {type: number}
            merchant_name: {type: string}
            category: {type: string}
    responses:
      201:
        description: Transaction created successfully
      400:
        description: Business logic error
    """
    content = request.get_json()
    t_type = content.get('type')
    
    try:
        if t_type == 'transfer':
            result = transaction_service.make_transfer(
                sender_id=content['sender_account_id'],
                receiver_id=content['receiver_account_id'],
                amount=float(content['amount'])
            )
        elif t_type == 'payment':
            result = transaction_service.make_payment(
                account_id=content['sender_account_id'],
                amount=float(content['amount']),
                merchant=content.get('merchant_name'),
                category=content.get('category')
            )
        elif t_type == 'deposit':
            result = transaction_service.make_deposit(
                account_id=content['sender_account_id'],
                amount=float(content['amount'])
            )
        else:
            return jsonify({"error": "Unknown transaction type"}), HTTPStatus.BAD_REQUEST

        return make_response(jsonify(result.put_into_dto()), HTTPStatus.CREATED)

    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return make_response(jsonify({"error": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR)