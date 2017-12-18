from flask import render_template, redirect, request, url_for, json, session, jsonify
from . import routes
from services import naive_bayes as nbService
from services import word_cloud as wcService

@routes.route('/test')
def defaultRoute():
    session.clear()
    return redirect(url_for('.home'))

@routes.route('/home')
def home():
    output = ""
    classifier = ""
    text = ""
    if session.get('output'):
        output = sanitize_output(session['output'])
    if session.get('classifier'):
        classifier = sanitize_output(session['classifier'])
    if session.get('text'):
        text = session['text']
    return render_template('check_text.html', text = text, output = output, classifier = classifier)

@routes.route('/check_text', methods=['POST'])
def check_text():
    session.clear()
    text = request.form.get('inputText')
    if not text == "":
        session['text'] = text
        print(text)
        a,b = nbService.check_text(text)
        if b:
            # result = json.dumps({"out":a[0], "clas":b[0]})
            session['classifier'] = b[0]
            session['output'] = a[0]
        else:
            session['output'] = a[0]
            # result = json.dumps({"out":a[0]})
        # session['result'] = result
    return redirect(url_for('.home'))

@routes.route('/word_cloud_b')
def word_cloud_b():
    weight_map = wcService.generate_cloud("b")
    # print(weight_map)
    return render_template('word-cloud.html', cloud = weight_map, classifier = "b")

@routes.route('/word_cloud_e')
def word_cloud_e():
    weight_map = wcService.generate_cloud("e")
    # print(weight_map)
    return render_template('word-cloud.html', cloud = weight_map, classifier = "e")

@routes.route('/word_cloud_m')
def word_cloud_m():
    weight_map = wcService.generate_cloud("m")
    # print(weight_map)
    return render_template('word-cloud.html', cloud = weight_map, classifier = "m")

@routes.route('/word_cloud_t')
def word_cloud_t():
    weight_map = wcService.generate_cloud("t")
    # print(weight_map)
    return render_template('word-cloud.html', cloud = weight_map, classifier = "t")

@routes.route('/twitter')
def twitter():
    return render_template('twitterSearch.html', text="", output="", classifier="")

def sanitize_output(value):
    value.strip('\'')
    if value == 'b':
        value = 'Business'
    if value == 'e':
        value = 'Entertainment'
    if value == 'm':
        value = 'Medicine'
    if value == 't':
        value = 'Technology'
    if value == 'news':
        value = 'News'
    if value == 'not_news':
        value = 'Not News'
    return value
