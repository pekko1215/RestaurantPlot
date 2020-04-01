from flask import Flask,render_template,request,redirect,session,url_for,jsonify,Blueprint
import util
from db import DBSession,User,Restraurant

APIRouter = Blueprint('api',__name__)

@APIRouter.route('/plot',methods=["GET"])
@util.login_required
def get_plot():
    data = DBSession.query(
        Restraurant,
        User
    ).join(
        Restraurant,
        Restraurant.created_by == User.id
    ).all()
    resp = []
    for plot in data:
        resp.append({
            'id':plot.Restraurant.id,
            'name':plot.Restraurant.name,
            'comment':plot.Restraurant.comment,
            'x':plot.Restraurant.x,
            'y':plot.Restraurant.y,
            'createdBy':plot.User.name,
            'isMine':plot.Restraurant.created_by == session['user_id']
        })
    print(resp)
    return jsonify(resp)


@APIRouter.route('/plot',methods=["POST"])
@util.login_required
def set_plot():
    if  'x' not in request.form or \
        'y' not in request.form or \
        'comment' not in request.form or \
        'name' not in request.form :
            return 'Invalid Form'
    plot = Restraurant()
    plot.x = request.form['x']
    plot.y = request.form['y']
    plot.comment = request.form['comment']
    plot.name = request.form['name']
    plot.created_by = session['user_id']


    DBSession.add(plot)
    DBSession.commit()

    return 'ok'

@APIRouter.route('/plot/<id>',methods=['DELETE'])
@util.login_required
def delete_plot(id):
    if id == None:
        return 'Invalid ID'
    plot = DBSession.query(Restraurant)\
        .filter(Restraurant.id == id)\
        .first()
    if plot == None:
        return 'Invalid ID'
    if plot.created_by != session['user_id']:
        return 'Invalid ID'
    DBSession.delete(plot)
    DBSession.commit()
    return 'ok'
    
