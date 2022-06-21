from lib2to3.pgen2 import token
from flask import Blueprint,jsonify, request
from app.models import Units,db
from .services import token_required


api=Blueprint('api',__name__, url_prefix='/api')

@api.route('/test', methods=['GET'])
def test():
    return jsonify('testing'),200


@api.route('/units',methods=['GET'])
def getUnits():

    units=Units.query.all()
    print(units)
    units=[a.to_dict() for a in units]
    return jsonify(units)

@api.route('/protoss',methods=['GET'])
def getProtoss():

    units=Units.query.all()
    punits=[]
    for a in units:
        if a.race=='Protoss':
            punits.append(a.to_dict())
    return jsonify(punits)

@api.route('/terran',methods=['GET'])
def getTerran():

    units=Units.query.all()
    tunits=[]
    for a in units:
        if a.race=='Terran':
            tunits.append(a.to_dict())
    return jsonify(tunits)

@api.route('/zerg',methods=['GET'])
def getZerg():

    units=Units.query.all()
    zunits=[]
    for a in units:
        if a.race=='Zerg':
            zunits.append(a.to_dict())
    return jsonify(zunits)

@api.route('/create',methods=['POST'])
@token_required
def createUnit():
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created=db.Column(db.DateTime, default=datetime.utcnow())
    race = db.Column(db.String(20), nullable=False)
    minerals = db.Column(db.Integer)
    vespene = db.Column(db.Integer)
    supply = db.Column(db.Integer)
    desc = db.Column(db.String(300))
    unit_tier = db.Column(db.Integer)
    unit_image = db.Column(db.String(80))
    url=db.Column(db.String(80))
    """
    try:
        newunit=request.get_json()
        a=Units(newunit)
    except:
        return jsonify({'error': ' improper request or body data'})
    try:
        db.session.add(a)
        db.session.commit()
    except:
        return jsonify({'error':'species already exists in the database'})
    return jsonify({'created':a.to_dict()})

@api.route('/unit/<string:uname>',methods=['GET'])
def getUnitName(uname):
    unit=Units.query.filter_by(name=uname.lower()).first()
    if unit:
        return jsonify(unit.to_dict()),200
    return jsonify({'error':f'no such animal with the name {uname.title()}'})

@api.route('/update/<string:uname>', methods=['POST'])
@token_required
def updateUnit(uname):
    try:
        newvals=request.get_json()
        unit=Units.query.get(uname)
        unit.from_dict(newvals)
        db.session.commit()
        return jsonify({'Updated unit':unit.to_dict()}),200
    except:
        return jsonify({'Request Failed':
        'Invalid request or unit name does not exist'}),400

@api.route('/delete/<string:uname>', methods=['DELETE'])
@token_required
def removeUnit(uname):
    unit = Units.query.get(uname.lower())
    if not unit:
        return jsonify({'Remove failed':f'No unit with name {uname} in the database.'}),404
    db.session.delete(unit)
    db.session.commit()
    return jsonify({'Removed unit':unit.to_dict()}),200