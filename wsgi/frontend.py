#!/usr/bin/python

import re
import os

from flask import Flask, render_template, session, request,redirect,json,url_for,flash
from dropbox import client as db_client, session as db_session

import settings

app = Flask(__name__)
app.config.from_object(settings)
sess = db_session.DropboxSession(settings.DROPBOX_KEY, settings.DROPBOX_SECRET, settings.DROPBOX_ACCESS_TYPE)

def is_authorized():
    if 'access_token_key' not in session:
        return False
    if 'access_token_secret' not in session:
        return False
    sess.set_token(session['access_token_key'],session['access_token_secret'])
    return sess.is_linked()

@app.route('/', methods=['GET'])
def index():
    context={}
    context["authorized"] = is_authorized()
    if not context["authorized"]:
        request_token = sess.obtain_request_token()
        session['request_token_key']=request_token.key
        session['request_token_secret']=request_token.secret
        context["login_url"] = sess.build_authorize_url(request_token, request.host_url+url_for("db_callback"))
    else:
        client = db_client.DropboxClient(sess)
        client_info = client.account_info()
        context["name"]=client_info["display_name"]
    return render_template('base.html',context=context)

@app.route('/db_callback', methods=['GET'])
def db_callback():
    sess.set_request_token(session['request_token_key'],session['request_token_secret'])
    access_token = sess.obtain_access_token()
    session['access_token_key']=access_token.key
    session['access_token_secret']=access_token.secret
    session['uid']=request.args.get('uid')
    return redirect(url_for('index'))

@app.route('/add_url', methods=['POST'])
def add_url():
    if request.method == 'POST' and 'link' in request.form:
        id = re.match("^http?.://www.youtube.com/watch\?v=(?P<id>[a-zA-Z0-9-_]*)$",request.form['link'])
        if id:
            if not os.path.isdir(settings.JOB_DIR):
                os.makedirs(settings.JOB_DIR)
            print session
            f = open(os.path.join(settings.JOB_DIR,"%s_%s.job" % (session["uid"],id.groups("id")[0])), 'w')
            f.write(json.dumps({
                'link':request.form['link'],
                'access_token_key':session['access_token_key'],
                'access_token_secret':session['access_token_secret'],
                'id':id.groups("id")[0]
            }, separators=(',',':')))
            f.close()
            flash("Url added to download.","success");
        else:
            flash("Invalid Url.","error");
    return redirect(url_for('index'))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop("access_token_key",None)
    session.pop("access_token_secret",None)
    session.pop("uid",None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
