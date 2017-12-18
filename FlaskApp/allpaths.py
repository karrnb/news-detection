from flask import Blueprint, redirect

allpaths = Blueprint('allpaths',__name__)

@allpaths.route('/')
def defaultRoute():
    return redirect('/home')

@allpaths.route('/home')
def home():
    return "Hello World"
