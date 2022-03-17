from gettext import find
from sqlalchemy import asc, desc, func
from src.DataModel.order import coin_deposit
from src.db import Session,engine
from flask import jsonify


class DepositService():
    def insetValue(value):
        db_session = Session(bind=engine)
        find_max=0
        find_min=0
        next_max=None
        prev_min=None
        check_value = None
        try:
        #check if value is already present
            check_value = db_session.query(coin_deposit.deposit).filter(coin_deposit.deposit==value).one()
            
            if not (check_value is None):
                db_session.query(coin_deposit).where(coin_deposit.deposit==value).update({"deposit_count":(coin_deposit.deposit_count+1)})
                db_session.commit()
                return jsonify({"value":value})

            else:
                # user_list = db_session.query(coin_deposit)
                next_max = db_session.query(func.min(coin_deposit.deposit)).filter(coin_deposit.deposit>value).scalar()
                prev_min = db_session.query(func.max(coin_deposit.deposit)).filter(coin_deposit.deposit<value).scalar()
                print(str(prev_min))
                find_max = db_session.query(coin_deposit).filter(coin_deposit.deposit==next_max).one()
                find_min = db_session.query(coin_deposit).filter(coin_deposit.deposit==prev_min).one()
            
                #update deposit_order
            
                db_session.query(coin_deposit).where(coin_deposit.deposit_order>=find_min.deposit_order).update({"deposit_order":(coin_deposit.deposit_order+1)})
           
                #insert the new value
           
                new_record = coin_deposit(deposit=value,deposit_order=find_min.deposit_order-1,deposit_count=1)
                db_session.add(new_record)
                db_session.flush()
                db_session.commit()
            
            
                return jsonify({"value":value,"prev min":prev_min,"next max":next_max,"prev min order id":find_min.deposit_order,"next max order id":find_max.deposit_order,"id":find_min.id, "inserted position":find_min.deposit_order-1})
        # return jsonify({"value":value,"prev_min":prev_min,"next_max":next_max,"prev_min_order_id":find_min,"next_man_order_id":find_max})
        except Exception as e:
            return jsonify({"Error":str(e)})

    def get_sorted_deposit(limit):
        db_session = Session(bind=engine)
        data = db_session.query(coin_deposit).order_by(asc(coin_deposit.deposit_order)).limit(limit)
        li = []
        for i in data:
            li.append({"deposit":i.deposit,"deposit_order":i.deposit_order,"deposit_count":i.deposit_count})
        return jsonify(li)