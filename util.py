import random, string
from flask import Flask,render_template,request,redirect,session,url_for,jsonify,Blueprint
from functools import wraps

def login_required(fn):
    @wraps(fn)
    def decorator(*args,**kwargs):
        if 'name' not in session:
            return redirect(url_for('index'))
        return fn(*args,**kwargs)
    return decorator

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)