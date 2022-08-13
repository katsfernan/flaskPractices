import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class OHLC (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    _open = db.Column(db.Integer, nullable = False)
    _high = db.Column(db.Integer,nullable = False)
    _low = db.Column(db.Integer, nullable = False)
    _close = db.Column(db.Integer, nullable = False)


def validate_int_list (target: list) -> bool:
    if target:
        for item in target:
            if not isinstance(item,int):
                return False
        return True

@app.route('/ohlc', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.data
        if data:
            response = []
            try:
                data = json.loads(data)
            except:
                return {'message':'The data provided is not correct'}, 400
            
            for item in data.values():
                if isinstance(item, list) and len(item) == 4 and validate_int_list(item):
                    new_record = OHLC(
                        _open = item[0], 
                        _high = item[1],
                        _low = item[2],
                        _close = item[3]
                        ) 
                    db.session.add(new_record)
                    db.session.commit()
                    response.append({
                        'id':new_record.id,
                        'open': new_record._open,
                        'high': new_record._high,
                        'low': new_record._low,
                        'close': new_record._close
                        })
            if response:
                return jsonify(
                    message='Data created successfuly',
                    data = response 
                )
            else:
                return {'message':'The data provided is not correct'}, 400
        else:
            return {'message':'No data were provided'}, 400