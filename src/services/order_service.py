from crypt import methods
import json
from flask import Blueprint, jsonify, request
from src.DataController.deposit_service import DepositService
from src.db import Session,engine
from src.DataModel.order import coin_deposit
order_service = Blueprint('src/services/customer_service',__name__)

@order_service.get('/')
def home():
    return "Home"

@order_service.get('/get/deposit')
def get_deposit():
    db_session = Session(bind=engine)
    user_list = db_session.query(coin_deposit)
    cd_list = []
    for d in user_list:
        cd_list.append({"id":d.id,"deposit":d.deposit, "deposit_order":d.deposit_order,"deposit_count":d.deposit_count})
    return jsonify(cd_list)

@order_service.route('/insert/deposit',methods=['POST'])
def insert_value():
    data = request.json
    return DepositService.insetValue(value=data['value'])

@order_service.route("/get/ordered/deposit/<value>")
def ordered_list(value):
    return DepositService.get_sorted_deposit(value)